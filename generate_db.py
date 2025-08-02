from modules.download_from_imdb import download_from_imdb
from modules.data_parser import movie_ids, actor_ids, actor_per_movie
from modules.dataset_writer import write_dataset


download_from_imdb() #download data from imdb files

#parse all the data
movie_ids = movie_ids()
actor_ids = actor_ids()
actor_per_movie = actor_per_movie(movie_ids, actor_ids)

#write the dataset we need to continue
write_dataset(actor_per_movie, max_movies=500)

