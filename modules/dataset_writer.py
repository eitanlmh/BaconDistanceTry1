import csv
import os


data_dir = "data/parsed data"
output = os.path.join(data_dir, "dataset.csv")

def write_dataset(actor_per_movie, max_movies=None):
    """
    write (movie, actor) airs i to a csv file.
    if max_movies is given, only include that many movies.
    """
    os.makedirs(data_dir, exist_ok=True)

    seen_movies = set()
    rows_written = 0

    with open(output, mode='w',encoding="utf-8", newline="") as file:

        writer = csv.writer(file)
        writer.writerow(["movie id", "movie", "actor id", "actor name"])

        for movie_id, movie_name, actor_id, actor_name in actor_per_movie:
            if max_movies is not None and movie_id not in seen_movies:
                if len(seen_movies) >= max_movies:
                    break
                seen_movies.add(movie_id)

            writer.writerow([movie_id, movie_name, actor_id, actor_name])
            rows_written += 1

    print(f"dataset saved to {output} with {rows_written} rows.")