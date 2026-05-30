import base64
import lzma
from pathlib import Path

encoded = ""

files = sorted(
    Path(".").glob("chunk_*.txt")
)

if not files:
    raise Exception(
        "No chunk files found."
    )

for file in files:

    text = file.read_text(
        encoding="utf-8"
    )

    text = (
        text.replace("\n", "")
            .replace("\r", "")
            .replace(" ", "")
            .strip()
    )

    encoded += text

print(
    f"Recovered chars : {len(encoded):,}"
)

compressed = base64.b32decode(encoded)

data = lzma.decompress(compressed)

with open("recovered.zip", "wb") as f:
    f.write(data)

print("Recovered successfully -> recovered.zip")