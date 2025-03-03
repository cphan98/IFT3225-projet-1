#!/usr/bin/env python3

import argparse # Command-line parsing library
import os # Operating system library
import re # Regular expressions library
import requests  # HTTP library
from bs4 import BeautifulSoup # HTML parsing library
from urllib.parse import urljoin, urlparse # URL parsing library

# Main function
def main():
    parser = argparse.ArgumentParser(description="Extract resources from a webpage. Authors: Hoang-Thi-Thi Cynthia Phan(20220019) , Laura Cadillo Manrique (20251700)")
    parser.add_argument("url", type=str, help="URL of the webpage")
    parser.add_argument("-r", "--regex", type=str, help="Filter resources matching regex", default=None)
    parser.add_argument("-i", action="store_false", dest="include_images", help="Exclude images")
    parser.add_argument("-v", action="store_true", dest="verbose", help="Include alt text for images")
    parser.add_argument("-p", "--path", type=str, help="Directory to save resources", default=None)
    
    args = parser.parse_args()
    
    if args.path: # A path was provided
        os.makedirs(args.path, exist_ok=True) # Create path
    
    # Extract resouces
    extract_resources(args.url, args.regex, args.include_images, True, args.path, args.verbose)

# Download a file from a URL and save it to a directory
# @param url: URL of the webpage
# @param path: Path to save the files
def download_file(url, path):
    filename = os.path.basename(urlparse(url).path)
    filepath = os.path.join(path, filename) # /path/to/directory/filename
    try:
        response = requests.get(url, stream=True) # Request the file
        response.raise_for_status() # Raises an exception for 4xx and 5xx status codes (client and server errors)
        with open(filepath, 'wb') as file:
            # Read the file in chunks and write it to the file
            for chunk in response.iter_content(1024): # 1024 bytes (1 KB) at a time
                file.write(chunk)
    except requests.RequestException as e:
        print(f"Failed to download: {filename}, Error: {e}")

# Extract imeages and/or videos from a webpage and optionally save them to a directory
# @param url: URL of the webpage
# @param regex: Regular expression to filter resources
# @param include_images: Include images in the extraction
# @param include_videos: Include videos in the extraction
# @param save_path: Path to save the resources
# @param verbose: Include alt text for images
def extract_resources(url, regex=None, include_images=True, include_videos=True, save_path=None, verbose=False):
    # Fetch the webpage
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Error fetching URL: {e}")
        return
    
    soup = BeautifulSoup(response.text, 'html.parser') # Parse the HTML content
    base_url = f"{urlparse(url).scheme}://{urlparse(url).netloc}{urlparse(url).path}" # Base URL
    resources = [] # List of resources
    
    # Extract images
    if include_images:
        for img in soup.find_all('img'):
            src = img.get('src') # Image source in the 'src' attribute
            alt = img.get('alt', '') # Alternative text in the 'alt' attribute
            if src: # If the image source exists
                if not regex or re.search(regex, src):
                    # If regex is not provided, all images are extracted
                    # If regex is provided, only images that match the regex are extracted
                    filename = os.path.basename(urlparse(src).path) # Extract the filename from the URL
                    resources.append(("IMAGE", filename if save_path else src, alt)) # Add the image to the resources list
                    if save_path: # If a path was provided
                        download_file(urljoin(base_url, src), save_path) # Download the image and save it to the path
    
    # Extract videos
    if include_videos:
        for video in soup.find_all('video'):
            src_list = [] # List of video sources

            src = video.get('src') # Video source in the 'src' attribute
            if src: # If the video source exists
                src_list.append(src)

            for source in video.find_all('source'): # Find all 'source' elements
                src = source.get('src') # Video source in the 'src' attribute
                if src: # If the video source exists
                    src_list.append(src)

            for src in src_list:
                full_url = urljoin(base_url, src) # Full URL of the video
                if not regex or re.search(regex, src):
                    # If regex is not provided, all images are extracted
                    # If regex is provided, only images that match the regex are extracted
                    filename = os.path.basename(urlparse(full_url).path) # Extract the filename from the URL
                    resources.append(("VIDEO", filename if save_path else src, '')) # Add the video to the resources list
                    if save_path: # If a path was provided
                        download_file(full_url, save_path) # Download the video and save it to the path
    
    # Print results
    print(f"PATH {save_path if save_path else base_url}")
    for res_type, res_src, res_alt in resources:
        alt_text = f' "{res_alt}"' if res_alt else ''
        print(f"{res_type} {res_src}{alt_text}")

if __name__ == "__main__":
    main()
