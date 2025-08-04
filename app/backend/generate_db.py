from app.backend.modules.generate_db_modules.download_from_imdb import download_from_imdb
from app.backend.modules.generate_db_modules.data_parser import movie_ids, actor_ids, actor_per_movie
from app.backend.modules.generate_db_modules.dataset_writer import write_dataset
import os

data_dir = "data/parsed_data"

output_graph_pkl = os.path.join(data_dir, "actor_graph_meta.pkl")
output_actor_name_to_id_pkl = os.path.join(data_dir, "actor_name_to_id.pkl")
output_actor_name_to_movie_ids_pkl = os.path.join(data_dir, "actor_name_to_movie_ids.pkl")

os.makedirs("data/parsed_data", exist_ok = True)


if os.path.exists(output_graph_pkl) and os.path.exists(output_actor_name_to_id_pkl) and os.path.exists(output_actor_name_to_movie_ids_pkl):
    print("pkls already exists. skipping building pickles...")

else:
    print("pkl files not found. generating pickles...")

    download_from_imdb() #download data from imdb files

    #parse all the data
    movie_ids = movie_ids()
    actor_ids = actor_ids()
    actor_per_movie = actor_per_movie(movie_ids, actor_ids)

    #write the dataset we need to continue, if needed it can recieve 'max_movie'
    write_dataset(actor_per_movie)

    print("pickles generated and saved")

