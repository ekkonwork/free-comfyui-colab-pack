#!/usr/bin/env python3
"""Apply proven shared Colab runtime/dependency fixes without touching model presets."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

SWAP_OLD = """    !sudo swapon /swapfile
    print("Swap enabled.")"""
SWAP_NEW = """    _swap_rc = !sudo swapon /swapfile
    if any("failed" in line.lower() for line in _swap_rc):
        print("Swap unavailable on this Colab VM; continuing without swap.")
    else:
        print("Swap enabled.")"""
SWAP_FINAL = """    _swap_result = subprocess.run(
        ["sudo", "swapon", "/swapfile"], capture_output=True, text=True
    )
    if _swap_result.returncode != 0:
        print("Swap unavailable on this Colab VM; continuing without swap.")
    else:
        print("Swap enabled.")"""

DOWNLOAD_OLD = """    if os.path.exists(outpath):
        print('Already exists:', outpath)
        return
    print('Downloading:', fname)
"""
DOWNLOAD_NEW = """    marker = outpath + '.aria2'
    ready = os.path.exists(outpath) and os.path.getsize(outpath) > 0 and not os.path.exists(marker)
    if ready and outpath.lower().endswith('.gguf'):
        with open(outpath, 'rb') as stream:
            ready = stream.read(4) == b'GGUF'
    if ready:
        print('Already exists and validated:', outpath)
        return
    if os.path.exists(outpath) and not os.path.exists(marker):
        print('Removing invalid completed file:', outpath)
        os.remove(outpath)
    print('Downloading/resuming:', fname)
"""


def patch_source(source: str) -> tuple[str, set[str]]:
    changes: set[str] = set()

    if SWAP_OLD in source:
        source = source.replace(SWAP_OLD, SWAP_FINAL)
        changes.add("swap-status")
    if SWAP_NEW in source:
        source = source.replace(SWAP_NEW, SWAP_FINAL)
        changes.add("swap-status")

    if "NODES = {" in source:
        anchor = '    "ComfyUI-GGUF": "https://github.com/city96/ComfyUI-GGUF.git",\n'
        additions = ""
        if "ComfyUI-Impact-Pack" not in source:
            additions += '    "ComfyUI-Impact-Pack": "https://github.com/ltdrdata/ComfyUI-Impact-Pack.git",\n'
            changes.add("impact-pack")
        if "ComfyUI-Impact-Subpack" not in source:
            additions += '    "ComfyUI-Impact-Subpack": "https://github.com/ltdrdata/ComfyUI-Impact-Subpack.git",\n'
            changes.add("impact-subpack")
        if "ComfyUI-SeedVR2_VideoUpscaler.git" not in source:
            additions += '    "seedvr2_videoupscaler": "https://github.com/numz/ComfyUI-SeedVR2_VideoUpscaler.git",\n'
            changes.add("seedvr2-node")
        if additions:
            if anchor not in source:
                raise RuntimeError("NODES cell has no ComfyUI-GGUF anchor")
            source = source.replace(anchor, anchor + additions, 1)

    if DOWNLOAD_OLD in source:
        source = source.replace(DOWNLOAD_OLD, DOWNLOAD_NEW)
        changes.add("download-validation")

    if (
        "face_yolov8m.pt" in source
        and "hand_yolov8n.pt" in source
        and "sam_vit_b_01ec64.pth" not in source
    ):
        source += """
# SAM for Impact Face/Hand Detailer (explicit clean-Colab dependency).
import os, subprocess, urllib.request
SAM_DIR = '/content/ComfyUI/models/sams'
SAM_FILE = 'sam_vit_b_01ec64.pth'
SAM_PATH = os.path.join(SAM_DIR, SAM_FILE)
os.makedirs(SAM_DIR, exist_ok=True)
if not (os.path.exists(SAM_PATH) and os.path.getsize(SAM_PATH) > 0):
    sam_url = 'https://dl.fbaipublicfiles.com/segment_anything/sam_vit_b_01ec64.pth'
    rc = subprocess.run(
        ['aria2c', '--console-log-level=error', '-c', '-x', '8', '-s', '8', '-k', '1M',
         sam_url, '-d', SAM_DIR, '-o', SAM_FILE],
        check=False,
    ).returncode
    if rc != 0 or not (os.path.exists(SAM_PATH) and os.path.getsize(SAM_PATH) > 0):
        urllib.request.urlretrieve(sam_url, SAM_PATH)
print('SAM ready:', SAM_PATH)
"""
        changes.add("sam-vit-b")

    return source, changes


def main() -> None:
    notebooks = sorted((ROOT / "notebooks").glob("**/*.ipynb"))
    if not notebooks:
        raise RuntimeError("No notebooks found")

    summary: list[str] = []
    for path in notebooks:
        notebook = json.loads(path.read_text(encoding="utf-8"))
        notebook_changes: set[str] = set()
        for cell in notebook.get("cells", []):
            if cell.get("cell_type") != "code":
                continue
            raw_source = cell.get("source", "")
            source = "".join(raw_source) if isinstance(raw_source, list) else str(raw_source)
            source, changes = patch_source(source)
            if changes:
                cell["source"] = source.splitlines(keepends=True)
                notebook_changes.update(changes)
        path.write_text(
            json.dumps(notebook, ensure_ascii=True, indent=2) + "\n",
            encoding="utf-8",
        )
        summary.append(f"{path.relative_to(ROOT)}: {','.join(sorted(notebook_changes)) or 'unchanged'}")

    print("\n".join(summary))


if __name__ == "__main__":
    main()
