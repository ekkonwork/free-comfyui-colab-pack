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
DETAIL_EXCEPTIONS = {"flux2_klein9b_gguf", "qwen_image_edit_2511"}
DETAIL_NOTEBOOKS = MODEL_NOTEBOOKS - DETAIL_EXCEPTIONS
EXPECTED_NOTEBOOKS = {
    "_paused/ltx2_gguf/comfy_ltx2_gguf.ipynb",
    "_paused/wan22_14b_combo/comfy_wan22_14b_combo.ipynb",
    "anima/comfy_anima_colab.ipynb",
    "anima_illustrious_compare/comfy_anima_illustrious_compare.ipynb",
    "chroma1_hd_gguf/comfy_chroma1_hd_gguf.ipynb",
    "flux2_klein9b_gguf/comfy_flux2_klein9b_gguf.ipynb",
    "flux_srpo/comfy_flux_srpo.ipynb",
    "janku_v777/comfy_janku_v777.ipynb",
    "nova_anime_xl_il_v190/comfy_nova_anime_xl_il_v190.ipynb",
    "qwen_image_2512/comfy_qwen_image_2512.ipynb",
    "qwen_image_edit_2511/comfy_qwen_image_edit_2511.ipynb",
    "rouwei_v080_epsilon/comfy_rouwei_v080_epsilon.ipynb",
    "universal/comfy_universal_colab.ipynb",
    "zimage_base/comfy_zimage_base.ipynb",
    "zimage_seedvr2/comfy_zimage_seedvr2.ipynb",
    "zimage_turbo/comfy_zimage_turbo.ipynb",
    "zimage_turbo_base/comfy_zimage_turbo_base.ipynb",
}


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


def cell_index(texts: list[str], needle: str) -> int:
    matches = [index for index, text in enumerate(texts) if needle in text]
    assert len(matches) == 1, f"Expected exactly one cell containing {needle!r}, got {matches}"
    return matches[0]


def assert_common_order(path: Path, texts: list[str]) -> None:
    install = cell_index(texts, "# @title 2) Install ComfyUI + Managers + node pack")
    launch = cell_index(texts, "# @title 5) Launch ComfyUI + Cloudflare Quick Tunnel")
    cf_watch = cell_index(texts, "# @title 5a) Watchdog: ComfyUI + Cloudflare Tunnel keepalive")
    bore_fallback = cell_index(texts, "# @title 5b) Fallback: bore.pub tunnel")
    bore_watch = cell_index(texts, "# @title 5c) Watchdog: ComfyUI + bore.pub keepalive")
    assert install < launch < cf_watch < bore_fallback < bore_watch, (
        f"{path}: unsafe launch/watchdog cell order "
        f"{install=}, {launch=}, {cf_watch=}, {bore_fallback=}, {bore_watch=}"
    )


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
    assert_common_order(path, texts)

    key = notebook_key(path)
    if key in MODEL_NOTEBOOKS:
        assert "https://github.com/numz/ComfyUI-SeedVR2_VideoUpscaler.git" in text, f"{key}: SeedVR2 node install missing"
        assert f"workflows/{key}/workflow.json" in text, f"{key}: bundled workflow URL missing"
        assert "/content/ComfyUI/user/default/workflows" in text, f"{key}: bundled workflow directory missing"
        install = cell_index(texts, "# @title 2) Install ComfyUI + Managers + node pack")
        model_download = cell_index(texts, "# @title 3) Download")
        workflow_install = cell_index(texts, "Install bundled workflow in ComfyUI") if key != "flux2_klein9b_gguf" else cell_index(texts, "Install the ONE bundled Klein workflow in ComfyUI")
        launch = cell_index(texts, "# @title 5) Launch ComfyUI + Cloudflare Quick Tunnel")
        assert install < model_download < workflow_install < launch, (
            f"{key}: unsafe Run-all order: "
            f"{install=}, {model_download=}, {workflow_install=}, {launch=}"
        )

    if key in DETAIL_NOTEBOOKS:
        for name in ("face_yolov8m.pt", "hand_yolov8n.pt", "sam_vit_b_01ec64.pth"):
            assert name in text, f"{key}: detail dependency {name} missing"
        assert "/content/ComfyUI/models/sams" in text, f"{key}: SAM directory missing"
        assert "dl.fbaipublicfiles.com/segment_anything/sam_vit_b_01ec64.pth" in text, f"{key}: explicit SAM URL missing"
        workflow_install = cell_index(texts, "Install bundled workflow") 
        detail_download = cell_index(texts, "# @title 3b) Download YOLO")
        launch = cell_index(texts, "# @title 5) Launch ComfyUI + Cloudflare Quick Tunnel")
        assert workflow_install < detail_download < launch, (
            f"{key}: detail dependencies must be installed before launch"
        )

    if key in DETAIL_EXCEPTIONS:
        for name in ("face_yolov8m.pt", "hand_yolov8n.pt", "sam_vit_b_01ec64.pth"):
            assert name not in text, f"{key}: unused detail dependency {name} remains"

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

    if key == "anima_illustrious_compare":
        launch = cell_index(texts, "# @title 5) Launch ComfyUI + Cloudflare Quick Tunnel")
        queue = cell_index(texts, "# @title 4) Queue a reproducible ComfyUI compare")
        cf_watch = cell_index(texts, "# @title 5a) Watchdog: ComfyUI + Cloudflare Tunnel keepalive")
        assert launch < queue < cf_watch, "Compare queue must run after launch and before blocking watchdog"

    if key == "universal":
        assert "https://github.com/numz/ComfyUI-SeedVR2_VideoUpscaler.git" in text, "universal: SeedVR2 node install missing"
        for name in ("face_yolov8m.pt", "hand_yolov8n.pt", "sam_vit_b_01ec64.pth"):
            assert name in text, f"universal: dependency {name} missing"
        detail_download = cell_index(texts, "# @title 3b) Download YOLO + SAM")
        launch = cell_index(texts, "# @title 5) Launch ComfyUI + Cloudflare Quick Tunnel")
        assert detail_download < launch, "universal: detail dependencies must precede launch"

    print("OK", path.relative_to(ROOT))


def main() -> None:
    paths = sorted((ROOT / "notebooks").rglob("*.ipynb"))
    relative = {path.relative_to(ROOT / "notebooks").as_posix() for path in paths}
    assert relative == EXPECTED_NOTEBOOKS, (
        f"Notebook set changed: missing={sorted(EXPECTED_NOTEBOOKS - relative)}, "
        f"extra={sorted(relative - EXPECTED_NOTEBOOKS)}"
    )
    for path in paths:
        check_notebook(path)


if __name__ == "__main__":
    main()
