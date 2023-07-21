from brownie import AdvancedCollectible, network
from scripts.helpful_scripts import get_sky
from metadata.sample_metadata import metadata_template
from pathlib import Path
import requests, json, os

sky_to_image_uri = {
    "CRESCENT": "",
    "NEBULA": "https://ipfs.io/ipfs/QmY9HKSC3zgzL86n2k7AanSHdWxcfRDYeZDuuMeDYbpZiD?filename=0-nebula.jpeg",
    "STARS": "https://ipfs.io/ipfs/Qmb1WiEcZuVjb8gxogxQRDPekcNrquX8SVg9eFGXMbdaX7?filename=1-stars.jpeg",
}


def upload_to_ipfs(filepath, token_id):
    with Path(filepath).open("rb") as fp:
        image_binary = fp.read()
        ipfs_url = "http://127.0.0.1:5001"
        endpoint = "/api/v0/add"
        response = requests.post(ipfs_url + endpoint, files={"file": image_binary})
        ipfs_hash = response.json()["Hash"]
        filename = f"{token_id}-" + filepath.split("/")[-1:][0]
        image_uri = f"https://ipfs.io/ipfs/{ipfs_hash}?filename={filename}"
        print(image_uri)
        return image_uri


def main():
    advanced_collectible = AdvancedCollectible[-1]
    number_of_advanced_collectibles = advanced_collectible.tokenCounter()
    print(f"You have created {number_of_advanced_collectibles} collectibles!")
    for token_id in range(number_of_advanced_collectibles):
        sky = get_sky(advanced_collectible.tokenIDtoSky(token_id))
        # metadata_file_name = f"./metadata/{network.show_active()}/{token_id}-{sky}.json"
        metadata_file_name = f"./metadata/{network.show_active()}/{sky}.json"
        collectible_metadata = metadata_template
        if Path(metadata_file_name).exists():
            print(f"{metadata_file_name} already exists! Delete it to overwrite")
        else:
            print(f"Creating Metadata file: {metadata_file_name}")
            collectible_metadata["name"] = sky
            collectible_metadata["description"] = f"A cool {sky} image"
            image_path = "./img/" + sky.lower() + ".jpeg"

            image_uri = None
            if os.getenv("UPLOAD_IPFS") == "true":
                image_uri = upload_to_ipfs(image_path, token_id)
            image_uri = image_uri if image_uri else sky_to_image_uri[sky]

            collectible_metadata["image"] = image_uri
            with open(metadata_file_name, "w") as file:
                json.dump(collectible_metadata, file)
            if os.getenv("UPLOAD_IPFS") == "true":
                upload_to_ipfs(metadata_file_name, token_id)
