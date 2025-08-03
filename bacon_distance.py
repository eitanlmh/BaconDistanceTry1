# from modules.bacon_distance_modules.graph_builder import build_actor_graph
from modules.bacon_distance_modules.bfs_search import find_bacon_distance
from modules.bacon_distance_modules.caching_json_to_graph import load_cached_graph
from modules.bacon_distance_modules.graph_builder import build_actor_graph

Kevin_Bacon_Name = "Kevin Bacon"
dataset_path = "data/parsed_data/dataset.json"
cache_path = "data/parsed_data/cached_graph.pkl"


def main():

    actor_name = input("Enter actor name: ").strip()

    try:
        print("graph making started")
        # graph, actor_id_to_name, name_to_id = load_cached_graph(dataset_path, cache_path)
        graph, actor_id_to_name, name_to_id = build_actor_graph(dataset_path)

    except FileNotFoundError as e:
        print(f"Error loading graph from JSON file: {e}")
        return

    if Kevin_Bacon_Name not in name_to_id:
        print("kevin bacon not found in the dataset")
        return

    try:
        print("dist making started")
        distance= find_bacon_distance(graph, name_to_id, actor_name)
        if distance == float("inf"):
            print(f"no connection found between kevin bacon and {actor_name}")
        else:
            print(f"bacon distance is {distance}")
    except ValueError as e:
        print(str(e))


if __name__ == "__main__":
    main()

