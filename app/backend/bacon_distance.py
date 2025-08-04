from app.backend.modules.bacon_distance_modules.bfs_search import find_bacon_distance
from app.backend.modules.bacon_distance_modules.graph_builder import build_actor_graph
import os
import pickle
import time

cache_path = "data/parsed_data/actor_graph.pkl"
Kevin_Bacon_Name = "Kevin Bacon"
dataset_path = "data/parsed_data/dataset.json"

def load_or_build_graph():

    if os.path.exists(cache_path):
        print(f"Loading cached graph... {cache_path}")
        start_time = time.time()
        with open(cache_path, "rb") as f:
            data = pickle.load(f)
        end_time = time.time()
        print(f"Loaded cached graph in {end_time - start_time:.2f} seconds.")
        return data['graph'], data['actor_name_to_id'], data['actor_name_to_movie_ids']

    else:
        print("Building graph from scratch...")
        start_time = time.time()
        graph, actor_name_to_id, actor_name_to_movie_ids = build_actor_graph(dataset_path)
        end_time = time.time()
        print(f"Built graph in {end_time - start_time:.2f} seconds.")

        print(f"saving graph to cache: {cache_path}...")
        with open (cache_path, "wb") as f:
            pickle.dump({
                'graph': graph,
                'actor_name_to_id': actor_name_to_id,
                'actor_name_to_movie_ids': actor_name_to_movie_ids
            }, f, protocol=pickle.HIGHEST_PROTOCOL)

        print(f"cache saved successfully")

        return graph, actor_name_to_id, actor_name_to_movie_ids


def main():

    try:
        print("Graph making started(cached or note)")
        graph, actor_name_to_id, actor_name_to_movie_ids = load_or_build_graph()
        print("graph is ready")

    except FileNotFoundError as e:
        print(f"Error loading graph from JSON file: {e}")
        return

    while True:
        actor_name = input("Enter actor name (or type 'exit' to quit): ").strip().title()

        if actor_name.lower() == "exit":
            break

        if not actor_name:
            continue

        try:
            print("dist making started")
            distance= find_bacon_distance(graph, actor_name_to_id, actor_name)
            if distance == 0:
                print(f"that is kevin bacon!")
            elif distance == float("inf"):
                print(f"no connection found between kevin bacon and {actor_name}")
            else:
                print(f"bacon distance for {actor_name} is {distance}")
        except ValueError as e:
            print(str(e))


if __name__ == "__main__":
    main()

