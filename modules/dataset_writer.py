import os
import json

data_dir = "data/parsed data"
output = os.path.join(data_dir, "dataset.json")

def write_dataset(actor_per_movie, max_movies=None):
    """
    write (movie, actor) airs i to a csv file.
    if max_movies is given, only include that many movies.
    """
    os.makedirs(data_dir, exist_ok=True)

    seen_movies = set()
    dataset = []

    for movie_id, movie_name, actor_id, actor_name in actor_per_movie:
        if max_movies is not None and movie_id not in seen_movies:
            if len(seen_movies) >= max_movies:
                break
            seen_movies.add(movie_id)

        dataset.append({
            "movie_id": movie_id,
            "movie_name": movie_name,
            "actor_id": actor_id,
            "actor_name": actor_name
        })
    try:
        with open(output, mode='w',encoding="utf-8") as file:
            json.dump(dataset, file, ensure_ascii=False, indent=2)
    except IOError as e:
        print(f"error writing to file {output}: {e}")
        return




    print(f"dataset saved to {output} with {len(dataset)} rows.")