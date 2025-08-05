import time
from flask import Flask, render_template, request
import threading
import os
from app.backend.bacon_distance import get_bacon_distance
import pickle

from app.backend.generate_db import generate_db

app = Flask(__name__)

#global vars to hold the loaded data
example_graph = None
example_actor_name_to_id = None

graph = None
actor_name_to_id = None
actor_name_to_movie_ids = None

data_source = None

example_graph_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "backend", "data", "example_parsed_data", "actor_graph_meta.pkl"))
real_graph_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "backend", "data", "parsed_data", "actor_graph_meta.pkl"))


@app.route("/", methods=["GET"])
def choose_data():
    return render_template("choose_data.html")

@app.route("/distance", methods=["GET", "POST"])
def main():
    global graph, actor_name_to_id, actor_name_to_movie_ids, data_source, example_graph_path, real_graph_path

    if request.method == "GET":
        data_source = request.args.get("data_source")
        print(f"data_source: {data_source}")

        def load_data():
            global graph, actor_name_to_id

            if data_source == "example":
                base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "backend", "data", "example_parsed_data"))
            else:
                base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "backend", "data", "parsed_data"))

            graph_path = os.path.join(base_path, "actor_graph_meta.pkl")
            actor_name_to_id_path = os.path.join(base_path, "actor_name_to_id.pkl")

            if not (os.path.exists(graph_path) and os.path.exists(actor_name_to_id_path)):
                print(f"{data_source} dataset not found. Running generate_db({data_source})...")
                generate_db(data_source)
            else:
                print(f"{data_source} cached dataset found. Skipping generate_db({data_source})...")

            with open(graph_path, "rb") as f:
                graph = pickle.load(f)

            with open(actor_name_to_id_path, "rb") as f:
                actor_name_to_id = pickle.load(f)

            print("Cache loaded")


        db_thread = threading.Thread(target=load_data)
        db_thread.start()
        db_thread.join()


    finale_answer = None

    if request.method == "POST":
        actor_name = request.form.get("actor_name")

        if actor_name and graph and actor_name_to_id:
            distance = get_bacon_distance(actor_name, graph, actor_name_to_id)


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