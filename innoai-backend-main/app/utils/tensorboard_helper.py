import os
import numpy as np
import tensorflow as tf
from tensorboard.plugins import projector

def save_embeddings(embeddings, metadata, log_dir):
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    # Check if embeddings and metadata are not empty
    if not embeddings or not metadata:
        raise ValueError("Embeddings or metadata are empty")

    # Save embeddings
    embedding_file = os.path.join(log_dir, "embeddings.tsv")
    np.savetxt(embedding_file, embeddings, delimiter='\t')

    # Save metadata
    metadata_file = os.path.join(log_dir, "metadata.tsv")
    with open(metadata_file, 'w') as f:
        for meta in metadata:
            f.write(meta + '\n')

def setup_tensorboard(log_dir):
    embedding_file_path = os.path.join(log_dir, "embeddings.tsv")
    metadata_file_path = os.path.join(log_dir, "metadata.tsv")

    if not (os.path.exists(embedding_file_path) and os.path.getsize(embedding_file_path) > 0):
        raise FileNotFoundError(f"Embeddings file not found or empty at {embedding_file_path}")
    if not (os.path.exists(metadata_file_path) and os.path.getsize(metadata_file_path) > 0):
        raise FileNotFoundError(f"Metadata file not found or empty at {metadata_file_path}")

    # Load the embeddings
    embeddings = np.loadtxt(embedding_file_path, delimiter="\t")
    embedding_var = tf.Variable(embeddings, name='embeddings')

    # Create a checkpoint from embedding variable
    checkpoint = tf.train.Checkpoint(embedding=embedding_var)
    checkpoint_path = os.path.join(log_dir, 'embeddings.ckpt')
    checkpoint.save(file_prefix=checkpoint_path)

    # Set up projector configuration
    config = projector.ProjectorConfig()
    embedding = config.embeddings.add()
    embedding.tensor_name = embedding_var.name
    embedding.metadata_path = os.path.basename(metadata_file_path)

    # Write projector configuration file
    projector_filepath = os.path.join(log_dir, 'projector_config.pbtxt')
    with open(projector_filepath, "w") as f:
        f.write(str(config))

    # Use a summary writer to log the embedding
    summary_writer = tf.summary.create_file_writer(log_dir)
    with summary_writer.as_default():
        projector.visualize_embeddings(summary_writer, config)