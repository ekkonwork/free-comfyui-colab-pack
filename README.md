# Free ComfyUI Colab Pack

Free Google Colab notebooks for popular ComfyUI workflows on low VRAM GPUs (focused on Colab Free T4).

This pack is built for people who want to run strong image/video models without setting up a full local server.

## Why this project
I put a lot of time and effort into these notebooks. They are tuned, tested, and maintained so people can run popular models for free in Colab.

If this project helps you, support really matters. Donations help me pay for GPU servers and food while I keep improving these notebooks.

## Killer Features
- Auto quant selection by VRAM budget (rare in public Colab packs).
- GGUF-first setup for low VRAM use cases.
- Match-only Lenovo UltraReal LoRA download by base-model tag.
- Built-in Hugging Face + Civitai token prompts.
- Stable Cloudflare tunnel launch logic with retries and health checks.
- Low-VRAM defaults for Colab T4 (memory-aware settings).
- Ready-to-use per-model workflow JSON files in this repo.

## Included Models
- Flux SRPO
- Z-Image-Base
- Z-Image-Turbo
- Z-Image-Turbo + Z-Image-Base
- Z-Image-Turbo + SeedVR2 Upscaler
- Qwen Image 2512
- Qwen Image Edit 2511
- Flux.2 Klein 9B GGUF
- Chroma1 HD GGUF
- Wan 2.2 14B combo
- LTX2 GGUF

## Repository Layout
```text
free-comfyui-colab-pack/
  notebooks/<model>/comfy_<model>.ipynb
  workflows/<model>/*.json
  docs/
```

## Quick Start
1. Open a notebook from `notebooks/<model>/` in Colab.
2. Run cells top-to-bottom.
3. Enter Hugging Face token when asked.
4. Enter Civitai token when asked (optional, but recommended for LoRA downloads).
5. Open generated Cloudflare link and load workflow from `workflows/<model>/`.

## Donate
If these notebooks save you time or money, please support development.

Your donation helps keep this project alive and directly goes to:
- GPU server costs
- model testing time
- food while maintaining the pack

See `docs/SUPPORT.md` for donation links.

## Hire Me
Available for paid work:
- Custom ComfyUI/Colab notebook builds
- Workflow optimization for low VRAM GPUs
- End-to-end smoke/regression setup for model packs

Contact details are in `docs/SUPPORT.md`.

## Notes
- Respect model licenses and terms.
- Cloudflare tunnels can still be unstable in Colab due to external network conditions.
- This repository currently does not include promo images/examples (planned later).
