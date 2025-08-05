import os, sys, requests
from zipfile import ZipFile

def download_file(url, output_dir):
    os.makedirs(output_dir, exist_ok=True)

    response = requests.get(url, stream=True)
    if response.status_code == 200:
        filename = os.path.join(output_dir, 'downloaded.zip')
        with open(filename, "wb") as f:
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:
                    f.write(chunk)
        return filename
    else:
        raise Exception("Failed to download file.")

def extract_zip(zip_path, output_dir):
    with ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(output_dir)
    os.remove(zip_path)

def fix_json(input_path):
    import json
    with open(input_path, 'r') as f:
        data = json.load(f)

    output_path = input_path.replace('.json', '_fixed.json')
    with open(output_path, 'w') as f:
        for key, value in data.items():
            f.write(json.dumps({key: value}) + '\n')

    os.remove(input_path)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Please provide the output directory.")
        sys.exit(1)

    EXTRACT_PATH = sys.argv[1]
    KAGGLE_URL = "https://storage.googleapis.com/kaggle-data-sets/1993933/3294812/bundle/archive.zip?X-Goog-Algorithm=GOOG4-RSA-SHA256&X-Goog-Credential=gcp-kaggle-com%40kaggle-161607.iam.gserviceaccount.com%2F20250728%2Fauto%2Fstorage%2Fgoog4_request&X-Goog-Date=20250728T023007Z&X-Goog-Expires=259200&X-Goog-SignedHeaders=host&X-Goog-Signature=6c72193c172a9adebbe47911fec60df6f07a83255380f019ec8655020e5c47c9e9921b0ec5d8182b86e44e78518b134f3433e14dcce0b4df683ccf368fddf7457d906a11268cbc0d460c88dc04d92989d28563743ee558d2847097adc7c64fe7a6458c350576beebcb45a25c930d96c54d975cfb49f9df62ee3b850fe11e7f6406168bbda47dd5e2e728ad8d1f29f3720cdb7a62ceb8f6cf278a3d2334e6e79337d711af6c0cd5b39541a403834368aeaf66fc68f9dc152099e942c7e34fa8d5518646909e56ebfde865a8ea84d855555649e0c37e9d008a6e553b824ae89ddacf019579272f0362de42317992c4efa0d48d134291c96ee620dcf0b05ce6a3eb"  

    try:
        zip_path = download_file(KAGGLE_URL, EXTRACT_PATH)
        extract_zip(zip_path, EXTRACT_PATH)
        fix_json(os.path.join(EXTRACT_PATH, "dict_artists.json"))  
    except Exception as e:
        print("Error:", e)
