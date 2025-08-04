import json
from flask import Flask, make_response, render_template, session, redirect, request
import threading
import subprocess
import os
from app.backend.run_bacon_distance import get_bacon_distance
app = Flask(__name__)

def run_generate_db():
    backend_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "backend"))
    dataset_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data", "parsed_data", "dataset.json"))
    pickled_dataset_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data", "parsed_data", "cached_dataset.pkl"))

    if not os.path.exists(dataset_path) or not os.path.exists(pickled_dataset_path):
        print("Dataset or cached dataset not found. running generate_db.py...")
        subprocess.run(["python", "generate_db.py"], cwd = backend_path)
    else:
        print("dataset and cached dataset found. skipping generate_db.py...")

generate_db_thread = threading.Thread(target=run_generate_db())
generate_db_thread.start()

# def run_loading_cache():
#     backend_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "backend"))
#     subprocess.run(["python, generate_db.py"], cwd = backend_path)
#
# loading_cache_thread = threading.Thread(target=run_loading_cache())
# loading_cache_thread.start()
@app.route("/", methods=["GET", "POST"])
def main():
    result = None
    if request.method == "POST":
        actor_name = request.form.get("actor_name")
        if actor_name:
            distance = get_bacon_distance(actor_name.strip().title())

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