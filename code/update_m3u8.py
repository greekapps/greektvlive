import re
import requests
import os
import logging

# Define the URL to fetch data from
url = "https://voe.sx/k4uygv3yxqsg"

# Define the path to the m3u8 file in the repo
m3u8_file_path = "files/ads/greektvlive.m3u8"

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def fetch_and_extract_m3u8():
    try:
        # Make the HTTP request to the URL
        response = requests.get(url)
        response.raise_for_status()
        content = response.text

        # Extract the m3u8 URL using regex
        url_match = re.search(r"https?://[^\s]+\.m3u8[^\s]*", content)
        m3u8_url = url_match.group(0) if url_match else None

        if m3u8_url:
            logging.info(f"Extracted m3u8 URL: {m3u8_url}")
            update_m3u8_file(m3u8_url)
        else:
            logging.warning("No m3u8 URL found.")
    except requests.exceptions.RequestException as e:
        logging.error(f"Failed to fetch the URL: {e}")

def update_m3u8_file(m3u8_url):
    try:
        # Ensure the directory exists
        os.makedirs(os.path.dirname(m3u8_file_path), exist_ok=True)
        
        # Write the new m3u8 URL to the file
        with open(m3u8_file_path, 'w') as file:
            file.write(m3u8_url)
        logging.info(f"Updated m3u8 file at {m3u8_file_path}.")
    except IOError as e:
        logging.error(f"Failed to update m3u8 file: {e}")

if __name__ == "__main__":
    fetch_and_extract_m3u8()
