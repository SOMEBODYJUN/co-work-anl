"""Download the explicitly adapted test encoder at a fixed revision."""
import argparse
import hashlib
import json
from pathlib import Path
import urllib.request

MODEL = "Xenova/bge-small-zh-v1.5"
REVISION = "75c43b069aac4d136ba6bc1122f995fedcfd2781"
FILES = {
    "tokenizer.json": "48cea5d44424912a6fd1ea647bf4fe50b55ab8b1e5879c3275f80e339e8fae26",
    "config.json": "d4193ead3a810fd694fa8a31d7fc72fbaebc0668b603e398734bf2f6538ff42f",
    "tokenizer_config.json": "e6f3b96db926a37d4039995fbf5ad17de158dfb8f6343d607e4dbaad18d75f5a",
    "onnx/model_quantized.onnx": "15b717c382bcb518ba457b93ea6850ede7f4f1cd8937454aa06972366cd19bcc",
}


def download(destination):
    root = Path(destination)
    for name, expected in FILES.items():
        target = root / name
        target.parent.mkdir(parents=True, exist_ok=True)
        if not target.exists():
            urllib.request.urlretrieve(f"https://huggingface.co/{MODEL}/resolve/{REVISION}/{name}", target)
        if hashlib.sha256(target.read_bytes()).hexdigest() != expected:
            raise ValueError(f"Encoder bytes differ from fixed revision: {name}")
    (root / "download_manifest.json").write_text(json.dumps({"model": MODEL, "revision": REVISION, "files": FILES}, indent=2))


if __name__ == "__main__":
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("destination")
    download(p.parse_args().destination)
