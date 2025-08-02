import json
from collections import defaultdict
import os

def build_graph (json_path):

    if not os.path.exists(json_path):
        raise FileNotFoundError(f"dataset file {json_path} not found")

    with open(json_path, encoding="utf-8") as json_f:
        data = json.load(json_f)

    graph = defaultdict(set)
    movie_to_actors = defaultdict(set)
    actor_id_to_name = {}

    for row in data:
        movie_id = row["movie_id"]
        actor_id = row["actor_id"]
        actor_name = row["actor_name"].strip()

        actor_id_to_name[actor_id] = actor_name
        movie_to_actors[movie_id].add(actor_id)

    for actors in movie_to_actors.values():
        actors_list = list(actors)
        for i in range(len(actors_list)):
            for j in range(i+1, len(actors_list)):
                a, b = actors_list[i], actors_list[j]
                graph[a].add(b)
                graph[b].add(a)

    return graph, actor_id_to_name

