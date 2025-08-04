import time

from flask import Flask, make_response, render_template, session, redirect, request
import threading
import subprocess
import os
from app.backend.bacon_distance import get_bacon_distance
import pickle
app = Flask(__name__)

#global vars to hold the loaded data
graph = None
actor_name_to_id = None
actor_name_to_movie_ids = None


def run_generate_db():
    backend_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "backend"))
    dataset_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", backend_path, "data", "parsed_data", "actor_graph_meta.pkl"))

    if not os.path.exists(dataset_path) :
        print("Dataset not found. running generate_db.py...")
        subprocess.run(["python", "generate_db.py"], cwd = backend_path)
    else:
        print("dataset and cached dataset found. skipping generate_db.py...")

generate_db_thread = threading.Thread(target=run_generate_db())
generate_db_thread.start()
generate_db_thread.join()
def load_cache():
    print("starting to load cache...")
    global graph, actor_name_to_id
    base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "backend", "data", "parsed_data"))

    with open(os.path.join(base_path, "actor_graph_meta.pkl"), "rb") as f:
        graph = pickle.load(f)

    with open(os.path.join(base_path, "actor_name_to_id.pkl"), "rb") as f:
        actor_name_to_id = pickle.load(f)

start_time = time.time()
load_cache()
end_time = time.time()

print("cache loaded in {} seconds".format(end_time - start_time))
@app.route("/", methods=["GET", "POST"])
def main():
    result = None
    if request.method == "POST":
        actor_name = request.form.get("actor_name")
        if actor_name:
            distance = get_bacon_distance(actor_name.strip().title(), graph, actor_name_to_id)


            if isinstance(distance, int):
                if distance == 0:
                    result = "This is Kevin Bacon!"
                elif distance == float("inf"):
                    result = f"No connection was found between Kevin Bacon and {actor_name}"
                else:
                    result = f"Bacon distance for {actor_name} is {distance}"
            else:
                result = "No actor name was provided"

    return render_template("main_page.html", result=result)

if __name__ == "__main__":
    app.run(debug=True)