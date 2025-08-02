import os
import urllib.request

urls = {
    "name_basics": "https://datasets.imdbws.com/name.basics.tsv.gz",
    "title_basics": "https://datasets.imdbws.com/title.basics.tsv.gz",
    "title_principals": "https://datasets.imdbws.com/title.principals.tsv.gz"
}

data_dir = "data"

def download_from_imdb():
    os.makedirs(data_dir, exist_ok=True)
    for name, url in urls.items():
        target_path = os.path.join(data_dir, f"{name}.tsv.gz")
        if os.path.exists(target_path):
            print(f"{name} already exists, skipping")
            continue
        print(f"Downloading {name} from {url}")
        urllib.request.urlretrieve(url, target_path)
        print(f"Extracting {name} to {target_path}")