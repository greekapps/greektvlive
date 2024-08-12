import re
import requests
from bs4 import BeautifulSoup
import os
import logging

# Define the initial URL
initial_url = "https://voe.sx/k4uygv3yxqsg"

# Define the path to the m3u8 file in the repo
m3u8_file_path = "files/ads/greektvlive.m3u8"

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def fetch_and_extract_m3u8():
    try:
        # Make the initial HTTP request to the URL
        response = requests.get(initial_url)
        response.raise_for_status()
        content = response.text

        # Check if the content contains JavaScript redirection
        if "<script>" in content and "window.location.href" in content:
            logging.info("JavaScript redirection detected.")
            
            # Extract the redirection URL from the script
            soup = BeautifulSoup(content, 'html.parser')
            script_tags = soup.find_all('script')
            redirection_url = None
            for script in script_tags:
                if 'window.location.href' in script.text:
                    # Find the URL from the script
                    url_match = re.search(r"window\.location\.href\s*=\s*['\"](https?://[^\s'\"]+)", script.text)
                    if url_match:
                        redirection_url = url_match.group(1)
                        break

            if redirection_url:
                logging.info(f"Redirecting to: {redirection_url}")
                # Follow the redirect
                fetch_and_extract_m3u8_from_redirect(redirection_url)
            else:
                logging.warning("No redirection URL found in the script.")
        else:
            logging.warning("No JavaScript redirection detected.")
            # Handle case where there is no JavaScript redirection
            handle_no_redirection(content)

    except requests.exceptions.RequestException as e:
        logging.error(f"Failed to fetch the URL: {e}")

def fetch_and_extract_m3u8_from_redirect(url):
    try:
        # Make the HTTP request to the redirected URL
        response = requests.get(url)
        response.raise_for_status()
        content = response.text

        # Extract the m3u8 URL using regex
        url_match = re.search(r"https?://[^\s]+\.m3u8[^\s]*", content)
        m3u8_url = url_match.group(0) if url_match else None

        if m3u8_url:
            # Clean up the URL if necessary (remove unwanted characters like '");')
            m3u8_url = re.sub(r'[");\s]+$', '', m3u8_url)
            logging.info(f"Extracted m3u8 URL: {m3u8_url}")
            update_m3u8_file(m3u8_url)
        else:
            logging.warning("No m3u8 URL found.")
    except requests.exceptions.RequestException as e:
        logging.error(f"Failed to fetch the redirected URL: {e}")

def handle_no_redirection(content):
    # You can add additional logic here if needed when no redirection occurs
    logging.info("Handling case where no redirection is present.")
    # Extract the m3u8 URL directly if it's in the initial content
    url_match = re.search(r"https?://[^\s]+\.m3u8[^\s]*", content)
    m3u8_url = url_match.group(0) if url_match else None

    if m3u8_url:
        # Clean up the URL if necessary
        m3u8_url = re.sub(r'[");\s]+$', '', m3u8_url)
        logging.info(f"Extracted m3u8 URL: {m3u8_url}")
        update_m3u8_file(m3u8_url)
    else:
        logging.warning("No m3u8 URL found.")

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
