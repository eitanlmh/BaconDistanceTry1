import os
import json
import networkx as nx
import matplotlib as plo
data_dir = "data/parsed_data"
output = os.path.join(data_dir, "dataset.json")
output_graph_png = os.path.join(data_dir, "movie_actor_graph.png")
output_graph_gml = os.path.join(data_dir, "movie_actor_graph.gml")

def write_dataset(actor_per_movie, max_movies=None):
    """
    write (movie, actor) airs i to a csv file.
    if max_movies is given, only include that many movies.
    """
    os.makedirs(data_dir, exist_ok=True)

    seen_movies = set()
    dataset = []

    G = nx.Graph()

    for movie_id, movie_name, actor_id, actor_name in actor_per_movie:
        if max_movies is not None and movie_id not in seen_movies:
            if len(seen_movies) >= max_movies:
                break
            seen_movies.add(movie_id)

        dataset.append({
            "movie_id": movie_id,
            "movie_name": movie_name,
            "actor_id": actor_id,
            "actor_name": actor_name
        })

        movie_node = f"{movie_id}"
        actor_node = f"{actor_id}"

        G.add_node(movie_node, type="movie", name=movie_name)
        G.add_node(actor_node, type="actor", name=actor_name)
        G.add_edge(movie_node, actor_node)

    try:
        with open(output, mode='w',encoding="utf-8") as file:
            json.dump(dataset, file, ensure_ascii=False, indent=2)
            print(f"dataset saved to {output} with {len(dataset)} rows.")
    except IOError as e:
        print(f"error writing to file {output}: {e}")
        return

    try:
        nx.write_gml(G, output_graph_gml)
        print(f"visual graph saved to {output_graph_gml}.")
    except IOError as e:
        print(f"error writing to file {output_graph_gml}: {e}")

