from flask import Flask, render_template, request
import threading
import os
from app.backend.bacon_distance import load_graph_from_pkl, find_actor_id_by_name, bfs_actor_distance
from app.backend.generate_db import generate_db

app = Flask(__name__)

#global vars to hold the loaded data

graph = None
data_source = None
bacon_id = None
@app.route("/", methods=["GET"])
def choose_data():
    return render_template("choose_data.html")

@app.route("/distance", methods=["GET", "POST"])
def main():
    global graph, data_source, bacon_id

    if request.method == "GET":
        data_source = request.args.get("data_source")
        print(f"data_source: {data_source}")

        def load_data():
            global graph, bacon_id
            if data_source == "example":
                base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "backend", "data", "example_parsed_data"))
                bacon_id = "nm0000002"
            else:
                base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "backend", "data", "real_parsed_data"))
                bacon_id = "nm0000102"

            graph_path = os.path.join(base_path, "dataset.pkl")

            if not (os.path.exists(graph_path)):
                print(f"{data_source} dataset not found. Running generate_db({data_source})...")
                generate_db(data_source)
            else:
                print(f"{data_source} cached dataset found. Skipping generate_db({data_source})...")

            graph = load_graph_from_pkl(graph_path)

            print("Cache loaded")


        db_thread = threading.Thread(target=load_data)
        db_thread.start()
        db_thread.join()


    finale_answer = None

    if request.method == "POST":
        actor_name = request.form.get("actor_name")

        if actor_name and graph:
            target_actor_id = find_actor_id_by_name(graph, actor_name)

            if not target_actor_id:
                finale_answer = f"{actor_name} actor is not found! try again"
            else:
                distance = bfs_actor_distance(graph, bacon_id, target_actor_id)


                if isinstance(distance, int):
                    if distance == 0:
                        finale_answer = "This is Kevin Bacon!"
                    elif distance == float("inf"):
                        finale_answer = f"No connection was found between Kevin Bacon and {actor_name}"
                    else:
                        finale_answer = f"Bacon distance for {actor_name} is {distance}"
                else:
                    finale_answer = "No actor name was provided"

    return render_template("main_page.html", result=finale_answer)


if __name__ == "__main__":
    app.run(debug=True)