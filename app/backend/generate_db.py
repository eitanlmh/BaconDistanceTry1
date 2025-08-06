import os
from app.backend.modules.generate_db_modules.dataset_writer import dataset_writer
from app.backend.modules.generate_db_modules.data_parser import movie_ids as mi
from app.backend.modules.generate_db_modules.data_parser import actor_ids as ai
from app.backend.modules.generate_db_modules.data_parser import actor_per_movie as apm


def generate_db(movie_path_of_data_to_read, actor_path_of_data_to_read, movie_per_actor_path_to_read, path_to_write_data_to):

    if os.path.exists(os.path.join(path_to_write_data_to, "dataset.pkl")):
        print("all wanted data parsed")
    else:
        print("parsed data does not exist, starting to parse")
        # parse all the data
        movie_ids = mi(movie_path_of_data_to_read)
        actor_ids = ai(actor_path_of_data_to_read)
        actor_per_movie = apm(movie_ids, actor_ids, movie_per_actor_path_to_read)
        # write the dataset we need in the right place to continue
        dataset_writer(actor_per_movie, path_to_write_data_to)



movie_example_path_to_read = os.path.join(os.path.abspath(os.path.dirname(__file__)), "data", "example_data", "movie_id_to_title.tsv.gz")
actor_example_path_to_read = os.path.join(os.path.abspath(os.path.dirname(__file__)), "data", "example_data", "actor_id_to_name.tsv.gz")
movie_per_actor_example_path_to_read = os.path.join(os.path.abspath(os.path.dirname(__file__)), "data", "example_data", "actor_per_movie.tsv.gz")
example_path_to_write = os.path.join(os.path.abspath(os.path.dirname(__file__)), "data", "example_parsed_data")
generate_db(movie_example_path_to_read, actor_example_path_to_read, movie_per_actor_example_path_to_read, example_path_to_write)




movie_real_path_to_read = os.path.join(os.path.abspath(os.path.dirname(__file__)), "data", "real_data", "title_basics.tsv.gz")
actor_real_path_to_read = os.path.join(os.path.abspath(os.path.dirname(__file__)), "data", "real_data", "name_basics.tsv.gz")
movie_per_actor_real_path_to_read = os.path.join(os.path.abspath(os.path.dirname(__file__)), "data", "real_data", "title_principals.tsv.gz")
real_path_to_write = os.path.join(os.path.abspath(os.path.dirname(__file__)), "data", "real_parsed_data")


generate_db(movie_real_path_to_read, actor_real_path_to_read, movie_per_actor_real_path_to_read, real_path_to_write)
