#!/usr/bin/env python3
"""Repository-wide static checks for bundled ComfyUI UI workflows.

The checks encode the audited architecture:
- one workflow.json per supported notebook;
- sampler parity for main/refiner/Face/Hand (denoise is the intentional delta);
- Klein + Qwen Edit exceptions;
- mandatory Qwen 8-step Lightning;
- optional bypassed SeedVR2 low-VRAM stage;
- CPU SAM for clean T4 operation.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
WORKFLOWS = {
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
GGUF_COUNTS = {
    "chroma1_hd_gguf": (1, 1),
    "flux_srpo": (1, 1),
    "flux2_klein9b_gguf": (2, 2),
    "qwen_image_2512": (1, 1),
    "qwen_image_edit_2511": (1, 1),
    "zimage_base": (1, 1),
    "zimage_seedvr2": (1, 1),
    "zimage_turbo": (1, 1),
    "zimage_turbo_base": (2, 2),
}


def nodes(graph: dict[str, Any]) -> list[dict[str, Any]]:
    return graph.get("nodes", [])


def subgraphs(graph: dict[str, Any]) -> list[dict[str, Any]]:
    return graph.get("definitions", {}).get("subgraphs", [])


def all_nodes(graph: dict[str, Any]):
    yield from nodes(graph)
    for sub in subgraphs(graph):
        yield from nodes(sub)


def link_parts(link):
    if isinstance(link, list):
        return link[0], link[1], link[2], link[3], link[4], link[5]
    return (
        link["id"],
        link["origin_id"],
        link["origin_slot"],
        link["target_id"],
        link["target_slot"],
        link["type"],
    )


def link_map(graph: dict[str, Any]):
    return {link_parts(link)[0]: link_parts(link) for link in graph.get("links", [])}


def node_map(graph: dict[str, Any]):
    return {node["id"]: node for node in nodes(graph)}


def input_index(node: dict[str, Any], name: str) -> int:
    for index, item in enumerate(node.get("inputs", [])):
        if item.get("name") == name:
            return index
    raise AssertionError(f"{node.get('type')}#{node.get('id')}: missing input {name}")


def output_index(node: dict[str, Any], name: str) -> int:
    for index, item in enumerate(node.get("outputs", [])):
        if item.get("name") == name:
            return index
    raise AssertionError(f"{node.get('type')}#{node.get('id')}: missing output {name}")


def origin_for_input(graph: dict[str, Any], node: dict[str, Any], name: str):
    item = node["inputs"][input_index(node, name)]
    assert item.get("link") is not None, f"{node.get('type')}#{node.get('id')}: {name} is disconnected"
    link = link_map(graph)[item["link"]]
    return link[1], link[2], link[5]


def resolve_origin(graph: dict[str, Any], node: dict[str, Any], name: str):
    by_id = node_map(graph)
    origin_id, origin_slot, kind = origin_for_input(graph, node, name)
    seen = set()
    while origin_id in by_id and by_id[origin_id].get("type") == "Reroute":
        assert origin_id not in seen, "reroute cycle"
        seen.add(origin_id)
        reroute = by_id[origin_id]
        origin_id, origin_slot, kind = origin_for_input(graph, reroute, "input")
    return origin_id, origin_slot, kind


def assert_link_integrity(graph: dict[str, Any], label: str) -> None:
    by_id = node_map(graph)
    links = link_map(graph)
    for link_id, (_, origin, origin_slot, target, target_slot, _) in links.items():
        assert origin == -10 or origin in by_id, f"{label}: link {link_id} bad origin {origin}"
        assert target == -20 or target in by_id, f"{label}: link {link_id} bad target {target}"
        if origin != -10:
            assert origin_slot < len(by_id[origin].get("outputs", [])), f"{label}: link {link_id} bad origin slot"
            assert link_id in (by_id[origin]["outputs"][origin_slot].get("links") or []), f"{label}: link {link_id} missing at origin"
        if target != -20:
            assert target_slot < len(by_id[target].get("inputs", [])), f"{label}: link {link_id} bad target slot"
            assert by_id[target]["inputs"][target_slot].get("link") == link_id, f"{label}: link {link_id} missing at target"
    for node in nodes(graph):
        for item in node.get("inputs", []):
            if item.get("link") is not None:
                assert item["link"] in links, f"{label}: stale input link {item['link']}"
        for item in node.get("outputs", []):
            for link_id in item.get("links") or []:
                assert link_id in links, f"{label}: stale output link {link_id}"


def seedvr_nodes(graph: dict[str, Any]):
    by_type = {}
    for node in nodes(graph):
        by_type.setdefault(node.get("type"), []).append(node)
    return (
        by_type.get("SeedVR2LoadDiTModel", []),
        by_type.get("SeedVR2LoadVAEModel", []),
        by_type.get("SeedVR2VideoUpscaler", []),
    )


def check_seedvr(graph: dict[str, Any], label: str, up_id: int | None = None) -> None:
    by_id = node_map(graph)
    if up_id is None:
        ups = [n for n in nodes(graph) if n.get("type") == "SeedVR2VideoUpscaler"]
        assert len(ups) == 1, f"{label}: expected one SeedVR2 stage"
        up = ups[0]
    else:
        up = by_id[up_id]
        assert up.get("type") == "SeedVR2VideoUpscaler", f"{label}: selected node is not SeedVR2"
    dit_id, _, _ = origin_for_input(graph, up, "dit")
    vae_id, _, _ = origin_for_input(graph, up, "vae")
    dit, vae = by_id[dit_id], by_id[vae_id]
    assert dit.get("type") == "SeedVR2LoadDiTModel", f"{label}: SeedVR2 DiT loader missing"
    assert vae.get("type") == "SeedVR2LoadVAEModel", f"{label}: SeedVR2 VAE loader missing"
    assert dit.get("widgets_values", [])[:7] == [
        "seedvr2_ema_3b-Q4_K_M.gguf", "cuda:0", 32, True, "cpu", False, "sdpa"
    ], f"{label}: unexpected SeedVR2 DiT low-VRAM profile"
    vw = vae.get("widgets_values", [])
    assert vw[:10] == [
        "ema_vae_fp16.safetensors", "cuda:0", True, 768, 128, True, 768, 128, "false", "cpu"
    ], f"{label}: unexpected SeedVR2 tiled VAE profile"
    uw = up.get("widgets_values", [])
    assert up.get("mode") == 4, f"{label}: SeedVR2 must be bypassed by default"
    assert uw[2:7] == [1536, 1536, 1, False, "lab"], f"{label}: unexpected SeedVR2 image settings"
    assert uw[11] == "cpu", f"{label}: SeedVR2 offload must be CPU"


def check_sam_and_detectors(
    graph: dict[str, Any],
    label: str,
    face: dict[str, Any] | None = None,
    hand: dict[str, Any] | None = None,
) -> None:
    by_id = node_map(graph)
    if face is None or hand is None:
        sam = [n for n in nodes(graph) if n.get("type") == "SAMLoader"]
        assert len(sam) == 1, f"{label}: expected one SAMLoader"
        sam_node = sam[0]
        detector_names = [
            str(n.get("widgets_values", [""])[0])
            for n in nodes(graph)
            if n.get("type") == "UltralyticsDetectorProvider"
        ]
        assert sum("face_yolov8m.pt" in name for name in detector_names) == 1, f"{label}: face YOLO missing"
        assert sum("hand_yolov8n.pt" in name for name in detector_names) == 1, f"{label}: hand YOLO missing"
    else:
        face_det_id, _, _ = resolve_origin(graph, face, "bbox_detector")
        hand_det_id, _, _ = resolve_origin(graph, hand, "bbox_detector")
        face_det, hand_det = by_id[face_det_id], by_id[hand_det_id]
        assert face_det.get("type") == hand_det.get("type") == "UltralyticsDetectorProvider"
        assert "face_yolov8m.pt" in str(face_det.get("widgets_values", [""])[0]), f"{label}: face YOLO mismatch"
        assert "hand_yolov8n.pt" in str(hand_det.get("widgets_values", [""])[0]), f"{label}: hand YOLO mismatch"
        sam_id, _, _ = resolve_origin(graph, face, "sam_model_opt")
        assert resolve_origin(graph, hand, "sam_model_opt")[0] == sam_id, f"{label}: face/hand SAM differ"
        sam_node = by_id[sam_id]
        assert sam_node.get("type") == "SAMLoader", f"{label}: detailer SAM source is not SAMLoader"
    assert sam_node.get("widgets_values", [])[:2] == ["sam_vit_b_01ec64.pth", "CPU"], f"{label}: SAM must be vit_b on CPU"


def standard_chain_from_output(
    graph: dict[str, Any], label: str, up_id: int | None = None
):
    """Return base, refiner, face, hand by walking backward from one SeedVR branch."""
    by_id = node_map(graph)
    if up_id is None:
        ups = [n for n in nodes(graph) if n.get("type") == "SeedVR2VideoUpscaler"]
        assert len(ups) == 1, f"{label}: one SeedVR2 upscaler required"
        up = ups[0]
    else:
        up = by_id[up_id]
        assert up.get("type") == "SeedVR2VideoUpscaler", f"{label}: invalid SeedVR branch anchor"
    hand_id, _, _ = origin_for_input(graph, up, "image")
    hand = by_id[hand_id]
    assert hand.get("type") == "FaceDetailer" and "Hand Detailer" in str(hand.get("title", "")), f"{label}: SeedVR must follow Hand Detailer"
    face_id, _, _ = origin_for_input(graph, hand, "image")
    face = by_id[face_id]
    assert face.get("type") == "FaceDetailer", f"{label}: hand must follow face detailer"
    decode_id, _, _ = origin_for_input(graph, face, "image")
    decode = by_id[decode_id]
    assert decode.get("type") == "VAEDecode", f"{label}: face detailer must follow VAEDecode"
    ref_id, _, _ = origin_for_input(graph, decode, "samples")
    refiner = by_id[ref_id]
    if refiner.get("type") == "KSampler":
        base_id, _, _ = origin_for_input(graph, refiner, "latent_image")
        base = by_id[base_id]
        assert base.get("type") == "KSampler", f"{label}: refiner must follow base KSampler"
    elif refiner.get("type") == "SamplerCustomAdvanced":
        base_id, _, _ = origin_for_input(graph, refiner, "latent_image")
        base = by_id[base_id]
        assert base.get("type") == "SamplerCustomAdvanced", f"{label}: refiner must follow base custom sampler"
    else:
        raise AssertionError(f"{label}: unsupported refiner node {refiner.get('type')}")
    return base, refiner, face, hand


def check_detail_sources(graph: dict[str, Any], face: dict[str, Any], hand: dict[str, Any], label: str) -> None:
    for name in ("model", "clip", "vae", "positive", "negative"):
        assert resolve_origin(graph, face, name) == resolve_origin(graph, hand, name), f"{label}: face/hand {name} sources differ"
    assert resolve_origin(graph, face, "sam_model_opt") == resolve_origin(graph, hand, "sam_model_opt"), f"{label}: face/hand SAM sources differ"


def check_standard_ksampler_pipeline(
    graph: dict[str, Any],
    label: str,
    expected: tuple[int, float, str, str] | None = None,
    up_id: int | None = None,
) -> tuple[int, float, str, str]:
    base, refiner, face, hand = standard_chain_from_output(graph, label, up_id)
    assert base.get("type") == refiner.get("type") == "KSampler", f"{label}: expected KSampler pipeline"
    preset = tuple(base.get("widgets_values", [])[2:6])
    if expected is not None:
        assert preset == expected, f"{label}: main sampling {preset} != {expected}"
    assert tuple(refiner.get("widgets_values", [])[2:6]) == preset, f"{label}: refiner sampling mismatch"
    assert refiner.get("widgets_values", [None] * 7)[6] == 0.30, f"{label}: refiner denoise"
    assert tuple(face.get("widgets_values", [])[5:9]) == preset, f"{label}: face sampling mismatch"
    assert tuple(hand.get("widgets_values", [])[5:9]) == preset, f"{label}: hand sampling mismatch"
    assert face.get("widgets_values", [None] * 10)[9] == 0.50, f"{label}: face denoise"
    assert hand.get("widgets_values", [None] * 10)[9] == 0.35, f"{label}: hand denoise"
    check_detail_sources(graph, face, hand, label)
    check_sam_and_detectors(graph, label, face, hand)
    check_seedvr(graph, label, up_id)
    return preset


def check_anima_subgraph(graph: dict[str, Any], label: str) -> None:
    base, refiner, face, hand = standard_chain_from_output(graph, label)
    assert tuple(base["widgets_values"][4:6]) == ("euler", "simple")
    assert tuple(refiner["widgets_values"][4:6]) == ("euler", "simple")
    assert tuple(face["widgets_values"][7:9]) == ("euler", "simple")
    assert tuple(hand["widgets_values"][7:9]) == ("euler", "simple")
    assert refiner["widgets_values"][6] == 0.30 and face["widgets_values"][9] == 0.50 and hand["widgets_values"][9] == 0.35
    for name in ("steps", "cfg"):
        source = resolve_origin(graph, base, name)
        assert resolve_origin(graph, refiner, name) == source, f"{label}: refiner dynamic {name} differs"
        assert resolve_origin(graph, face, name) == source, f"{label}: face dynamic {name} differs"
        assert resolve_origin(graph, hand, name) == source, f"{label}: hand dynamic {name} differs"
    ints = [n.get("widgets_values", [None])[0] for n in nodes(graph) if n.get("type") == "PrimitiveInt"]
    floats = [n.get("widgets_values", [None])[0] for n in nodes(graph) if n.get("type") == "PrimitiveFloat"]
    assert 30 in ints and 8 in ints, f"{label}: Base/Turbo step presets missing"
    assert 4 in floats and 1 in floats, f"{label}: Base/Turbo CFG presets missing"
    check_detail_sources(graph, face, hand, label)
    check_sam_and_detectors(graph, label)
    check_seedvr(graph, label)


def check_custom_chroma(graph: dict[str, Any], label: str) -> None:
    base, refiner, face, hand = standard_chain_from_output(graph, label)
    assert base.get("type") == refiner.get("type") == "SamplerCustomAdvanced"
    beta = next(n for n in nodes(graph) if n.get("type") == "BetaSamplingScheduler")
    cfg = next(n for n in nodes(graph) if n.get("type") == "CFGGuider")
    sampler = next(n for n in nodes(graph) if n.get("type") == "KSamplerSelect")
    shift = next(n for n in nodes(graph) if n.get("type") == "ModelSamplingAuraFlow")
    split = next(n for n in nodes(graph) if n.get("type") == "SplitSigmasDenoise")
    assert beta.get("widgets_values")[:3] == [26, 0.45, 0.45]
    assert cfg.get("widgets_values", [None])[0] == 3.8
    assert sampler.get("widgets_values", [None])[0] == "euler"
    assert shift.get("widgets_values", [None])[0] == 1
    assert split.get("widgets_values", [None])[0] == 0.30
    for item in (face, hand):
        assert tuple(item["widgets_values"][5:9]) == (26, 3.8, "euler", "beta")
        assert item["inputs"][input_index(item, "scheduler_func_opt")].get("link") is not None
    assert face["widgets_values"][9] == 0.50 and hand["widgets_values"][9] == 0.35
    for name in ("noise", "guider", "sampler"):
        assert resolve_origin(graph, refiner, name) == resolve_origin(graph, base, name), f"{label}: refiner {name} mismatch"
    assert resolve_origin(graph, refiner, "sigmas")[0] == split["id"], f"{label}: refiner must use split beta sigmas"
    check_detail_sources(graph, face, hand, label)
    check_sam_and_detectors(graph, label)
    check_seedvr(graph, label)


def check_custom_srpo(graph: dict[str, Any], label: str) -> None:
    base, refiner, face, hand = standard_chain_from_output(graph, label)
    assert base.get("type") == refiner.get("type") == "SamplerCustomAdvanced"
    scheduler = next(n for n in nodes(graph) if n.get("type") == "BasicScheduler")
    guidance = next(n for n in nodes(graph) if n.get("type") == "FluxGuidance")
    sampler = next(n for n in nodes(graph) if n.get("type") == "KSamplerSelect")
    split = next(n for n in nodes(graph) if n.get("type") == "SplitSigmasDenoise")
    assert scheduler.get("widgets_values")[:3] == ["normal", 50, 1]
    assert guidance.get("widgets_values", [None])[0] == 3.5
    assert sampler.get("widgets_values", [None])[0] == "euler"
    assert split.get("widgets_values", [None])[0] == 0.30
    assert any(n.get("type") == "ImpactNegativeConditioningPlaceholder" for n in nodes(graph))
    for item in (face, hand):
        assert tuple(item["widgets_values"][5:9]) == (50, 1, "euler", "normal")
    assert face["widgets_values"][9] == 0.50 and hand["widgets_values"][9] == 0.35
    for name in ("noise", "guider", "sampler"):
        assert resolve_origin(graph, refiner, name) == resolve_origin(graph, base, name), f"{label}: refiner {name} mismatch"
    assert resolve_origin(graph, refiner, "sigmas")[0] == split["id"], f"{label}: refiner must use split normal sigmas"
    assert resolve_origin(graph, face, "positive")[0] == guidance["id"], f"{label}: face lost FluxGuidance"
    assert resolve_origin(graph, hand, "positive")[0] == guidance["id"], f"{label}: hand lost FluxGuidance"
    check_detail_sources(graph, face, hand, label)
    check_sam_and_detectors(graph, label)
    check_seedvr(graph, label)


def check_output_is_seedvr(graph: dict[str, Any], label: str) -> None:
    links = link_map(graph)
    output_links = graph.get("outputs", [{}])[0].get("linkIds") or []
    assert len(output_links) == 1, f"{label}: expected one IMAGE output link"
    link = links[output_links[0]]
    by_id = node_map(graph)
    assert by_id[link[1]].get("type") == "SeedVR2VideoUpscaler", f"{label}: SeedVR2 must be final subgraph stage"


def check_save_is_seedvr(graph: dict[str, Any], save: dict[str, Any], label: str) -> None:
    origin_id, _, _ = origin_for_input(graph, save, "images")
    assert node_map(graph)[origin_id].get("type") == "SeedVR2VideoUpscaler", f"{label}: SeedVR2 must feed SaveImage"


def check_folder(folder: Path) -> None:
    files = sorted(p.name for p in folder.iterdir() if p.is_file())
    assert files == ["workflow.json"], f"{folder.name}: expected exactly workflow.json, got {files}"
    graph = json.loads((folder / "workflow.json").read_text(encoding="utf-8"))
    assert_link_integrity(graph, f"{folder.name}:top")
    for sub in subgraphs(graph):
        assert_link_integrity(sub, f"{folder.name}:{sub.get('name')}")
    serialized = json.dumps(graph, ensure_ascii=False)
    low = serialized.lower()

    if folder.name in GGUF_COUNTS:
        expected_unet, expected_clip = GGUF_COUNTS[folder.name]
        all_types = [n.get("type") for n in all_nodes(graph)]
        assert all_types.count("UnetLoaderGGUF") == expected_unet, f"{folder.name}: GGUF UNET count"
        clip_count = all_types.count("CLIPLoaderGGUF") + all_types.count("DualCLIPLoaderGGUF")
        assert clip_count == expected_clip, f"{folder.name}: GGUF CLIP count"
        assert "UNETLoader" not in all_types and "DualCLIPLoader" not in all_types, f"{folder.name}: native loader remains"

    if folder.name == "anima":
        assert len(subgraphs(graph)) == 1
        check_anima_subgraph(subgraphs(graph)[0], "anima")
        check_output_is_seedvr(subgraphs(graph)[0], "anima")

    elif folder.name == "anima_illustrious_compare":
        assert len(subgraphs(graph)) == 1
        check_anima_subgraph(subgraphs(graph)[0], "compare:Anima")
        check_output_is_seedvr(subgraphs(graph)[0], "compare:Anima")
        saves = [n for n in nodes(graph) if n.get("type") == "SaveImage"]
        seed_saves = [s for s in saves if node_map(graph)[origin_for_input(graph, s, "images")[0]].get("type") == "SeedVR2VideoUpscaler"]
        assert len(seed_saves) == 3, "compare: expected RouWei/Nova/JANKU SeedVR saves"
        presets = []
        for save in seed_saves:
            up_id, _, _ = origin_for_input(graph, save, "images")
            presets.append(
                check_standard_ksampler_pipeline(
                    graph, f"compare:{save['id']}", up_id=up_id
                )
            )
        presets = sorted(presets)
        assert presets == sorted([
            (28, 5, "euler_ancestral", "normal"),
            (30, 5, "euler_ancestral", "normal"),
            (30, 5, "euler_ancestral", "normal"),
        ])
        for save in seed_saves:
            check_save_is_seedvr(graph, save, f"compare:{save['id']}")

    elif folder.name in {"janku_v777", "nova_anime_xl_il_v190", "rouwei_v080_epsilon"}:
        expected = {
            "janku_v777": (30, 5, "euler_ancestral", "normal"),
            "nova_anime_xl_il_v190": (30, 5, "euler_ancestral", "normal"),
            "rouwei_v080_epsilon": (28, 5, "euler_ancestral", "normal"),
        }[folder.name]
        check_standard_ksampler_pipeline(graph, folder.name, expected)
        check_save_is_seedvr(graph, next(n for n in nodes(graph) if n.get("type") == "SaveImage"), folder.name)

    elif folder.name == "chroma1_hd_gguf":
        check_custom_chroma(graph, folder.name)
        check_save_is_seedvr(graph, next(n for n in nodes(graph) if n.get("type") == "SaveImage"), folder.name)

    elif folder.name == "flux_srpo":
        check_custom_srpo(graph, folder.name)
        check_save_is_seedvr(graph, next(n for n in nodes(graph) if n.get("type") == "SaveImage"), folder.name)

    elif folder.name == "qwen_image_2512":
        assert "Qwen-Image-2512-Lightning-8steps-V1.0-bf16.safetensors" in serialized
        assert "Lightning-4steps" not in serialized
        assert len(subgraphs(graph)) == 1
        check_standard_ksampler_pipeline(subgraphs(graph)[0], folder.name, (8, 1, "euler", "simple"))
        check_output_is_seedvr(subgraphs(graph)[0], folder.name)

    elif folder.name == "qwen_image_edit_2511":
        assert "Qwen-Image-Edit-2511-Lightning-8steps-V1.0-bf16.safetensors" in serialized
        assert "Lightning-4steps" not in serialized
        assert "FaceDetailer" not in serialized and "refiner" not in low
        sub = subgraphs(graph)[0]
        sampler_node = next(n for n in nodes(sub) if n.get("type") == "KSampler")
        assert tuple(sampler_node["widgets_values"][2:6]) == (8, 1, "euler", "simple")
        check_seedvr(sub, folder.name)
        check_output_is_seedvr(sub, folder.name)

    elif folder.name == "flux2_klein9b_gguf":
        assert "FaceDetailer" not in serialized and "refiner" not in low
        assert len(subgraphs(graph)) == 2, "Klein must have Base + Distilled on one canvas"
        seen = {}
        for sub in subgraphs(graph):
            scheduler = next(n for n in nodes(sub) if n.get("type") == "Flux2Scheduler")
            cfg = next(n for n in nodes(sub) if n.get("type") == "CFGGuider")
            unet = next(n for n in nodes(sub) if n.get("type") == "UnetLoaderGGUF")
            sampler_node = next(n for n in nodes(sub) if n.get("type") == "KSamplerSelect")
            seen[unet["widgets_values"][0]] = (scheduler["widgets_values"][0], cfg["widgets_values"][0], sampler_node["widgets_values"][0])
            check_seedvr(sub, f"Klein:{sub.get('name')}")
            check_output_is_seedvr(sub, f"Klein:{sub.get('name')}")
        assert seen == {
            "flux-2-klein-base-9b-Q4_K_M.gguf": (50, 4, "euler"),
            "flux-2-klein-9b-Q4_K_M.gguf": (4, 1, "euler"),
        }

    elif folder.name in {"zimage_base", "zimage_seedvr2", "zimage_turbo", "zimage_turbo_base"}:
        expected_by_name = {
            "Text to Image(Z-Image-Base Int8)": (30, 4, "res_multistep", "simple"),
            "Text to Image (Z-Image-Turbo)": (8, 1, "res_multistep", "simple"),
        }
        assert subgraphs(graph)
        for sub in subgraphs(graph):
            assert sub.get("name") in expected_by_name, f"{folder.name}: unknown Z-Image branch {sub.get('name')}"
            check_standard_ksampler_pipeline(sub, f"{folder.name}:{sub.get('name')}", expected_by_name[sub["name"]])
            check_output_is_seedvr(sub, f"{folder.name}:{sub.get('name')}")

    else:
        raise AssertionError(f"Unhandled workflow folder {folder.name}")

    assert "seedvr2_ema_3b-q4_k_m.gguf" in low, f"{folder.name}: SeedVR2 3B Q4 missing"


def check_notebook_binding(folder: str) -> None:
    notebook_dir = ROOT / "notebooks" / folder
    paths = list(notebook_dir.glob("*.ipynb"))
    assert len(paths) == 1, f"{folder}: expected one notebook"
    notebook = json.loads(paths[0].read_text(encoding="utf-8"))
    text = "\n".join(
        "".join(cell.get("source", [])) if isinstance(cell.get("source", []), list) else str(cell.get("source", ""))
        for cell in notebook.get("cells", [])
    )
    assert f"workflows/{folder}/workflow.json" in text, f"{folder}: bundled workflow URL missing"
    assert "/content/ComfyUI/user/default/workflows" in text, f"{folder}: install directory missing"


def main() -> None:
    folders = {p.name for p in (ROOT / "workflows").iterdir() if p.is_dir()}
    assert folders == WORKFLOWS, f"workflow folder set changed: {sorted(folders ^ WORKFLOWS)}"
    for name in sorted(WORKFLOWS):
        check_folder(ROOT / "workflows" / name)
        check_notebook_binding(name)
        print("OK", name)


if __name__ == "__main__":
    main()
