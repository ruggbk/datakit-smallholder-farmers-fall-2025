from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
import umap
from sklearn.cluster import HDBSCAN
from sklearn.metrics import silhouette_score
import time

# -------------------------------------------------------------------
# UMAP + HDBSCAN clustering
# -------------------------------------------------------------------

def cluster_with_umap_hdbscan(
        df,
        sample_size=None,         # e.g. 100_000
        umap_params=None,
        hdbscan_params=None,
        random_state=42,
        silhouette_sample=10000   # number of points to subsample for silhouette
    ):
    """
    Run UMAP + HDBSCAN on all data or a random sample.

    Returns:
        result_df: copy of (subsampled) df with cluster labels
        umap_embeddings: np.ndarray of reduced vectors
        clusterer: fitted HDBSCAN instance
        silhouette: approximate silhouette score (excluding noise)
    """

    t0 = time.time()

    # ---- Sampling --------------------------------------------------------
    if sample_size is not None and sample_size < len(df):
        sampled_df = df.sample(n=sample_size, random_state=random_state)
    else:
        sampled_df = df.copy()

    # ---- Defaults --------------------------------------------------------
    if umap_params is None:
        umap_params = dict(
            n_neighbors=30,
            n_components=5,
            metric='cosine',
            random_state=random_state
        )

    if hdbscan_params is None:
        hdbscan_params = dict(
            min_cluster_size=250,
            min_samples=10,
            metric='euclidean',
            cluster_selection_method='eom'
        )

    # ---- UMAP ------------------------------------------------------------
    reducer = umap.UMAP(**umap_params)
    X = np.vstack(sampled_df["embedding"].to_numpy()).astype("float32")
    umap_embeddings = reducer.fit_transform(X)

    # ---- HDBSCAN ---------------------------------------------------------
    clusterer = HDBSCAN(**hdbscan_params)
    labels = clusterer.fit_predict(umap_embeddings)

    # ---- Attach results --------------------------------------------------
    result_df = sampled_df.copy()
    result_df["cluster"] = labels

    # ---- Diagnostics -----------------------------------------------------
    noise_ratio = (labels == -1).mean()
    n_clusters = len(set(labels)) - (1 if -1 in labels else 0)
    duration = time.time() - t0

    print(f"Finished clustering in {duration:.1f} seconds")
    print(f"Noise ratio: {noise_ratio:.2%}")
    print(f"Clusters found: {n_clusters}")

    # ---- Approximate silhouette score -----------------------------------
    labels_no_noise = labels[labels != -1]
    emb_no_noise = umap_embeddings[labels != -1]
    silhouette = None
    if len(set(labels_no_noise)) > 1:
        n_points = len(labels_no_noise)
        if n_points > silhouette_sample:
            # Subsample for speed
            idx = np.random.choice(np.arange(n_points), size=silhouette_sample, replace=False)
            silhouette = silhouette_score(emb_no_noise[idx], labels_no_noise[idx], metric='cosine')
        else:
            silhouette = silhouette_score(emb_no_noise, labels_no_noise, metric='cosine')
        print(f"Approx. silhouette score (excluding noise): {silhouette:.3f}")

    return result_df, umap_embeddings, clusterer

# -------------------------------------------------------------------
# Re-cluster members of noise cluster (-1) for re-integration with main clusters
# -------------------------------------------------------------------
def recluster_noise(umap_embeddings, labels, hdbscan_params=None):
    """
    Recluster noise points (-1) from a previous HDBSCAN run in the same UMAP space.
    Returns: new labels (shifted to avoid collisions), HDBSCAN object
    """
    hdbscan_params = hdbscan_params or dict(min_cluster_size=50, min_samples=5, metric='euclidean', cluster_selection_method='eom')

    noise_mask = labels == -1
    noise_embeddings = umap_embeddings[noise_mask]

    clusterer = HDBSCAN(**hdbscan_params)
    noise_labels = clusterer.fit_predict(noise_embeddings)

    # Shift labels to avoid collisions with main clusters
    max_label = labels.max()
    noise_labels_shifted = np.where(noise_labels != -1, noise_labels + max_label + 1, -1)

    # Output diagnostics
    noise_ratio = (noise_labels == -1).mean()
    n_clusters = len(set(noise_labels)) - (1 if -1 in noise_labels else 0)
    print(f"Reclustered noise points: {len(noise_labels)}")
    print(f"New noise ratio: {noise_ratio:.2%}")
    print(f"Clusters found in noise: {n_clusters}")

    return noise_labels_shifted, clusterer


# -------------------------------------------------------------------
# Print list of example questions from clusters
# -------------------------------------------------------------------

def print_cluster_examples(
    df,
    text_column="Q_basic_clean",
    cluster_column="cluster",
    top_n=20,
    examples_per_cluster=5,
    exclude_noise=True,
    random_examples=False,
):
    """
    Print sample text examples from the largest clusters in a clustered DataFrame.
    """
    if cluster_column not in df.columns:
        raise ValueError(f"Column '{cluster_column}' not found in DataFrame.")

    if text_column not in df.columns:
        raise ValueError(f"Column '{text_column}' not found in DataFrame.")
    
    # Cluster counts
    cluster_counts = df[cluster_column].value_counts()

    # Optionally remove noise cluster (-1)
    if exclude_noise and -1 in cluster_counts.index:
        cluster_counts = cluster_counts[cluster_counts.index != -1]

    # Select largest clusters
    top_clusters = cluster_counts.head(top_n).index.tolist()

    # Print examples
    for cluster_id in top_clusters:
        size = cluster_counts[cluster_id]
        print(f"\n--- Cluster {cluster_id} (size={size}) ---")

        subset = df[df[cluster_column] == cluster_id]

        if random_examples:
            examples = subset[text_column].sample(
                min(examples_per_cluster, len(subset)),
                random_state=42
            )
        else:
            examples = subset[text_column].head(examples_per_cluster)

        for q in examples:
            print("-", q)

# -------------------------------------------------------------------
# Summarize clusters with keywords
# -------------------------------------------------------------------

def summarize_clusters(
    df,
    text_col='Q_basic_clean',
    cluster_col='cluster',
    meta_col=None,
    top_n_words=5,
    max_features=5000,
    extra_stop_words=None,
    sample_questions=0,      
    random_samples=False,    
    preview=False             
):
    """
    Generate keyword summaries for clusters, optionally including:
      - meta-cluster labels
      - sample questions
      - printed preview
    
    Returns a DataFrame with:
      ['cluster', 'size', 'keywords', (optional) 'meta_label', (optional) 'samples']
    """
    
    # Stop words
    if extra_stop_words is None:
        stop_words = 'english'
    else:
        stop_words = list(ENGLISH_STOP_WORDS.union(set(extra_stop_words)))

    # Fit TF-IDF on whole corpus
    vectorizer = TfidfVectorizer(stop_words=stop_words, max_features=max_features)
    vectorizer.fit(df[text_col])
    terms = vectorizer.get_feature_names_out()
    
    cluster_rows = []
    
    for cluster_id in sorted(df[cluster_col].unique()):
        subset = df[df[cluster_col] == cluster_id]
        cluster_texts = subset[text_col]
        
        # TF-IDF keyword extraction
        tfidf_matrix = vectorizer.transform(cluster_texts)
        mean_scores = tfidf_matrix.mean(axis=0).A1
        top_indices = mean_scores.argsort()[-top_n_words:][::-1]
        top_terms = [terms[i] for i in top_indices]

        # Base info
        row = {
            'cluster': cluster_id,
            'size': len(subset),
            'keywords': ", ".join(top_terms)
        }

        # Optional meta label
        if meta_col is not None and meta_col in df.columns:
            row['meta_label'] = subset[meta_col].iloc[0]

        # Optional sampled questions
        if sample_questions > 0:
            if random_samples:
                samples = subset[text_col].sample(
                    min(sample_questions, len(subset)),
                    random_state=42
                ).tolist()
            else:
                samples = subset[text_col].head(sample_questions).tolist()
            
            row['samples'] = samples
        
        cluster_rows.append(row)

    summary_df = pd.DataFrame(cluster_rows)

    # Optional formatted preview printing
    if preview:
        for _, r in summary_df.iterrows():
            print(f"\n=== Cluster {r['cluster']} (size={r['size']}) ===")
            print("Keywords:", r['keywords'])
            if 'meta_label' in r:
                print("Meta:", r['meta_label'])
            if 'samples' in r:
                print("Sample questions:")
                for q in r['samples']:
                    print("  -", q)

    return summary_df

# -------------------------------------------------------------------
# Preview metacluster for quality check
# -------------------------------------------------------------------
def metacluster_preview(df, metacluster_num: int = 0, meta_titles=None) -> None:
    """
    Print a preview of all clusters belonging to a specified meta-cluster.

    Args:
        df (pd.DataFrame): DataFrame containing cluster info, with columns:
                           'meta_label', 'cluster', 'size', 'keywords', and optionally 'samples'.
        metacluster_num (int, optional): Index of the meta-cluster in `meta_titles`. Defaults to 0.
    """
#     if meta_titles:
#         meta_label = meta_titles[metacluster_num]
#     else:
#         meta_label = metacluster_num
#     metacluster_df = df[df['meta_label'] == meta_label]

#     print(f"Previewing Meta-cluster {metacluster_num}: {meta_label}")

#     for _, row in metacluster_df.iterrows():
#         print(f"\n=== Cluster {row['cluster']} (size={row['size']}) ===")
#         print("Keywords:", row['keywords'])
#         if 'samples' in row and row['samples']:
#             print("Sample questions:")
#             for question in row['samples']:
#                 print("  -", question)

    if meta_titles:
        meta_label_title = meta_titles[metacluster_num]
    else:
        meta_label_title = metacluster_num

    metacluster_df = df[df['meta_label'] == metacluster_num]

    print(f"Previewing Meta-cluster {metacluster_num}: {meta_label_title}")

    for _, row in metacluster_df.iterrows():
        print(f"\n=== Cluster {row['cluster']} (size={row['size']}) ===")
        print("Keywords:", row['keywords'])
        if 'samples' in row and row['samples']:
            print("Sample questions:")
            for question in row['samples']:
                print("  -", question)

