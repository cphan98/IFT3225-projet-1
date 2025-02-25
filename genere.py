import sys

template = """<!DOCTYPE html>
<html lang='fr'>
<head>
    <meta charset='UTF-8'>
    <meta name='viewport' content='width=device-width, initial-scale=1.0'>
    <title>Visualisateur</title>
    <style>
        body { font-family: Arial, sans-serif; text-align: center; }
        table { width: 80%; margin: auto; border-collapse: collapse; }
        th, td { border: 1px solid black; padding: 8px; }
        button { margin: 10px; padding: 10px; }
    </style>
</head>
<body>
    <h1>Visualisateur</h1>
    <h3>d’images/vidéo</h3>
    <table>
        <tr><th>ressource</th><th>alt</th></tr>
        {rows}
    </table>
    <button onclick="alert('Mode Carrousel activé')">Carrousel</button>
    <button onclick="alert('Mode Galerie activé')">Galerie</button>
</body>
</html>
"""

def main():
    rows = ""
    for line in sys.stdin:
        parts = line.strip().split()
        if len(parts) == 2:
            resource, alt = parts
        else:
            resource, alt = parts[0], ""
        rows += f"<tr><td>{resource}</td><td>{alt}</td></tr>\n"
    
    html_content = template.format(rows=rows)
    with open("mapage.html", "w", encoding="utf-8") as f:
        f.write(html_content)

if __name__ == "__main__":
    main()
