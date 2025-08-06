import gzip
import csv
from tqdm import tqdm

data_dir = "data" # This is where our data is.
downloaded_data_dir = "real_data"
example_data_dir = "example_data"
def movie_ids(movie_path): # return a dict of movie id with movie name

    movie_ids = {}

    try:
        with gzip.open(movie_path, "rt", encoding="utf-8") as file:
            reader = csv.DictReader(file, delimiter="\t")
            print("reading movie IDs from {}".format(movie_path))
            for row in tqdm(reader, desc="Processing movie IDs", unit="rows"):

                if row.get("titleType") != "movie":
                    continue
                if row.get("primaryTitle") == "\\N":
                    continue

                movie_ids[row["tconst"]] = row["primaryTitle"]

        print("read {} movie IDs from {}".format(len(movie_ids), movie_path))
    except Exception as e:
        print(f"failed to read movies data: {e}")

    return movie_ids

def actor_ids(actor_path): # return a dict of actor id with actor name

    actor_ids = {}

    try:
        with gzip.open(actor_path, mode="rt", encoding="utf-8") as file:
            reader = csv.DictReader(file, delimiter="\t")
            print("reading actor IDs from {}".format(actor_path))

            for row in tqdm(reader, desc="Processing actor IDs", unit="rows"):
                actor_ids[row["nconst"]] = row["primaryName"]

        print("read {} actors IDs from {}".format(len(actor_ids), actor_path))
    except Exception as e:
        print(f"failed to read actor data: {e}")

    return actor_ids

def actor_per_movie(movie_ids, actor_ids, movie_per_actors_path):

    actor_per_movie = []

    try:
        with gzip.open(movie_per_actors_path, "rt", encoding="utf-8") as file:
            reader = csv.DictReader(file, delimiter="\t")
            print("reading actor per movie IDs from {}".format(movie_per_actors_path))
            for row in tqdm(reader, desc="Processing actor/movie pairs", unit="rows"):

                movie_id = row["tconst"]
                actor_id = row["nconst"]
                category = row["category"]

                if category not in ("actor", "actress"):
                    continue
                if movie_id not in movie_ids or actor_id not in actor_ids:
                    continue

                actor_name = actor_ids[actor_id]

                actor_per_movie.append((movie_id, actor_id, actor_name))
        print("read {} movies and its actors from {}".format(len(actor_per_movie), movie_per_actors_path))
    except Exception as e:
        print(f"failed to read movies and its actors data: {e}")

    return actor_per_movie

# if __name__ == "__main__":
#
#     #movie_ids()
#     #actor_ids()
#     actor_per_movie(movie_ids(), actor_ids())

