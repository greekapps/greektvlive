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

def save_m3u8_file_with_url(m3u8_url, filename):
    # Save the m3u8 URL as a comment in the m3u8 file
    with open(filename, 'w') as file:
        # Writing the m3u8 URL as a comment at the top of the file
        file.write(f"#EXTM3U\n")
        file.write(f"# M3U8 URL: {m3u8_url}\n")

if __name__ == "__main__":
    site_url = "https://www.alphacyprus.com.cy/live"  # Replace with the actual website URL
    m3u8_file = "channels/alphacyprus.m3u8"

    # Step 1: Get the m3u8 URL from the website
    m3u8_url = get_m3u8_url(site_url)

    if m3u8_url:
        # Step 2: Save the m3u8 URL as an attribute in the m3u8 file
        save_m3u8_file_with_url(m3u8_url, m3u8_file)
        print(f"m3u8 URL saved as attribute in {m3u8_file}")
    else:
        print("Failed to find m3u8 URL.")
