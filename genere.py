import sys
import argparse

def generate_html(resources):
    html = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Viewer</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
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
        <tbody>
"""

    # Add rows with file names and their descriptions
    for resource, alt_text, res_type in resources:
        if res_type == "IMAGE":
            html += f'<tr  class="clickable" data-src="{resource}" data-type="{res_type}"><td>{resource}</td><td>{alt_text}</td></tr>\n'
        elif res_type == "VIDEO":
            html += f'<tr class="clickable" data-src="{resource}" data-type="{res_type}"><td>{resource}</td><td>{alt_text}</td></tr>\n'

    html += """        </tbody>
    </table>

    <div id="popup" class="popup">
        <span id="popup-content"></span>
    </div>

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
                        <div class="carousel-inner">
"""

    # Add media to the carousel
    for i, (resource, _, res_type) in enumerate(resources):
        active_class = "active" if i == 0 else ""
        if res_type == "IMAGE":
            html += f'                            <div class="carousel-item {active_class}">\n'
            html += f'                                <img src="{resource}" class="d-block w-100">\n'
            html += f'                            </div>\n'
        elif res_type == "VIDEO":
            html += f'                            <div class="carousel-item {active_class}">\n'
            html += f'                                <video controls class="d-block w-100"><source src="{resource}" type="video/mp4"></video>\n'
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
                    <div class="row">
"""

    # Add media to the gallery
    for resource, _, res_type in resources:
        html += f'                        <div class="col-md-4 mb-3">\n'
        if res_type == "IMAGE":
            html += f'                            <img src="{resource}" class="img-fluid rounded">\n'
        elif res_type == "VIDEO":
            html += f'                            <video controls class="img-fluid"><source src="{resource}" type="video/mp4"></video>\n'
        html += f'                        </div>\n'

    html += """                    </div>
                </div>
            </div>
        </div>
    </div>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
    <script src="script.js"></script>
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
        
        elif line.startswith("IMAGE ") or line.startswith("VIDEO "):
            parts = line.split(" ", 2)
            media_type = parts[0]
            media_name = parts[1]
            alt_text = parts[2].strip('"') if len(parts) > 2 else "No description"
            resources.append((media_name, alt_text, media_type))

    if not base_path:
        print("Error: No base path detected.", file=sys.stderr)
        sys.exit(1)

    print(generate_html(resources))

if __name__ == "__main__":
    main()
