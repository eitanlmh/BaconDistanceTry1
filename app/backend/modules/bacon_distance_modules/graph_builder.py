from collections import defaultdict
import os
from itertools import combinations
import ijson
import networkx as nx

def build_actor_graph (json_path):
    if not os.path.exists(json_path):
        raise FileNotFoundError(f"dataset file {json_path} not found")

    actor_graph = nx.Graph()
    actor_name_to_id = {}
    movie_to_actors = defaultdict(set)
    actor_name_to_movie_ids = defaultdict(set)

    print(f"Loading dataset from {json_path}")
    with open(json_path, "rb") as json_file:

        for line in ijson.items(json_file, 'item'):
            try:
                movie_id = line["movie_id"]
                actor_id = line["actor_id"]
                actor_name = line["actor_name"].strip()

                actor_name_to_id[actor_name] = actor_id
                actor_name_to_movie_ids[actor_name].add(movie_id)

                movie_to_actors[movie_id].add(actor_id)

                actor_graph.add_node(actor_id, name=actor_name)
            except KeyError as e:
                print(f"skipping line dut to missing key: {e}. line: {line}")
                continue

    print(f"Finished processing records. building graph edges.")

    for actors in movie_to_actors.values():
            for a, b in combinations(actors, 2):
                actor_graph.add_edge(a, b)

    return actor_graph, actor_name_to_id, actor_name_to_movie_ids


