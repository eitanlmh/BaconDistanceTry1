import json
from collections import defaultdict
import os
from itertools import combinations
import ijson

def build_actor_graph (json_path):

    if not os.path.exists(json_path):
        raise FileNotFoundError(f"dataset file {json_path} not found")

    graph = defaultdict(set)
    movie_to_actors = defaultdict(set)
    actor_id_to_name = {}
    name_to_id = defaultdict(set)

    with open(json_path, "rb") as json_f:
        rows = ijson.items(json_f, 'item')
        # print(rows)
        for row in rows:
            movie_id = row["movie_id"]
            actor_id = row["actor_id"]
            actor_name = row["actor_name"].strip()

            actor_id_to_name[actor_id] = actor_name
            movie_to_actors[movie_id].add(actor_id)
            name_to_id[actor_name].add(actor_id)

    for actors in movie_to_actors.values():
        for a, b in combinations(actors, 2):
            graph[a].add(b)
            graph[b].add(a)
        # actors_list = list(actors)
        # for i in range(len(actors_list)):
        #     for j in range(i+1, len(actors_list)):
        #         a, b = actors_list[i], actors_list[j]
        #         graph[a].add(b)
        #         graph[b].add(a)

    return graph, actor_id_to_name, name_to_id

