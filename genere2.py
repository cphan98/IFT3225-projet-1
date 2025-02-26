import sys
import argparse

def generate_html(resources):
    html_template = f"""<!DOCTYPE html>
<html lang='fr'>
<head>
    <meta charset='UTF-8'>
    <meta name='viewport' content='width=device-width, initial-scale=1.0'>
    <title>Visualisateur</title>
    <link rel='stylesheet' href='styles.css'>
</head>
<body>
    <h1>Visualisateur</h1>
    <h3>d'images/vidéo</h3>
    <table id='table-view'>
        <tr><th>Ressource</th><th>alt</th></tr>
        {''.join(f'<tr><td><img src="{src}" alt="{alt}"></td><td>{alt}</td></tr>' for src, alt in resources)}
    </table>
    <div class='hidden' id='carousel-view'>
        <button onclick='prevImage()'>⟨</button>
        <img id='carousel-img' src='{resources[0][0]}' alt='{resources[0][1]}' />
        <button onclick='nextImage()'>⟩</button>
        <br><button onclick='showTable()'>Back</button>
    </div>
    <br>
    <button onclick='showCarousel()'>Carrousel</button>
    <button onclick='showGallery()'>Galerie</button>
    <script src='script.js'></script>
</body>
</html>"""
    print(html_template)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate an HTML page to visualize images and videos.")
    parser.add_argument("-h", "--help", action="help", help="Show the synopsis and authors of the command.")
    
    args = parser.parse_args()
    
    resources = []
    for line in sys.stdin:
        parts = line.strip().split(' ', 2)
        if len(parts) >= 2:
            res_type, src = parts[:2]
            alt = parts[2] if len(parts) == 3 else ''
            if res_type == "IMAGE":
                resources.append((src, alt))
    
    generate_html(resources)
