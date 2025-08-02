import gzip
import csv
import os



data_dir = "data" # This is where our data is.

def movie_ids(): # return a dict of movie id with movie name

    print("files in data", os.listdir(data_dir)) #Listing directory files

    movie_file = os.path.join(data_dir, "title_basics.tsv.gz")

    print("reading movie IDs from {}".format(movie_file))

    movie_ids = {}
    try:
        with gzip.open(movie_file, "rt", encoding="utf-8") as fin:
            reader = csv.DictReader(fin, delimiter="\t")
            for row in reader:
                if row.get("titleType") != "movie":
                    continue
                if row.get("primaryTitle") == "\\N":
                    continue
                movie_ids[row["tconst"]] = row["primaryTitle"]
        print("read {} movie IDs from {}".format(len(movie_ids), movie_file))
    except Exception as e:
        print(f"failed to read movies data: {e}")

    return movie_ids

def actor_ids(): # return a dict of actor id with actor name
    print("files in data", os.listdir(data_dir)) #Listing directory files

    actor_file = os.path.join(data_dir, "name_basics.tsv.gz")

    print("reading actor IDs from {}".format(actor_file))

    actor_ids = {}
    try:
        with gzip.open(actor_file, "rt", encoding="utf-8") as fin:
            reader = csv.DictReader(fin, delimiter="\t")
            for row in reader:
                actor_ids[row["nconst"]] = row["primaryName"]
        print("read {} actors IDs from {}".format(len(actor_ids), actor_file))
    except Exception as e:
        print(f"failed to read actor data: {e}")

    return actor_ids

def actor_per_movie(movie_ids, actor_ids):
    print("files in data", os.listdir(data_dir)) #Listing directory files
    #
    # movie_id_per_moviename = movie_ids()
    # actor_id_per_actorname = actor_ids()

    actor_per_movie_file = os.path.join(data_dir, "title_principals.tsv.gz")
    print("reading actor per movie IDs from {}".format(actor_per_movie_file))

    actor_per_movie = []
    try:
        with gzip.open(actor_per_movie_file, "rt", encoding="utf-8") as fin:
            reader = csv.DictReader(fin, delimiter="\t")
            for row in reader:
                # movie_id = movie_id_per_moviename[row["tconst"]]
                # print(movie_id)
                # actor_id = actor_id_per_actorname[row["nconst"]]
                #
                movie_id = row["tconst"]
                actor_id = row["nconst"]
                category = row["category"]

                if category not in ("actor", "actress"):
                    continue
                if movie_id not in movie_ids or actor_id not in actor_ids:
                    continue


                # if row.get("category") != ("actor" or "actress") :
                #     continue
                # if row.get("tconst") != movie_id or row.get("nconst") != actor_id:
                #     continue
                movie = movie_ids[movie_id]
                actor = actor_ids[actor_id]
                actor_per_movie.append((movie, actor))
        print("read {} movie and its actors from {}".format(len(actor_per_movie), actor_per_movie_file))
    except Exception as e:
        print(f"failed to read movies and its actors data: {e}")

    return actor_per_movie

# if __name__ == "__main__":
#
#     #movie_ids()
#     #actor_ids()
#     actor_per_movie(movie_ids(), actor_ids())

