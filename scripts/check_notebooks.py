#!/usr/bin/env python3
"""Static validation for every Colab notebook, including paused notebooks."""

from __future__ import annotations

import ast
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MODEL_NOTEBOOKS = {
    "anima",
    "anima_illustrious_compare",
    "chroma1_hd_gguf",
    "flux2_klein9b_gguf",
    "flux_srpo",
    "janku_v777",
    "nova_anime_xl_il_v190",
    "qwen_image_2512",
    "qwen_image_edit_2511",
    "rouwei_v080_epsilon",
    "zimage_base",
    "zimage_seedvr2",
    "zimage_turbo",
    "zimage_turbo_base",
}
DETAIL_NOTEBOOKS = MODEL_NOTEBOOKS - {"flux2_klein9b_gguf", "qwen_image_edit_2511"}


def source_text(cell: dict) -> str:
    source = cell.get("source", "")
    return "".join(source) if isinstance(source, list) else str(source)


def compile_colab_cell(path: Path, index: int, source: str) -> None:
    # Convert shell/IPython magic lines to pass while preserving indentation.
    cleaned = []
    for line in source.splitlines():
        stripped = line.strip()
        if stripped.startswith(("!", "%")):
            indent = line[: len(line) - len(line.lstrip())]
            cleaned.append(f"{indent}pass  # {stripped[:100]}")
        else:
            cleaned.append(line)
    ast.parse("\n".join(cleaned), filename=f"{path}:cell{index}")


def notebook_key(path: Path) -> str | None:
    rel = path.relative_to(ROOT / "notebooks")
    if rel.parts[0] == "_paused":
        return None
    return rel.parts[0]


def check_notebook(path: Path) -> None:
    notebook = json.loads(path.read_text(encoding="utf-8"))
    cells = notebook.get("cells", [])
    texts = [source_text(cell) for cell in cells]
    text = "\n".join(texts)

    assert "Bearer ***" not in text, f"{path}: redacted bearer token literal remains"

    for index, cell in enumerate(cells):
        if cell.get("cell_type") == "code":
            compile_colab_cell(path, index, source_text(cell))

    assert text.count("# @title 5a) Watchdog: ComfyUI + Cloudflare Tunnel keepalive") == 1, f"{path}: unified Cloudflare watchdog missing/duplicated"
    assert text.count("# @title 5c) Watchdog: ComfyUI + bore.pub keepalive") == 1, f"{path}: unified bore watchdog missing/duplicated"
    assert "Manager/external ComfyUI startup detected" in text, f"{path}: Manager-safe process detection missing"
    assert "COMFY_RESTART_GRACE = 25" in text and "COMFY_HUNG_GRACE = 120" in text, f"{path}: ComfyUI restart grace missing"
    assert "Watchdog: Cloudflare Tunnel keepalive (auto-restart, never exits)" not in text, f"{path}: legacy CF-only watchdog remains"
    assert "Watchdog: bore.pub keepalive (auto-restart, never exits)" not in text, f"{path}: legacy bore-only watchdog remains"

    key = notebook_key(path)
    if key in MODEL_NOTEBOOKS:
        assert "https://github.com/numz/ComfyUI-SeedVR2_VideoUpscaler.git" in text, f"{key}: SeedVR2 node install missing"
        assert f"workflows/{key}/workflow.json" in text, f"{key}: bundled workflow URL missing"
        assert "/content/ComfyUI/user/default/workflows" in text, f"{key}: bundled workflow directory missing"

    if key in DETAIL_NOTEBOOKS:
        for name in ("face_yolov8m.pt", "hand_yolov8n.pt", "sam_vit_b_01ec64.pth"):
            assert name in text, f"{key}: detail dependency {name} missing"
        assert "/content/ComfyUI/models/sams" in text, f"{key}: SAM directory missing"
        assert "dl.fbaipublicfiles.com/segment_anything/sam_vit_b_01ec64.pth" in text, f"{key}: explicit SAM URL missing"

    if key == "qwen_image_2512":
        assert "Qwen-Image-2512-Lightning-8steps-V1.0-bf16.safetensors" in text
        assert "Qwen-Image-2512-Lightning-4steps" not in text

    if key == "qwen_image_edit_2511":
        assert "Qwen-Image-Edit-2511-Lightning-8steps-V1.0-bf16.safetensors" in text
        assert "Qwen-Image-Edit-2511-Lightning-4steps" not in text

    if key == "flux2_klein9b_gguf":
        assert "patch_flux2_gguf_workflow" not in text and "force_mode(" not in text, "Klein: runtime workflow generator remains"
        assert "This is the only Klein workflow: Base + Distilled branches on one canvas." in text
        assert "flux2_klein9b_gguf.json" in text

    print("OK", path.relative_to(ROOT))


def main() -> None:
    paths = sorted((ROOT / "notebooks").rglob("*.ipynb"))
    assert paths, "No notebooks found"
    for path in paths:
        check_notebook(path)


if __name__ == "__main__":
    main()
