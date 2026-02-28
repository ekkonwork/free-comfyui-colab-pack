# Free ComfyUI Colab Pack

![Free ComfyUI Colab Pack Banner](docs/assets/free_comfyui_colab_pack_banner.png)


[![Donate on Boosty](https://img.shields.io/badge/Donate-Boosty-F15F2C?style=for-the-badge)](https://boosty.to/ekkonwork/donate)
[![Hire Me on LinkedIn](https://img.shields.io/badge/Hire%20Me-LinkedIn-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/mikhail-kuznetsov-14304433b)

Free Google Colab notebooks for popular ComfyUI workflows on low VRAM GPUs (focused on Colab Free T4).

## Why this project
I put a lot of time and effort into these notebooks. They are tuned, tested, and maintained so people can run popular models for free in Colab.

The goal is simple: fast, practical, and stable model access in Colab without heavy local setup.

## Killer Features
- Auto quant selection by VRAM budget (rare in public Colab packs).
- GGUF-first setup for low VRAM use cases.
- Match-only Lenovo UltraReal LoRA download by base-model tag.
- Built-in Hugging Face + Civitai token prompts.
- Stable Cloudflare tunnel launch logic with retries and health checks.
- Low-VRAM defaults for Colab T4 (memory-aware settings).
- Ready-to-use per-model workflow JSON files in this repo.

## Notebook Catalog
### Flux SRPO
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ekkonwork/free-comfyui-colab-pack/blob/main/notebooks/flux_srpo/comfy_flux_srpo.ipynb)
- What: FLUX-based SRPO GGUF text-to-image notebook tuned for quick T4 runs.
- Model creators/sources: FLUX.1 family by Black Forest Labs, SRPO model by Tencent Hunyuan (`tencent/SRPO`), GGUF conversion pack by `befox`.
- Workflow: `workflows/flux_srpo/flux_schnell_full_text_to_image.json`
- Preview image: coming soon.

### Flux2 Klein 9B GGUF
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ekkonwork/free-comfyui-colab-pack/blob/main/notebooks/flux2_klein9b_gguf/comfy_flux2_klein9b_gguf.ipynb)
- What: Flux.2 Klein 9B base/distilled GGUF notebook for T2I and edit flows.
- Model creators/sources: FLUX.2 family by Black Forest Labs, GGUF releases by `unsloth`, VAE package by `Comfy-Org`.
- Workflows: `workflows/flux2_klein9b_gguf/`
- Preview image: coming soon.

### Z-Image Base
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ekkonwork/free-comfyui-colab-pack/blob/main/notebooks/zimage_base/comfy_zimage_base.ipynb)
- What: Z-Image base GGUF setup for quality-oriented generation.
- Model creators/sources: original Z-Image by `Tongyi-MAI` (`Tongyi-MAI/Z-Image`), GGUF ports by `unsloth`, ComfyUI split assets used from `Comfy-Org/z_image`.
- Workflow: `workflows/zimage_base/zimage_base_test_workflow.json`
- Preview image: coming soon.

### Z-Image Turbo
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ekkonwork/free-comfyui-colab-pack/blob/main/notebooks/zimage_turbo/comfy_zimage_turbo.ipynb)
- What: fast Z-Image Turbo GGUF notebook for speed-first generation.
- Model creators/sources: original Z-Image Turbo by `Tongyi-MAI` (`Tongyi-MAI/Z-Image-Turbo`), GGUF ports by `unsloth`, ComfyUI split assets used from `Comfy-Org/z_image`.
- Workflow: `workflows/zimage_turbo/zimage_turbo_test_workflow.json`
- Preview image: coming soon.

### Z-Image Turbo + Base
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ekkonwork/free-comfyui-colab-pack/blob/main/notebooks/zimage_turbo_base/comfy_zimage_turbo_base.ipynb)
- What: combo notebook with Turbo + Base variants in one setup.
- Model creators/sources: original Z-Image models by `Tongyi-MAI` (`Tongyi-MAI/Z-Image` and `Tongyi-MAI/Z-Image-Turbo`), GGUF variants by `unsloth`, ComfyUI split assets used from `Comfy-Org/z_image`.
- Workflows: `workflows/zimage_turbo_base/`
- Preview image: coming soon.

### Z-Image Turbo + SeedVR2 Upscaler
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ekkonwork/free-comfyui-colab-pack/blob/main/notebooks/zimage_seedvr2/comfy_zimage_seedvr2.ipynb)
- What: two-stage pipeline (Z-Image generation + SeedVR2 upscaling).
- Model creators/sources: original Z-Image Turbo by `Tongyi-MAI` (`Tongyi-MAI/Z-Image-Turbo`) with GGUF ports by `unsloth`, SeedVR2 node/files by `numz` and GGUF pack by `cmeka`.
- Workflows: `workflows/zimage_seedvr2/`
- Preview image: coming soon.

### Qwen Image 2512
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ekkonwork/free-comfyui-colab-pack/blob/main/notebooks/qwen_image_2512/comfy_qwen_image_2512.ipynb)
- What: Qwen Image 2512 GGUF generation notebook with optional Lightning LoRA.
- Model creators/sources: Qwen family by Alibaba/Qwen team, GGUF packs by `unsloth` and `ggml-org`, Lightning LoRA by `lightx2v`.
- Workflow: `workflows/qwen_image_2512/qwen_image_test_workflow.json`
- Preview image: coming soon.

### Qwen Image Edit 2511
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ekkonwork/free-comfyui-colab-pack/blob/main/notebooks/qwen_image_edit_2511/comfy_qwen_image_edit_2511.ipynb)
- What: Qwen Image Edit 2511 notebook for image editing use cases.
- Model creators/sources: Qwen family by Alibaba/Qwen team, GGUF packs by `unsloth` and `ggml-org`, Lightning LoRA by `lightx2v`.
- Workflow: `workflows/qwen_image_edit_2511/qwen_image_edit_test_workflow_v2.json`
- Preview image: coming soon.

### Chroma1 HD GGUF
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ekkonwork/free-comfyui-colab-pack/blob/main/notebooks/chroma1_hd_gguf/comfy_chroma1_hd_gguf.ipynb)
- What: Chroma1-HD text-to-image GGUF notebook.
- Model creators/sources: Chroma1-HD by `lodestones`, GGUF package by `silveroxides`.
- Workflow: `workflows/chroma1_hd_gguf/ComfyUI_Chroma1-HD_T2I-workflow.json`
- Preview image: coming soon.

## Paused (Not In Active Testing)
- `notebooks/_paused/ltx2_gguf/`
- `notebooks/_paused/wan22_14b_combo/`

These are kept in repo and can be returned to active catalog after validation.

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

I spend a lot of time on open-source projects. Even a $1 donation helps and goes directly to GPU servers and food.

[![Donate](docs/assets/Donate_Banner.webp)](https://boosty.to/ekkonwork/donate)
[![Donate on Boosty](https://img.shields.io/badge/Donate-Boosty-F15F2C?style=for-the-badge)](https://boosty.to/ekkonwork/donate)

### Crypto Donations (Telegram Wallet)
[![Donate via Telegram Wallet](https://img.shields.io/badge/Donate-Telegram%20Wallet-2AABEE?style=for-the-badge&logo=telegram&logoColor=white)](https://t.me/wallet)

![Telegram Wallet QR](docs/assets/telegram_wallet_qr.png)

Wallet addresses:
- TON: `UQAMPvqduXVWyax325-zqk81rTwNG1bRhCvXPyIs7eeIxEVp`
- USDT (TON): `UQAMPvqduXVWyax325-zqk81rTwNG1bRhCvXPyIs7eeIxEVp`
- Memo/Tag: check Wallet receive screen before sending.

See full support info in `docs/SUPPORT.md`.

## Hire Me
[![Hire Me](docs/assets/Hire_Me_banner.webp)](https://www.linkedin.com/in/mikhail-kuznetsov-14304433b)
[![Hire Me on LinkedIn](https://img.shields.io/badge/Hire%20Me-LinkedIn-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/mikhail-kuznetsov-14304433b)

- Email: `ekkonwork@gmail.com`
- Telegram: `@Mikhail_ML_ComfyUI`

## Notes
- Respect model licenses and terms.
- Cloudflare tunnels can still be unstable in Colab due to external network conditions.
