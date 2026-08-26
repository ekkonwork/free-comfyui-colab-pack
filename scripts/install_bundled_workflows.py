#!/usr/bin/env python3
"""Add one deterministic bundled-workflow install cell to each supported notebook."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CELL_ID = "cell_install_bundled_workflow"
SUPPORTED = {
    "anima",
    "anima_illustrious_compare",
    "chroma1_hd_gguf",
    "flux_srpo",
    "flux2_klein9b_gguf",
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


RUNTIME_REPLACEMENTS = {
    "chroma1_hd_gguf": {
        "Chroma1-HD-Q4_K_M.gguf": "chroma_fname",
        "flan-t5-xxl-Q4_K_M.gguf": "flan_fname",
    },
    "flux_srpo": {
        "srpo-Q3_K.gguf": "srpo_fname",
        "t5-v1_1-xxl-encoder-Q4_K_M.gguf": "t5_fname",
    },
    "flux2_klein9b_gguf": {
        "flux-2-klein-base-9b-Q4_K_M.gguf": "(base_fname or distilled_fname)",
        "Qwen3-8B-Q4_K_M.gguf": "q_fname",
    },
    "qwen_image_2512": {
        "qwen-image-2512-Q2_K.gguf": "img_fname",
        "Qwen2.5-VL-7B-Instruct-Q4_K_M.gguf": "vl_fname",
        "Qwen-Image-2512-Lightning-4steps-V1.0-fp32.safetensors": "globals().get('lora_fname', 'Qwen-Image-2512-Lightning-4steps-V1.0-fp32.safetensors')",
    },
    "qwen_image_edit_2511": {
        "qwen-image-edit-2511-Q2_K.gguf": "edit_fname",
        "Qwen2.5-VL-7B-Instruct-Q4_K_M.gguf": "vl_fname",
        "Qwen-Image-Edit-2511-Lightning-4steps-V1.0-bf16.safetensors": "globals().get('lora_fname', 'Qwen-Image-Edit-2511-Lightning-4steps-V1.0-bf16.safetensors')",
    },
    "zimage_base": {
        "z-image-Q4_K_M.gguf": "zb_fname",
        "Qwen3-4B-Q4_K_M.gguf": "q_fname",
    },
    "zimage_turbo": {
        "z-image-turbo-Q4_K_M.gguf": "zt_fname",
        "Qwen3-4B-Q4_K_M.gguf": "q_fname",
    },
    "zimage_seedvr2": {
        "z-image-turbo-Q4_K_M.gguf": "z_fname",
        "Qwen3-4B-Q4_K_M.gguf": "q_fname",
    },
    "zimage_turbo_base": {
        "z-image-turbo-Q4_K_M.gguf": "zt_fname",
        "z-image-Q4_K_M.gguf": "zb_fname",
        "Qwen3-4B-Q4_K_M.gguf": "q_fname",
    },
}


def workflow_cell(model: str) -> dict:
    replacements = RUNTIME_REPLACEMENTS.get(model, {})
    replacement_lines = "\n".join(f'    {old!r}: {expression},' for old, expression in replacements.items())
    source = f'''# @title Install bundled workflow in ComfyUI
import json
from pathlib import Path
from urllib.request import urlopen

WORKFLOW_URL = "https://raw.githubusercontent.com/ekkonwork/free-comfyui-colab-pack/main/workflows/{model}/workflow.json"
WORKFLOW_DIR = Path("/content/ComfyUI/user/default/workflows")
WORKFLOW_PATH = WORKFLOW_DIR / "{model}.json"
WORKFLOW_DIR.mkdir(parents=True, exist_ok=True)
workflow = json.loads(urlopen(WORKFLOW_URL, timeout=60).read().decode("utf-8"))
replacements = {{
{replacement_lines}
}}

def replace_runtime_names(value):
    if isinstance(value, str):
        return replacements.get(value, value)
    if isinstance(value, list):
        return [replace_runtime_names(item) for item in value]
    if isinstance(value, dict):
        return {{key: replace_runtime_names(item) for key, item in value.items()}}
    return value

workflow = replace_runtime_names(workflow)
WORKFLOW_PATH.write_text(json.dumps(workflow, ensure_ascii=False, indent=2), encoding="utf-8")
print("Bundled workflow installed:", WORKFLOW_PATH)
'''
    return {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {"id": CELL_ID},
        "outputs": [],
        "source": source.splitlines(keepends=True),
    }


def main() -> None:
    seen = set()
    for folder in sorted(SUPPORTED):
        notebook_dir = ROOT / "notebooks" / folder
        paths = list(notebook_dir.glob("*.ipynb"))
        if len(paths) != 1:
            raise RuntimeError(f"Expected exactly one notebook in {notebook_dir}, got {len(paths)}")
        path = paths[0]
        notebook = json.loads(path.read_text(encoding="utf-8"))
        if folder == "anima_illustrious_compare":
            obsolete_plugin = '    "images-grid-comfy-plugin": "https://github.com/LEv145/images-grid-comfy-plugin.git",\n'
            for cell in notebook["cells"]:
                source = "".join(cell.get("source", []))
                if obsolete_plugin in source:
                    cell["source"] = source.replace(obsolete_plugin, "").splitlines(keepends=True)
        notebook["cells"] = [
            cell for cell in notebook["cells"] if cell.get("metadata", {}).get("id") != CELL_ID
        ]
        insert_at = next(
            (i + 1 for i, cell in enumerate(notebook["cells"])
             if cell.get("metadata", {}).get("id") == "cell_models"),
            2,
        )
        notebook["cells"].insert(insert_at, workflow_cell(folder))
        path.write_text(json.dumps(notebook, ensure_ascii=True, indent=2) + "\n", encoding="utf-8")
        seen.add(folder)
        print(path.relative_to(ROOT))
    if seen != SUPPORTED:
        raise RuntimeError(f"Unpatched notebooks: {sorted(SUPPORTED - seen)}")


if __name__ == "__main__":
    main()
