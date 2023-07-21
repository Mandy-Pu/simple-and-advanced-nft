import os, requests
from pathlib import Path

PINATA_BASE_URL = "https://api.pinata.cloud"
endpoint = "/pinning/pinFileToIPFS"
filepath = "./img/nebula.jpeg"
filename = "0-" + filepath.split("/")[-1:][0]
# header = {"Authorization": os.getenv("PINATA_JWT")}
header = {
    "pinata_api_key": os.getenv("PINATA_API_KEY"),
    "pinata_secret_api_key": os.getenv("PINATA_API_SECRET"),
}


def main():
    with Path(filepath).open("rb") as fp:
        image_binary = fp.read()
        # print(header)
        response = requests.post(
            PINATA_BASE_URL + endpoint,
            files={"file": (filename, image_binary)},
            headers=header,
        )
        print(response.json())
