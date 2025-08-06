import os
import json
from collections import defaultdict
from itertools import combinations

import networkx as nx
import pickle


def dataset_writer(actor_per_movie, path, max_movies=None):
    """
    write (movie, actor) airs i to a csv file.
    if max_movies is given, only include that many movies.
    """

    seen_movies = set()

    gdataset = nx.Graph()

    movie_nodes = set()
    actor_nodes = set()

    for movie_id, actor_id, actor_name in actor_per_movie:
        if max_movies is not None and movie_id not in seen_movies:
            if len(seen_movies) >= max_movies:
                break
            seen_movies.add(movie_id)

        if movie_id not in movie_nodes:
            gdataset.add_node(movie_id, node_type="movie")
            movie_nodes.add(movie_id)

        if actor_id not in actor_nodes:
            gdataset.add_node(actor_id, node_type="actor", name=actor_name)
            actor_nodes.add(actor_id)

        gdataset.add_edge(movie_id, actor_id)

    output = os.path.join(path, "dataset.pkl")

    try:
        with open(output, "wb") as pkl_file:
            pickle.dump(gdataset, pkl_file)
            print(f"Graph pickled to {path}.")
    except IOError as e:
        print(f"Error pickling graph to {output}: {e}")

    print(f"dataset saved to graph with {gdataset}.")