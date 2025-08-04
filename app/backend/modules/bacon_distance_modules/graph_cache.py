import pickle
import time

cache_path = "data/parsed_data/actor_graph_meta.pkl"

_graph = None
_actor_name_to_id = None
_actor_name_to_movie_ids = None

def load_graph():
    global _graph, _actor_name_to_id, _actor_name_to_movie_ids

    if _graph is not None:
        return _graph, _actor_name_to_id, _actor_name_to_movie_ids

    # if os.path.exists(cache_path):
    print(f"Loading cached graph from {cache_path}")
    start = time.time()
    with open(cache_path, "rb") as f:
        data = pickle.load(f)
    _graph = data['graph']
    _actor_name_to_id = data['actor_name_to_id']
    _actor_name_to_movie_ids = data['actor_name_to_movie_ids']
    print(f"Graph loaded in {time.time() - start:.2f} seconds")

    return _graph, _actor_name_to_id, _actor_name_to_movie_ids
