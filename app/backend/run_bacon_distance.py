from app.backend.modules.bacon_distance_modules.graph_builder import build_actor_graph
from app.backend.modules.bacon_distance_modules.bfs_search import find_bacon_distance
import os
import pickle
import time

cache_path = "app/backend/data/parsed_data/actor_graph.pkl"
dataset_path = "app/backend/data/parsed_data/dataset.json"

graph = None
actor_name_to_id = None
actor_name_to_movie_ids = None

def load_data():
    global graph, actor_name_to_id, actor_name_to_movie_ids

    if graph is not None:
        return

    if os.path.exists(cache_path):
        with open(cache_path, "rb") as f:
            data = pickle.load(f)

        graph = data["graph"]
        actor_name_to_id = data["actor_name_to_id"]
        actor_name_to_movie_ids = data["actor_name_to_movie_ids"]
    else:
        graph, actor_name_to_id, actor_name_to_movie_ids = build_actor_graph()
        with open(cache_path, "wb") as f:
            pickle.dump({
                'graph': graph,
                'actor_name_to_is': actor_name_to_id,
                'actor_name_to_movie_ids': actor_name_to_movie_ids,
            }, f, protocol=pickle.HIGHEST_PROTOCOL)

def get_bacon_distance(actor_name):
    load_data()

    try:
        distance = find_bacon_distance(graph, actor_name_to_id, actor_name)
        return distance
    except ValueError as e:
        return str(e)