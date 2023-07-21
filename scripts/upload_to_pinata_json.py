import os, requests, json
from pathlib import Path

PINATA_BASE_URL = "https://api.pinata.cloud"
endpoint = "/pinning/pinJSONToIPFS"
filepath = "./metadata/sepolia/NEBULA.json"
filename = "0-" + filepath.split("/")[-1:][0]
# header = {"Authorization": os.getenv("PINATA_JWT")}
header = {
    "Content-Type": "metadata/json",
    "pinata_api_key": os.getenv("PINATA_API_JSON_KEY"),
    "pinata_secret_api_key": os.getenv("PINATA_API_JSON_SECRET"),
}


def main():
    with Path(filepath).open("rb") as fp:
        # image_binary = fp.read()
        image_binary = json.load(fp)
        print(json.dumps(image_binary))
        # print(header)
        response = requests.post(
            PINATA_BASE_URL + endpoint,
            files={"file": (filename, json.dumps(image_binary))},
            headers=header,
        )
        print(response.json())
