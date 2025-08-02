import sys
from modules.bacon_distance_modules.graph_builder import load_graph_from_json
from modules.bacon_distance_modules.actor_lookup import build_name_id_mapping
from modules.bacon_distance_modules.bfs_search import find_bacon_distance

Kevin_Bacon_Name = "Kevin Bacon"
dataset_path = "data/parsed_data/dataset.json"
def main():

    actor_name = input("Enter actor name: ")

    try:
        graph, actor_id_to_name = load_graph_from_json(dataset_path)
    except FileNotFoundError as e:
        print(f"Error loading graph from JSON file: {e}")
        return

    name_to_ids, actor_id_to_name = build_name_id_mapping(actor_id_to_name)

    if (Kevin_Bacon_Name not in name_to_ids):
        print("kevin bacon not found in the dataset")
        return

    kevin_bacon_ids = name_to_ids[Kevin_Bacon_Name]
    kevin_bacon_id = next(iter(kevin_bacon_ids))

    try:
        distance= find_bacon_distance(graph, name_to_ids, kevin_bacon_id, actor_name)
        if distance == float("inf"):
            print(f"no connection found between kevin bacon and {actor_name}")
        else:
            print(f"bacon distance is {distance}")
    except ValueError as e:
        print(str(e))


if __name__ == "__main__":
    main()

