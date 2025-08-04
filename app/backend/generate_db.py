from app.backend.modules.generate_db_modules.download_from_imdb import download_from_imdb
from app.backend.modules.generate_db_modules.data_parser import movie_ids, actor_ids, actor_per_movie
from app.backend.modules.generate_db_modules.dataset_writer import write_dataset
import os
import pickle
import json


dataset_json_path = "data/parsed_data/dataset.json"
dataset_pkl_path = "data/parsed_data/dataset.pkl"

os.makedirs("data/parsed_data", exist_ok = True)

if os.path.exists(dataset_pkl_path):
    print("dataset.pkl already exists. skipping dataset...")

elif os.path.exists(dataset_json_path):
    print("dataset.pkl not found, but dataset.json file exists. skipping generation.")
    with open(dataset_json_path, "r", encoding="utf-8") as f:
        dataset = json.load(f)
    with open(dataset_pkl_path, "wb") as f:
        pickle.dump(dataset, f)
    print("saved pickle dataset")

else:
    print("dataset json file not found. generating dataset...")

    download_from_imdb() #download data from imdb files

    #parse all the data
    movie_ids = movie_ids()
    actor_ids = actor_ids()
    actor_per_movie = actor_per_movie(movie_ids, actor_ids)

    #write the dataset we need to continue
    write_dataset(actor_per_movie)

    #pkl it
    with open(dataset_json_path, "wb") as f:
        pickle.dump(actor_per_movie, f)

    print("dataset generated and saved")

