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

def download_m3u8_content(m3u8_url):
    # Send an HTTP request to the m3u8 URL and get its content
    response = requests.get(m3u8_url)
    if response.status_code == 200:
        return response.text
    return None

def save_m3u8_file(content, filename):
    # Save the m3u8 content to a file
    with open(filename, 'w') as file:
        file.write(content)

if __name__ == "__main__":
    site_url = "https://www.alphacyprus.com.cy/live"  # Replace with the actual website URL
    m3u8_file = "channels/alphacyprus.m3u8"

    # Step 1: Get the m3u8 URL from the website
    m3u8_url = get_m3u8_url(site_url)

    if m3u8_url:
        # Step 2: Download the actual m3u8 content from the extracted URL
        m3u8_content = download_m3u8_content(m3u8_url)
        
        if m3u8_content:
            # Step 3: Save the content to an m3u8 file
            save_m3u8_file(m3u8_content, m3u8_file)
            print(f"m3u8 content saved to {m3u8_file}")
        else:
            print("Failed to download m3u8 content.")
    else:
        print("Failed to find m3u8 URL.")
