import os
import lzma
import base64
import hashlib
from pathlib import Path

# ============================================================
# CONFIG
# ============================================================

INPUT_FILE = "System_Design_Complete_Guide.zip"

OUTPUT_DIR = "encoded_pages"

# Increase/decrease depending on how much fits on screen
CHUNK_SIZE = 12000

# ============================================================
# CREATE OUTPUT DIRECTORY
# ============================================================

Path(OUTPUT_DIR).mkdir(exist_ok=True)

# ============================================================
# READ FILE
# ============================================================

with open(INPUT_FILE, "rb") as f:
    data = f.read()

print(f"Original size     : {len(data):,} bytes")

# ============================================================
# MAXIMUM COMPRESSION
# ============================================================

compressed = lzma.compress(
    data,
    preset=9 | lzma.PRESET_EXTREME
)

print(f"Compressed size   : {len(compressed):,} bytes")

# ============================================================
# OCR FRIENDLY ENCODING
# ============================================================

encoded = base64.b32encode(compressed).decode("ascii")

print(f"Encoded length    : {len(encoded):,} chars")

# ============================================================
# SPLIT INTO CHUNKS
# ============================================================

chunks = [
    encoded[i:i + CHUNK_SIZE]
    for i in range(0, len(encoded), CHUNK_SIZE)
]

print(f"HTML pages        : {len(chunks)}")

# ============================================================
# GENERATE HTML PAGES
# ============================================================

for idx, chunk in enumerate(chunks, start=1):

    checksum = hashlib.sha256(
        chunk.encode("ascii")
    ).hexdigest()

    html = f"""
<!DOCTYPE html>
<html>

<head>

<meta charset="utf-8">

<title>Chunk {idx}</title>

<style>

html,
body {{
    width:100%;
    height:100%;
    margin:0;
    padding:0;
    overflow:hidden;
    background:white;
}}

#header {{
    position:fixed;
    top:0;
    left:0;
    right:0;

    background:white;

    font-family:Arial,sans-serif;

    font-size:12px;

    padding:2px;

    border-bottom:1px solid #ddd;

    z-index:1000;
}}

#data {{

    position:absolute;

    top:20px;
    left:0;
    right:0;
    bottom:0;

    width:100%;
    height:calc(100% - 20px);

    border:none;
    outline:none;

    resize:none;

    padding:2px;

    box-sizing:border-box;

    font-family:Consolas,monospace;

    font-size:10px;

    line-height:0.95;

    white-space:pre-wrap;

    word-break:break-all;

    overflow-wrap:anywhere;
}}

</style>

</head>

<body>

<div id="header">
Chunk {idx}/{len(chunks)}
&nbsp;&nbsp;|&nbsp;&nbsp;
SHA256: {checksum}
</div>

<textarea id="data" readonly>{chunk}</textarea>

</body>

</html>
"""

    output_file = os.path.join(
        OUTPUT_DIR,
        f"chunk_{idx:03d}.html"
    )

    with open(
        output_file,
        "w",
        encoding="utf-8"
    ) as f:
        f.write(html)

print()
print("Done.")
print(f"Generated HTML pages in: {OUTPUT_DIR}")
print()
print("Photo Tips:")
print("1. Open HTML")
print("2. Press F11")
print("3. Set browser zoom to 50%")
print("4. Take photo")