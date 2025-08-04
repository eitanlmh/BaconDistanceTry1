import gzip
import csv
import os
from tqdm import tqdm


data_dir = "data/downloaded_data" # This is where our data is.
chunk_size = 100000

def movie_ids(): # return a dict of movie id with movie name

    print("files in data", os.listdir(data_dir)) #Listing directory files

    movie_file = os.path.join(data_dir, "title_basics.tsv.gz")
    movie_id = {}

    try:
        with gzip.open(movie_file, "rt", encoding="utf-8") as file:
            reader = csv.DictReader(file, delimiter="\t")
            print("reading movie IDs from {}".format(movie_file))
            for row in tqdm(reader, desc="Processing movie IDs", unit="rows"):

                if row.get("titleType") != "movie":
                    continue
                if row.get("primaryTitle") == "\\N":
                    continue

                movie_id[row["tconst"]] = row["primaryTitle"]

        print("read {} movie IDs from {}".format(len(movie_id), movie_file))
    except Exception as e:
        print(f"failed to read movies data: {e}")

    return movie_id

def actor_ids(): # return a dict of actor id with actor name
    print("files in data", os.listdir(data_dir)) #Listing directory files

    actor_file = os.path.join(data_dir, "name_basics.tsv.gz")
    actor_id = {}

    try:
        with gzip.open(actor_file, mode="rt", encoding="utf-8") as file:
            reader = csv.DictReader(file, delimiter="\t")
            print("reading actor IDs from {}".format(actor_file))

            for row in tqdm(reader, desc="Processing actor IDs", unit="rows"):
                actor_id[row["nconst"]] = row["primaryName"]

        print("read {} actors IDs from {}".format(len(actor_id), actor_file))
    except Exception as e:
        print(f"failed to read actor data: {e}")

    return actor_id

def actor_per_movie(movie_ids, actor_ids):
    print("files in data", os.listdir(data_dir)) #Listing directory files

    actor_per_movie_file = os.path.join(data_dir, "title_principals.tsv.gz")
    actor_per_movie = []

    try:
        with gzip.open(actor_per_movie_file, "rt", encoding="utf-8") as file:
            reader = csv.DictReader(file, delimiter="\t")
            print("reading actor per movie IDs from {}".format(actor_per_movie_file))
            for row in tqdm(reader, desc="Processing actor/movie pairs ", unit="rows"):

                movie_id = row["tconst"]
                actor_id = row["nconst"]
                category = row["category"]

                if category not in ("actor", "actress"):
                    continue
                if movie_id not in movie_ids or actor_id not in actor_ids:
                    continue

                movie_name = movie_ids[movie_id]
                actor_name = actor_ids[actor_id]

                actor_per_movie.append((movie_id, movie_name, actor_id, actor_name))
        print("read {} movies and its actors from {}".format(len(actor_per_movie), actor_per_movie_file))
    except Exception as e:
        print(f"failed to read movies and its actors data: {e}")

    return actor_per_movie


