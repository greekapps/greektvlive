import requests
import re

def get_m3u8_url(url):
    # Send an HTTP request to the website
    response = requests.get(url)
    if response.status_code == 200:
        # Use regex to extract the m3u8 URL from the 'hls' key in the var src object
        m3u8_url_match = re.search(r"hls:\s*'(https?://[^\s]+\.m3u8[^\']*)'", response.text)
        if m3u8_url_match:
            return m3u8_url_match.group(1)
    return None

def save_m3u8_file(m3u8_url, filename):
    # Save the m3u8 URL to a file
    with open(filename, 'w') as file:
        file.write(m3u8_url)

if __name__ == "__main__":
    site_url = "https://www.alphacyprus.com.cy/live"  # Replace with the actual website URL
    m3u8_file = "alphacyprus.m3u8"

    m3u8_url = get_m3u8_url(site_url)
    if m3u8_url:
        save_m3u8_file(m3u8_url, m3u8_file)
        print(f"m3u8 URL saved to {m3u8_file}")
    else:
        print("Failed to find m3u8 URL.")
