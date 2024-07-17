import streamlit as st
# from opsci_toolbox.helpers.dataviz import generate_wordcloud, fig_bar_trend
# import matplotlib.pyplot  as plt 
# from eldar import Query
# import pandas as pd
# from opsci_toolbox.helpers.nlp import sample_most_engaging_posts, sampling_by_engagement
# from opsci_toolbox.helpers.nlp_cuml import reduce_with_cuml_UMAP, hdbscan_cuml_clustering, transform_with_cuml_UMAP, transform_with_cuml_HDBSCAN, cuml_chi2_per_category, convert_cudf_to_df, convert_df_to_cudf
# import numpy as np
# from FlagEmbedding import BGEM3FlagModel
from opsci_toolbox.helpers.sna import create_collocations, create_maximum_tree, words_partitions, compute_metrics, layout_graphviz, prepare_nodes, prepare_edges, layout_forceatlas
from opsci_toolbox.helpers.dataviz import network_graph
from opsci_toolbox.helpers.nlp import load_stopwords_df, sampling_by_engagement

date = st.session_state['date']
txt_query = st.session_state['txt_query']
ignore_case = st.session_state['ignore_case']
ignore_accent = st.session_state['ignore_accent']
match_word = st.session_state['match_word']
df = st.session_state['df']
df_filter = st.session_state['df_filter']

layout = "neato"
min_freq_nodes = st.sidebar.number_input("Minimum word frequency", min_value=1, max_value=100, value=5, step=1)
min_freq_edges = st.sidebar.number_input("Minimum edges frequency", min_value=1, max_value=100, value=7, step=1)
resolution = st.sidebar.number_input("Modularity", min_value=0.0, max_value=3.0, value=1.0, step=0.1)

min_node_size = 8
max_node_size = 40
colormap="inferno"

min_edge_size = 1
max_edge_size = 5
    
df_twitter = df_filter[df_filter['plateforme']=="Twitter"].reset_index(drop=True)
df_telegram = df_filter[df_filter['plateforme']=="Telegram"].reset_index(drop=True)

df_stopwords = load_stopwords_df("en")
st.header("Semantic analysis", divider="rainbow")
datasets = {"Telegram" :df_telegram, "Twitter": df_twitter}
for title, dataset in datasets.items():
    if len(dataset) > 0:
        if len(dataset)>1000:
            dataset = sampling_by_engagement(dataset, 'engagements', top_rows=0.5, sample_size=1000)

        edges, df_nodes = create_collocations(dataset["lemmatized_text"], min_freq_nodes, min_freq_edges, list(df_stopwords['word'].unique()))

        # on crée notre graphe
        G,T=create_maximum_tree(edges, df_nodes)

        # on calcule la modularité
        words_partitions(T, resolution)

        # on calcule les métriques de centralité
        compute_metrics(T) 

        # on positionne les points
        layout_positions = layout_graphviz(T, layout = layout)
        # layout_positions = layout_forceatlas(T, dissuade_hubs=True, scalingRatio=10)

        # on ajoute nos métadonnées
        prepare_nodes(T, layout_positions, colormap, min_node_size, max_node_size)

        prepare_edges(T, min_edge_size, max_edge_size)

        fig_similitudes = network_graph(T, col_size = "scaled_size", col_color = "modularity_color", title_text = f"{title} - Word co-occurencies", sample_nodes=0.2, show_halo=True, show_edges=True, node_mode="markers+text", width=1600, height=1200, template="plotly", plot_bgcolor="#FFFFFF")
        st.plotly_chart(fig_similitudes, use_container_width=True)
    else:
        st.write("NO DATA")



# ################################################
# # TOPIC MODELING
# ################################################
# sample_size = 1000           # total size of the sample
# top_rows = 0.3                  # number / proportion of the most important items 
# chunks_size = 100000              # size of chunks for new data points predictions
# ### UMAP PARAMETERS
# n_neighbors = 25                 # number of neighbors 25
# n_components = 2                 # number of components
# min_dist = 0.0                   # minimum grouping distance 
# metric = "cosine"                # distance metric - "hellinger" is another potential choice
# spread = 1.0
# n_epochs = 300
# learning_rate = 1.0

# ### HDBSCAN PARAMETERS
# run_soft_clustering = True           # apply a soft clustering (= all points have a vector membership)
# min_cluster_size = 50               # minimum size of cluster
# min_samples = 5                      # The number of samples in a neighborhood for a point to be considered as a core point

# ### TOPIC REPRESENTATION 
# n_words = 20                     # n words to keep for labeling
# p_value_limit = 0.95
# min_freq=3

# # SAMPLING BY ENGAGEMENT
# df_sample = sampling_by_engagement(df_filter, 'engagements', top_rows=top_rows, sample_size=sample_size)
# df_sample = df_sample.drop_duplicates(subset="translated_text").reset_index(drop=True)
# df_not_sample = df_filter[~df_filter["message_id"].isin(df_sample["message_id"].to_list())]

# model = BGEM3FlagModel('BAAI/bge-m3', use_fp16=False) 

# embeddings = model.encode(list(df_sample["translated_text"]), 
#                             batch_size=8, 
#                             max_length=8192, # If you don't need such a long length, you can set a smaller value to speed up the encoding process.
#                             )['dense_vecs']

# not_sample_embeddings = model.encode(list(df_not_sample["translated_text"]), 
#                             batch_size=8, 
#                             max_length=8192, # If you don't need such a long length, you can set a smaller value to speed up the encoding process.
#                             )['dense_vecs']

# # reducer, sample_reduced_embeddings = reduce_with_cuml_UMAP(np.array(df_sample["embeddings"].tolist()), n_neighbors = n_neighbors, n_components = n_components, min_dist = min_dist, metric = metric, spread=spread, learning_rate=learning_rate, n_epochs=n_epochs)
# reducer, sample_reduced_embeddings = reduce_with_cuml_UMAP(embeddings, n_neighbors = n_neighbors, n_components = n_components, min_dist = min_dist, metric = metric, spread=spread, learning_rate=learning_rate, n_epochs=n_epochs)

# clusterer, sample_labels, sample_probas = hdbscan_cuml_clustering(sample_reduced_embeddings, min_cluster_size=min_cluster_size, min_samples=min_samples, prediction_data = True)
# df_sample['topic'] = sample_labels.astype(int).astype(str)
# df_sample['probas'] = sample_probas

# not_sample_reduced_embeddings = transform_with_cuml_UMAP(reducer, not_sample_embeddings)

# # not_sample_reduced_embeddings = transform_with_cuml_UMAP(reducer, np.array(df_not_sample["embeddings"].tolist()))
# not_sample_labels, not_sample_probas = transform_with_cuml_HDBSCAN(clusterer, not_sample_reduced_embeddings)
# df_not_sample['topic'] = not_sample_labels.astype(int).astype(str)
# df_not_sample['probas'] = not_sample_probas
# df_new = pd.concat([df_sample, df_not_sample]).reset_index(drop=True)

# st.write(df_new.head())

# col_topic = "topic"
# df_chi = cuml_chi2_per_category(df_filter["lemmatized_text"], df_filter[col_topic].astype(str), col_topic, n_words = n_words, p_value_limit=p_value_limit, min_freq=min_freq)
# df_chi=df_chi.reset_index(drop=True)
# df_chi_gb = df_chi.groupby(col_topic).agg({"relevant_words_chi2":lambda x: " | ".join(list(x))}).reset_index()
