import gzip

from app.backend.modules.generate_db_modules.download_from_imdb import download_from_imdb
# from app.backend.modules.generate_db_modules.data_parser import movie_ids, actor_ids, actor_per_movie
from app.backend.modules.generate_db_modules.data_parser import actor_per_movie as apm
from app.backend.modules.generate_db_modules.data_parser import movie_ids as mi
from app.backend.modules.generate_db_modules.data_parser import actor_ids as ai
from app.backend.modules.generate_db_modules.dataset_writer import dataset_writer
import os
import csv

data_dir = None
output_graph_pkl = None
output_actor_name_to_id_pkl = None
output_actor_name_to_movie_ids_pkl = None


def generate_db(data_source):
    global output_graph_pkl, output_actor_name_to_id_pkl, output_actor_name_to_movie_ids_pkl, data_dir

    if data_source == "example":


        data_dir = os.path.join(os.path.dirname(__file__), "data", "example_data")
        example_actor_id_to_name_path = os.path.join(data_dir, "actor_id_to_name.csv")
        example_movie_id_to_title_path = os.path.join(data_dir, "movie_id_to_title.csv")
        example_actor_per_movie_path = os.path.join(data_dir, "actor_per_movie.tsv.gz")
        example_parsed_data_dir = os.path.join(os.path.dirname(__file__), "data", "example_parsed_data")

        output_graph_pkl = os.path.join(example_parsed_data_dir, "actor_graph_meta.pkl")
        output_actor_name_to_id_pkl = os.path.join(example_parsed_data_dir, "actor_name_to_id.pkl")
        output_actor_name_to_movie_ids_pkl = os.path.join(example_parsed_data_dir, "actor_name_to_movie_ids.pkl")


        example_actor_id_to_name = {}
        example_movie_id_to_title = {}

        with open(example_actor_id_to_name_path, "rt", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                example_actor_id_to_name[row["nconst"]] = row["primaryName"]

        with open(example_movie_id_to_title_path, "rt", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                example_movie_id_to_title[row["tconst"]] = row["primaryTitle"]

        dapm = apm(example_movie_id_to_title, example_actor_id_to_name, example_actor_per_movie_path)

        dataset_writer(dapm, data_source)

    if data_source == "real":
        os.makedirs("data/parsed_data", exist_ok=True)

        data_dir = os.path.join(os.path.dirname(__file__), "..", "data", "parsed_data")

        output_graph_pkl = os.path.join(data_dir, "actor_graph_meta.pkl")
        output_actor_name_to_id_pkl = os.path.join(data_dir, "actor_name_to_id.pkl")
        output_actor_name_to_movie_ids_pkl = os.path.join(data_dir, "actor_name_to_movie_ids.pkl")


        if os.path.exists(output_graph_pkl) and os.path.exists(output_actor_name_to_id_pkl) and os.path.exists(
                output_actor_name_to_movie_ids_pkl):
            print("pkls already exists. skipping building pickles...")

        else:
            print("pkl files not found. generating pickles...")
            data_dir = "data/downloaded_data"  # This is where our data is.

            download_from_imdb()  # download data from imdb files
            actor_per_movie_path = os.path.join(data_dir, "title_principals.tsv.gz")
            # parse all the data
            movie_ids = mi()
            actor_ids = ai()
            actor_per_movie = apm(movie_ids, actor_ids, actor_per_movie_path)

            # write the dataset we need to continue, if needed it can recieve 'max_movie'
            dataset_writer(actor_per_movie, data_source)

            print("pickles generated and saved")
