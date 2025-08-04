import os
from collections import defaultdict
import networkx as nx
import pickle
from itertools import combinations


data_dir = "data/parsed_data"

output_graph_pkl = os.path.join(data_dir, "actor_graph_meta.pkl")
output_actor_name_to_id_pkl = os.path.join(data_dir, "actor_name_to_id.pkl")
output_actor_name_to_movie_ids_pkl = os.path.join(data_dir, "actor_name_to_movie_ids.pkl")


def write_dataset(actor_per_movie, max_movies=None):
    """
    write (movie, actor) airs i to a csv file.
    if max_movies is given, only include that many movies.
    """
    os.makedirs(data_dir, exist_ok=True)

    seen_movies = set()
    actor_name_to_id = {}
    movie_id_to_actors_id = defaultdict(set)
    actor_name_to_movie_ids = defaultdict(set)

    G = nx.Graph()


    for movie_id, movie_name, actor_id, actor_name in actor_per_movie:
        if max_movies is not None and movie_id not in seen_movies:
            if len(seen_movies) >= max_movies:
                break
            seen_movies.add(movie_id)

        actor_name = actor_name.strip()
        actor_name_to_id[actor_name] = actor_id
        actor_name_to_movie_ids[actor_name].add(movie_id)

        movie_id_to_actors_id[movie_id].add(actor_id)

        if not G.has_node(actor_id):
            G.add_node(actor_id, name=actor_name)

    for actors in movie_id_to_actors_id.values():
        for a, b in combinations(actors, 2):
            G.add_edge(a, b)

    try:
        with open(output_graph_pkl, "wb") as pkl_file:
            pickle.dump(G, pkl_file)
            print(f"Graph pickled to {output_graph_pkl}.")
    except IOError as e:
        print(f"Error pickling graph to {output_graph_pkl}: {e}")

    try:
        with open(output_actor_name_to_id_pkl, "wb") as pkl_file:
            pickle.dump(actor_name_to_id, pkl_file)
            print(f"actor_name_to_id pickled to {output_actor_name_to_id_pkl}.")
    except IOError as e:
        print(f"Error pickling actor_name_to_id to {output_actor_name_to_id_pkl}: {e}")

    try:
        with open(output_actor_name_to_movie_ids_pkl, "wb") as pkl_file:
            pickle.dump(actor_name_to_movie_ids, pkl_file)
            print(f"actor_name_to_movie_ids pickled to {output_actor_name_to_movie_ids_pkl}.")
    except IOError as e:
        print(f"Error pickling graph to {output_actor_name_to_movie_ids_pkl}: {e}")


