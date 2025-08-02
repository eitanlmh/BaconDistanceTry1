import csv
import os

output = "dataset.csv"

def write_dataset(actor_per_movie, max_movies=None):
    """
    write (movie, actor) airs i to a csv file.
    if max_movies is given, only include that many movies.
    """

    seen_movies = set()
    rows_written = 0

    with open(output, 'w',encoding="utf-8", newline="") as fin:

        writer = csv.writer(fin)
        writer.writerow(["movie", "actor"])
        for movie, actor in actor_per_movie:
            if max_movies is not None and movie not in seen_movies:
                if len(seen_movies) < max_movies:
                    continue
                seen_movies.add(movie)

            writer.writerow([movie, actor])
            rows_written += 1

    print(f"dataset daved to {output} with {rows_written} rows.")