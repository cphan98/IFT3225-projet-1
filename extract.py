#!/usr/bin/env python3

import argparse # Pour traiter les arguments de la ligne de commande
import os # Pour manipuler les fichiers et répertoires
import re # Pour les expressions régulières
import requests # Pour télécharger les ressources
from bs4 import BeautifulSoup # Pour analyser le HTML
from urllib.parse import urljoin, urlparse # Pour manipuler les URLs

def download_file(url, path):
    filename = os.path.basename(urlparse(url).path)
    filepath = os.path.join(path, filename)
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()
        with open(filepath, 'wb') as file:
            for chunk in response.iter_content(1024):
                file.write(chunk)
        print(f"Downloaded: {filename}")
    except requests.RequestException:
        print(f"Failed to download: {filename}")

def extract_resources(url, regex=None, include_images=True, include_videos=True, save_path=None, verbose=False):
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Error fetching URL: {e}")
        return
    
    soup = BeautifulSoup(response.text, 'html.parser')
    base_url = f"{urlparse(url).scheme}://{urlparse(url).netloc}"
    resources = []
    
    if include_images:
        for img in soup.find_all('img'):
            src = img.get('src')
            alt = img.get('alt', '')
            if src:
                full_url = urljoin(base_url, src)
                if not regex or re.search(regex, src):
                    resources.append(("IMAGE", full_url, alt))
                    if save_path:
                        download_file(full_url, save_path)
    
    if include_videos:
        for video in soup.find_all('video'):
            src = video.get('src')
            if not src:
                source = video.find('source')
                if source:
                    src = source.get('src')
            if src:
                full_url = urljoin(base_url, src)
                if not regex or re.search(regex, src):
                    resources.append(("VIDEO", full_url, ''))
                    if save_path:
                        download_file(full_url, save_path)
    
    # Print results
    print(f"PATH {save_path if save_path else url}")
    for res_type, res_url, res_alt in resources:
        alt_text = f' "{res_alt}"' if res_alt and verbose else ''
        print(f"{res_type} {res_url}{alt_text}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Extract resources from a webpage.")
    parser.add_argument("url", type=str, help="URL of the webpage")
    parser.add_argument("-r", "--regex", type=str, help="Filter resources matching regex", default=None)
    parser.add_argument("-i", action="store_false", dest="include_images", help="Exclude images")
    parser.add_argument("-v", action="store_true", dest="verbose", help="Include alt text for images")
    parser.add_argument("-p", "--path", type=str, help="Directory to save resources", default=None)
    # parser.add_argument("-h", "--help", action="help", help="Show this help message and exit")
    
    args = parser.parse_args()
    
    if args.path:
        os.makedirs(args.path, exist_ok=True)
    
    extract_resources(args.url, args.regex, args.include_images, True, args.path, args.verbose)
