import os
import joblib
import pandas as pd
import numpy as np
import duckdb
from pathlib import Path
# -------------------------------------------------------------------
# Quick save various files in data directory if they do not already exist
# -------------------------------------------------------------------
def quick_save_file(data_dir, filename, obj):
    """
    Save an object to the specified data directory if it does not already exist.
    Automatically handles pandas DataFrames and NumPy arrays for optimal speed.
    
    Parameters:
        data_dir (str): Directory where the file should be saved.
        filename (str): Name of the file (include extension, e.g., .pkl, .parquet, .npy).
        obj: Object to save. If filename ends with .parquet, obj must be a pandas DataFrame.
             If obj is a NumPy array, it will be saved as .npy for speed if possible.
    """
    path = os.path.join(data_dir, filename)
    
    if os.path.exists(path):
        print(f"{filename} already exists. Skipping save.")
        return

    # Handle pandas DataFrames
    if isinstance(obj, pd.DataFrame) or filename.endswith(".parquet"):
        obj.to_parquet(path)
    # Handle NumPy arrays
    elif isinstance(obj, np.ndarray):
        # Ensure .npy extension for speed
        if not filename.endswith(".npy"):
            path = os.path.splitext(path)[0] + ".npy"
        np.save(path, obj)
    # Fallback for other objects
    else:
        joblib.dump(obj, path)  # turn off compression for speed
    
    print(f"Saved {os.path.basename(path)}")


# -------------------------------------------------------------------
# Save output of UMAP and HDBSCAN clustering for a set topic
# -------------------------------------------------------------------

def save_topic_files(data_dir, topic, clusterer, umap_embedding, df):
    """
    Saves the clusterer, UMAP embedding, and clustered DataFrame for a given topic.
    
    Parameters:
        data_dir (str): Directory where files should be saved.
        topic (str): Topic name used in filenames.
        clusterer: The clustering model object to save (e.g., HDBSCAN).
        umap_embedding: The UMAP embedding object to save.
        df: The clustered DataFrame to save as parquet.
    """
    files_to_save = {
        f"{topic}_hdbscan_model.pkl": clusterer,
        f"{topic}_umap_embedding.pkl": umap_embedding,
        f"{topic}_clustered_df.parquet": df
    }

    for filename, obj in files_to_save.items():
        path = os.path.join(data_dir, filename)
        if not os.path.exists(path):
            if filename.endswith(".parquet"):
                obj.to_parquet(path)
            else:
                joblib.dump(obj, path)
            print(f"Saved {filename}")
        else:
            print(f"{filename} already exists. Skipping save.")

# -------------------------------------------------------------------
# Save minimal question cluster data with UMAP embeddings to be reattached to full dataset
# -------------------------------------------------------------------

def save_question_clusters(df, embedding_2d, topic, folder='../data'):
    """
    Save minimal question cluster data with UMAP embeddings.

    Parameters
    ----------
    df : pd.DataFrame
        Original DataFrame with 'question_id', 'cluster', 'meta_label'.
    embedding_2d : np.ndarray
        2D UMAP embeddings (n_rows, 2).
    topic : str
        Topic name (e.g., 'unlabeled', 'chicken', 'maize').
    folder : str
        Folder to save the Parquet file.
    """
    minimal_df = df[['question_id', 'meta_label', 'cluster']].copy()
    # Downcast integer columns
    minimal_df = minimal_df.astype({'question_id': 'int32',
                                    'cluster': 'int32',
                                    'meta_label': 'int32'})
    # Add 2D UMAP embeddings as float32
    minimal_df['umap_x'] = embedding_2d[:, 0].astype('float32')
    minimal_df['umap_y'] = embedding_2d[:, 1].astype('float32')
    
    filename = f"{folder}/question_clusters_{topic}.parquet"
    minimal_df.to_parquet(filename, index=False)
    print(f"Saved {filename} ({minimal_df.shape[0]} rows)")


# -------------------------------------------------------------------
# Load and join question data with embeddings
# -------------------------------------------------------------------


def load_clustered_questions(full_path, cluster_path, topic):
    """
    Load the large WeFarm 'full dataset' (e.g. "b0cd514b-b9cc-4972-a0c2-c91726e6d825.csv", CSV or Parquet) and join it with the cluster
    annotation file (always Parquet). Returns a Pandas DataFrame of the joined data.
    """

    full_path = Path(full_path)
    cluster_path = Path(cluster_path)

    con = duckdb.connect()

    # Detect the format of the full dataset
    if full_path.suffix.lower() in ['.csv', '.txt']:
        full_reader = f"read_csv_auto('{full_path.as_posix()}', HEADER=True)"
    elif full_path.suffix.lower() in ['.parquet']:
        full_reader = f"read_parquet('{full_path.as_posix()}')"
    else:
        raise ValueError(f"Unsupported full dataset file type: {full_path.suffix}")

    # Build WHERE clause for topic
    if topic is None:
        where_clause = "WHERE f.question_topic IS NULL AND f.question_language = 'eng'"
    else:
        where_clause = f"WHERE f.question_topic = '{topic}' AND f.question_language = 'eng'"

    # Cluster labels are always Parquet
    cluster_reader = f"read_parquet('{cluster_path.as_posix()}')"

    query = f"""
    SELECT f.question_id, f.question_content, c.cluster, c.meta_label, c.umap_x, c.umap_y
    FROM {full_reader} AS f
    RIGHT JOIN {cluster_reader} AS c
    ON f.question_id = c.question_id
    {where_clause}
    """

    df = con.execute(query).df()
    df = df.drop_duplicates(subset='question_id', keep='first')

    return df