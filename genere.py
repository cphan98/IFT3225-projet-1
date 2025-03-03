#!/usr/bin/env python3

import sys
import os
import argparse

def generate_html(base_path, resources):
    html = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Viewer</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
</head>
<body class="container mt-4">
    <h1 class="text-center">Viewer</h1>
    <p class="text-center text-muted">Images/Videos</p>

    <table class="table table-bordered">
        <thead class="table-light">
            <tr>
                <th>Resource</th>
                <th>Alt</th>
            </tr>
        </thead>
        <tbody>\n"""

    # Add rows with file names and their descriptions
    for resource, alt_text in resources:
        html += f'<tr><td>{resource}</td><td>{alt_text}</td></tr>\n'

    html += """        </tbody>
    </table>

    <div class="text-center mt-3">
        <button class="btn btn-primary me-2" data-bs-toggle="modal" data-bs-target="#carouselModal">Carousel</button>
        <button class="btn btn-primary" data-bs-toggle="modal" data-bs-target="#galleryModal">Gallery</button>
    </div>

    <!-- Carousel Modal -->
    <div class="modal fade" id="carouselModal" tabindex="-1" aria-hidden="true">
        <div class="modal-dialog modal-lg">
            <div class="modal-content">
                <div class="modal-header">
                    <h5 class="modal-title">Carousel</h5>
                    <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                </div>
                <div class="modal-body">
                    <div id="carouselExample" class="carousel slide" data-bs-ride="carousel">
                        <div class="carousel-inner">\n"""

    # Add images to the carousel
    for i, (resource, _) in enumerate(resources):
        full_path = os.path.abspath(os.path.join(base_path, resource)).replace("\\", "/")
        active_class = "active" if i == 0 else ""
        html += f'                            <div class="carousel-item {active_class}">\n'
        html += f'                                <img src="file:///{full_path}" class="d-block w-100">\n'
        html += f'                            </div>\n'

    html += """                        </div>
                        <button class="carousel-control-prev" type="button" data-bs-target="#carouselExample" data-bs-slide="prev">
                            <span class="carousel-control-prev-icon"></span>
                        </button>
                        <button class="carousel-control-next" type="button" data-bs-target="#carouselExample" data-bs-slide="next">
                            <span class="carousel-control-next-icon"></span>
                        </button>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <!-- Gallery Modal -->
    <div class="modal fade" id="galleryModal" tabindex="-1" aria-hidden="true">
        <div class="modal-dialog modal-lg">
            <div class="modal-content">
                <div class="modal-header">
                    <h5 class="modal-title">Gallery</h5>
                    <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                </div>
                <div class="modal-body">
                    <div class="row">\n"""

    # Add images to the gallery
    for resource, _ in resources:
        full_path = os.path.abspath(os.path.join(base_path, resource)).replace("\\", "/")
        html += f'                        <div class="col-md-4 mb-3">\n'
        html += f'                            <img src="file:///{full_path}" class="img-fluid rounded">\n'
        html += f'                        </div>\n'

    html += """                    </div>
                </div>
            </div>
        </div>
    </div>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>"""
    
    return html

def main():
    parser = argparse.ArgumentParser(description="generate html with the resources from a webpage. Authors: Hoang-Thi-Thi Cynthia Phan(20220019) , Laura Cadillo Manrique (20251700) ")
    parser.add_argument("url", type=str, help="URL of the webpage")
    base_path = None
    resources = []

    for line in sys.stdin:
        line = line.strip()
        
        if line.startswith("PATH "):  
            base_path = line.split(" ", 1)[1]
        
        elif line.startswith("IMAGE "):  
            parts = line.split(" ", 2)  
            image_name = parts[1]  
            alt_text = parts[2].strip('"') if len(parts) > 2 else "No description"  
            resources.append((image_name, alt_text))

    if not base_path:
        print("Error: No base path detected.", file=sys.stderr)
        sys.exit(1)

    print(generate_html(base_path, resources))

if __name__ == "__main__":
    main()
