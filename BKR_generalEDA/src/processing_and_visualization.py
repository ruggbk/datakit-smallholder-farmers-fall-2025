import os
import joblib
import pandas as pd
import numpy as np
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

