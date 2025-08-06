import pickle
import time
import sys
from collections import deque

real_cache_path = "data/real_parsed_data/dataset.pkl"
example_cache_path = "data/example_parsed_data/dataset.pkl"


def load_graph_from_pkl(cache_path):
    with open(cache_path, "rb") as f:
        return pickle.load(f)

def find_actor_id_by_name(graph, actor_name):
    for node, data in graph.nodes(data=True):
        if data.get("node_type") == "actor" and data.get("name", "").lower() == actor_name.lower():
            return node
    return None

def bfs_actor_distance(graph, source_actor_id, target_actor_id):
    if source_actor_id not in graph or target_actor_id not in graph:
        return None

    visited = set()
    queue = deque([(source_actor_id, 0)])

    while queue:
        current_node, dist = queue.popleft()

        if current_node == target_actor_id:
            return dist // 2

        visited.add(current_node)

        for neighbor in graph.neighbors(current_node):
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append((neighbor, dist + 1))
    return None

def main(cache_path, Kevin_Bacon=None):
    graph = load_graph_from_pkl(cache_path)
    print(graph)
    print("Type actor name (or exit to quit): ")

    while True:
        actor_name = input("actor name: ").strip().title()

        if actor_name.lower() == "exit":
            print("goodbye")
            break

        target_actor_id = find_actor_id_by_name(graph, actor_name)

        if not target_actor_id:
            print("actor name doesn't exist")
            continue

        distance = bfs_actor_distance(graph, Kevin_Bacon, target_actor_id)

        if distance is not None:
            print(f"bacon distance to {actor_name} is: {distance}!")
        else:
            print(f" no path found from {actor_name} from kevin bacon!")


if __name__ == "__main__":
    main(example_cache_path, Kevin_Bacon="nm0000002")
    #main(real_cache_path, Kevin_Bacon="nm0000102")

    #you can choose:
    # 1. real_cache_path, define kevon bacon to be nm0000102 like so - main(real_cache_path, Kevin_Bacon=="nm0000102")
    # 2. example_cache_path define kevon bacon to be nm0000002 like so - main(real_cache_path, Kevin_Bacon=="nm0000002")

