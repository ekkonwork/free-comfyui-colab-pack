#!/usr/bin/env python3
"""Static checks for bundled UI workflows and notebook auto-install cells."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
GGUF = {
    "chroma1_hd_gguf": (1, 1),
    "flux_srpo": (1, 1),
    "flux2_klein9b_gguf": (1, 1),
    "qwen_image_2512": (1, 1),
    "qwen_image_edit_2511": (1, 1),
    "zimage_base": (1, 1),
    "zimage_seedvr2": (1, 1),
    "zimage_turbo": (1, 1),
    "zimage_turbo_base": (2, 2),
}
SDXL = {"janku_v777", "nova_anime_xl_il_v190", "rouwei_v080_epsilon"}


def all_nodes(graph):
    yield from graph.get("nodes", [])
    for subgraph in graph.get("definitions", {}).get("subgraphs", []):
        yield from subgraph.get("nodes", [])


def links_for(nodes):
    return {link for node in nodes for output in node.get("outputs", []) for link in (output.get("links") or [])}


def check_graph(folder: Path) -> None:
    files = list(folder.glob("*"))
    assert [p.name for p in files if p.is_file()] == ["workflow.json"], f"{folder.name}: expected only workflow.json"
    graph = json.loads((folder / "workflow.json").read_text(encoding="utf-8"))
    assert isinstance(graph.get("nodes"), list) and isinstance(graph.get("links"), list), f"{folder.name}: not UI workflow JSON"
    nodes = list(all_nodes(graph))
    types = [n.get("type") for n in nodes]
    serialized = json.dumps(graph, ensure_ascii=False).lower()
    assert "seedvr" not in serialized, f"{folder.name}: SeedVR is forbidden in bundled workflows"
    if folder.name in GGUF:
        expected_unet, expected_clip = GGUF[folder.name]
        assert types.count("UnetLoaderGGUF") == expected_unet, f"{folder.name}: wrong GGUF UNET loader count"
        assert sum(types.count(t) for t in ("CLIPLoaderGGUF", "DualCLIPLoaderGGUF")) == expected_clip, f"{folder.name}: wrong GGUF CLIP loader count"
        assert "UNETLoader" not in types and "CLIPLoader" not in types and "DualCLIPLoader" not in types, f"{folder.name}: native loader remains"
        for node in nodes:
            if node.get("type") in {"UnetLoaderGGUF", "CLIPLoaderGGUF", "DualCLIPLoaderGGUF"}:
                assert any(output.get("links") for output in node.get("outputs", [])), f"{folder.name}: disconnected {node['type']}"
    if folder.name in SDXL:
        top = graph["nodes"]
        by_title = {n.get("title"): n for n in top if n.get("title")}
        top_types = [n.get("type") for n in top]
        assert top_types.count("KSampler") == 2, f"{folder.name}: needs base + refiner KSampler"
        assert top_types.count("FaceDetailer") == 2, f"{folder.name}: needs face + hand detailers"
        detector_models = [str(n.get("widgets_values", [""])[0]) for n in top if n.get("type") == "UltralyticsDetectorProvider"]
        assert any("face" in name for name in detector_models), f"{folder.name}: face detector missing"
        assert any("hand" in name for name in detector_models), f"{folder.name}: hand detector missing"
        titles = {n.get("title") for n in top}
        assert "Second sampler / refiner" in titles and "Hand Detailer" in titles
        base = next(n for n in top if n.get("type") == "KSampler" and n.get("title") != "Second sampler / refiner")
        refiner = by_title["Second sampler / refiner"]
        face = next(n for n in top if n.get("type") == "FaceDetailer" and n.get("title") != "Hand Detailer")
        hand = by_title["Hand Detailer"]
        decode = next(n for n in top if n.get("type") == "VAEDecode")
        edges = {(link[1], link[3]) for link in graph["links"]}
        assert (base["id"], refiner["id"]) in edges, f"{folder.name}: base does not feed refiner"
        assert (refiner["id"], decode["id"]) in edges, f"{folder.name}: refiner does not feed decode"
        assert (decode["id"], face["id"]) in edges, f"{folder.name}: decode does not feed face detailer"
        assert (face["id"], hand["id"]) in edges, f"{folder.name}: face does not feed hand detailer"
    if folder.name == "anima":
        assert "anima/anima_aestheticv11.safetensors" in serialized
    if folder.name == "anima_illustrious_compare":
        for name in (
            "anima/anima_aestheticv11.safetensors",
            "rouwei_v080epsilon.safetensors",
            "novaanimexl_ilv190.safetensors",
            "jankutrainedchenkinnoobai_v777.safetensors",
        ):
            assert name in serialized, f"comparison missing {name}"
    assert set(link[0] for link in graph["links"]) <= links_for(graph["nodes"]), f"{folder.name}: stale top-level links"


def check_notebook(folder: Path) -> None:
    paths = list((ROOT / "notebooks" / folder.name).glob("*.ipynb"))
    assert len(paths) == 1, f"{folder.name}: notebook missing"
    notebook = json.loads(paths[0].read_text(encoding="utf-8"))
    cells = [cell for cell in notebook["cells"] if cell.get("metadata", {}).get("id") == "cell_install_bundled_workflow"]
    assert len(cells) == 1, f"{folder.name}: workflow install cell count {len(cells)}"
    source = "".join(cells[0]["source"])
    compile(source, f"{paths[0]}:{cells[0].get('metadata', {}).get('id')}", "exec")
    assert f"workflows/{folder.name}/workflow.json" in source
    assert "/content/ComfyUI/user/default/workflows" in source


def main() -> None:
    folders = sorted((ROOT / "workflows").iterdir())
    for folder in folders:
        if folder.is_dir():
            check_graph(folder)
            check_notebook(folder)
            print("OK", folder.name)


if __name__ == "__main__":
    main()
