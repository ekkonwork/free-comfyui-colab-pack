# Free ComfyUI Colab Pack

[![Donate on Boosty](https://img.shields.io/badge/Donate-Boosty-F15F2C?style=for-the-badge)](https://boosty.to/ekkonwork/donate)
[![Hire Me on LinkedIn](https://img.shields.io/badge/Hire%20Me-LinkedIn-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/mikhail-kuznetsov-14304433b)

Free Google Colab notebooks for popular ComfyUI workflows on low VRAM GPUs (focused on Colab Free T4).

## Why this project
I put a lot of time and effort into these notebooks. They are tuned, tested, and maintained so people can run popular models for free in Colab.

If this project helps you, support really matters. Donations directly help me pay for GPU servers and food while I keep improving and testing this pack.

## Killer Features
- Auto quant selection by VRAM budget (rare in public Colab packs).
- GGUF-first setup for low VRAM use cases.
- Match-only Lenovo UltraReal LoRA download by base-model tag.
- Built-in Hugging Face + Civitai token prompts.
- Stable Cloudflare tunnel launch logic with retries and health checks.
- Low-VRAM defaults for Colab T4 (memory-aware settings).
- Ready-to-use per-model workflow JSON files in this repo.

## Active Models
- Flux SRPO
- Z-Image-Base
- Z-Image-Turbo
- Z-Image-Turbo + Z-Image-Base
- Z-Image-Turbo + SeedVR2 Upscaler
- Qwen Image 2512
- Qwen Image Edit 2511
- Flux.2 Klein 9B GGUF
- Chroma1 HD GGUF

## Paused (Not In Active Testing)
- Wan 2.2 14B combo
- LTX2 GGUF

These models are kept in `_paused` folders and can return to active list after validation.

## Repository Layout
```text
free-comfyui-colab-pack/
  notebooks/<model>/comfy_<model>.ipynb
  notebooks/_paused/<model>/comfy_<model>.ipynb
  workflows/<model>/*.json
  workflows/_paused/<model>/*.json
  docs/
```

## Quick Start
1. Open a notebook from `notebooks/<model>/` in Colab.
2. Run cells top-to-bottom.
3. Enter Hugging Face token when asked.
4. Enter Civitai token when asked (recommended for LoRA downloads).
5. Open generated Cloudflare link and load workflow from `workflows/<model>/`.

## Support
If these notebooks save you time, please support development:

[![Donate](docs/assets/Donate_Banner.webp)](https://boosty.to/ekkonwork/donate)

[![Donate on Boosty](https://img.shields.io/badge/Donate-Boosty-F15F2C?style=for-the-badge)](https://boosty.to/ekkonwork/donate)

See full support info in `docs/SUPPORT.md`.

## Hire Me
[![Hire Me](docs/assets/Hire_Me_banner.webp)](https://www.linkedin.com/in/mikhail-kuznetsov-14304433b)

[![Hire Me on LinkedIn](https://img.shields.io/badge/Hire%20Me-LinkedIn-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/mikhail-kuznetsov-14304433b)

## Notes
- Respect model licenses and terms.
- Cloudflare tunnels can still be unstable in Colab due to external network conditions.
