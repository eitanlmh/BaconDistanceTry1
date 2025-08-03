import pickle
import os
from modules.bacon_distance_modules.graph_builder import build_actor_graph

def load_cached_graph(json_path, pickle_path):

    if os.path.exists(pickle_path):
        with open(pickle_path, "rb") as f:
            return pickle.load(f)

    print("cache not found, parsing json")
    graph, actor_id_to_name, name_to_id = build_actor_graph(json_path)

    with open(pickle_path, "wb") as f:
        pickle.dump((graph, actor_id_to_name, name_to_id), f)

    return graph, actor_id_to_name, name_to_id