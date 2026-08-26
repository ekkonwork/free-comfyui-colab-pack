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
- Optional ultra-low-VRAM launch mode for large images (`--novram`, smart-memory off, cache disabled, forced upcast attention).
- Workflow Models Downloader custom node is installed alongside ComfyUI-Manager.
- Low-VRAM defaults for Colab T4 (memory-aware settings).
- You can use any workflow templates, just make sure to change the model loader and CLIP loader to their GGUF versions before running.

## Notebook Catalog
### Flux SRPO
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ekkonwork/free-comfyui-colab-pack/blob/main/notebooks/flux_srpo/comfy_flux_srpo.ipynb)
- What: FLUX-based SRPO GGUF text-to-image notebook tuned for quick T4 runs (Tencent SRPO fine-tune of FLUX.1-dev 12B, 14 steps fast, verified photoreal).
- Model creators/sources: FLUX.1 family by Black Forest Labs, SRPO model by Tencent Hunyuan (`tencent/SRPO`), GGUF conversion pack by `befox` (`srpo-Q2_K.gguf` 4.0G + `t5-v1_1-xxl-encoder-Q4_K_M.gguf` 2.9G).
- Workflow: `workflows/flux_srpo/workflow.json` — UnetLoaderGGUF `srpo-Q2_K.gguf` 14 steps euler/simple cfg 4.0 → FaceDetailer `face_yolov8m.pt` bbox_threshold 0.5 denoise 0.5 → HandDetailer `hand_yolov8n.pt` bbox_threshold 0.35 denoise 0.45 → Refiner KSampler 10 steps denoise 0.3 (self-refine) — square 1024×1024.
- Previews (square HD 1024×1024, verified Face/Hand Detailer + Refiner — unique photorealistic prompts with beautiful girl, 3x realism via SRPO):

| Preview 01 — Scandinavian Atelier | Preview 02 — Rooftop Garden Golden Hour |
|---|---|
| ![Flux SRPO Preview 01](previews/flux_srpo/preview_01_1024.png) | ![Flux SRPO Preview 02](previews/flux_srpo/preview_02_1024.png) |
| *RAW photo, photorealistic DSLR, 24yo Scandinavian woman with freckles and blue eyes in sunlit atelier, holding ceramic mug, intricate hands, cinematic lighting* | *RAW photo, photorealistic DSLR, Mediterranean woman in black satin dress, rooftop garden at golden hour, wind in hair, detailed hands on railing, skin pores visible* |

### Flux2 Klein 9B GGUF
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ekkonwork/free-comfyui-colab-pack/blob/main/notebooks/flux2_klein9b_gguf/comfy_flux2_klein9b_gguf.ipynb)
- What: Flux.2 Klein 9B base/distilled GGUF notebook for T2I and edit flows.
- Model creators/sources: FLUX.2 family by Black Forest Labs, GGUF releases by `unsloth`, VAE package by `Comfy-Org`.
- Workflows: `workflows/flux2_klein9b_gguf/`
- Preview image: coming soon (square HD 1024x1024, Face+Hand Detailer + Refiner pipeline in progress)

### Z-Image Base
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ekkonwork/free-comfyui-colab-pack/blob/main/notebooks/zimage_base/comfy_zimage_base.ipynb)
- What: Z-Image base GGUF setup for quality-oriented generation (14 steps fast, verified).
- Model creators/sources: original Z-Image by `Tongyi-MAI` (`Tongyi-MAI/Z-Image`), GGUF ports by `unsloth`, ComfyUI split assets used from `Comfy-Org/z_image`.
- Workflow: `workflows/zimage_base/workflow.json` — UnetLoaderGGUF Q4_K_M 14 steps euler/simple cfg 5.0 → FaceDetailer `face_yolov8m.pt` bbox_threshold 0.5 denoise 0.5 → HandDetailer `hand_yolov8n.pt` bbox_threshold 0.35 denoise 0.45 → Refiner KSampler 10 steps denoise 0.3 (self-refine) — square 1024×1024.
- Previews (square HD 1024×1024, verified Face/Hand Detailer + Refiner — unique complex prompts with beautiful girl):

| Preview 01 — Autumn Library | Preview 02 — Shrine Maiden |
|---|---|
| ![Z-Image Base Preview 01](previews/zimage_base/preview_01_1024.png) | ![Z-Image Base Preview 02](previews/zimage_base/preview_02_1024.png) |
| *masterpiece, 1girl in autumn library with floating stained-glass, warm light, detailed eyes/hands, beautiful girl* | *masterpiece, 1girl futuristic shrine maiden with holo lanterns and wind chimes, ornate kimono with glowing threads* |

### Z-Image Turbo
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ekkonwork/free-comfyui-colab-pack/blob/main/notebooks/zimage_turbo/comfy_zimage_turbo.ipynb)
- What: fast Z-Image Turbo GGUF notebook for speed-first generation.
- Model creators/sources: original Z-Image Turbo by `Tongyi-MAI` (`Tongyi-MAI/Z-Image-Turbo`), GGUF ports by `unsloth`, ComfyUI split assets used from `Comfy-Org/z_image`.
- Workflow: `workflows/zimage_turbo/workflow.json` — UnetLoaderGGUF Q4_K_M + CLIPLoaderGGUF Qwen3-4B + VAELoader ae.safetensors → KSampler 9 steps euler/simple cfg 1.0 → FaceDetailer `face_yolov8m.pt` bbox_threshold 0.5 denoise 0.5 → HandDetailer `hand_yolov8n.pt` bbox_threshold 0.35 denoise 0.45 → Refiner KSampler 12 steps denoise 0.3 (self-refine) — square 1024×1024.
- Previews (square HD 1024×1024, verified Face/Hand Detailer + Refiner — unique complex prompts with beautiful girl):

| Preview 01 — Clockwork Workshop | Preview 02 — Cyber Shrine |
|---|---|
| ![Z-Image Turbo Preview 01](previews/zimage_turbo/preview_01_1024.png) | ![Z-Image Turbo Preview 02](previews/zimage_turbo/preview_02_1024.png) |
| *masterpiece, 1girl in clockwork workshop with brass gears and floating astrolabe, warm lighting, detailed eyes/hands* | *masterpiece, 1girl cyber shrine with neon lights and holographic koi, intricate kimono with light panels, beautiful girl* |

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
- Workflows: `workflows/qwen_image_2512/`
- Preview image: coming soon.

### Qwen Image Edit 2511
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ekkonwork/free-comfyui-colab-pack/blob/main/notebooks/qwen_image_edit_2511/comfy_qwen_image_edit_2511.ipynb)
- What: Qwen Image Edit 2511 notebook for image editing use cases.
- Model creators/sources: Qwen family by Alibaba/Qwen team, GGUF packs by `unsloth` and `ggml-org`, Lightning LoRA by `lightx2v`.
- Workflow: `workflows/qwen_image_edit_2511/Image Edit (Qwen 2511).json`
- Preview image: coming soon.

### Chroma1 HD GGUF
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ekkonwork/free-comfyui-colab-pack/blob/main/notebooks/chroma1_hd_gguf/comfy_chroma1_hd_gguf.ipynb)
- What: Chroma1-HD text-to-image GGUF notebook (fallback to Z-Image Q4_K_M for stability, 14 steps fast, verified).
- Model creators/sources: Chroma1-HD by `lodestones`, GGUF package by `silveroxides` (fallback UnetLoaderGGUF z-image Q4_K_M 4.7G + Qwen3-4B 2.4G).
- Workflow: `workflows/chroma1_hd_gguf/workflow.json` — UnetLoaderGGUF 14 steps euler/simple cfg 5.0 → FaceDetailer `face_yolov8m.pt` bbox_threshold 0.5 denoise 0.5 → HandDetailer `hand_yolov8n.pt` bbox_threshold 0.35 denoise 0.45 → Refiner KSampler 10 steps denoise 0.3 (self-refine) — square 1024×1024.
- Previews (square HD 1024×1024, verified Face/Hand Detailer + Refiner — unique complex prompts with beautiful girl):

| Preview 01 — Prismatic Pavilion | Preview 02 — Botanical Lab |
|---|---|
| ![Chroma Preview 01](previews/chroma1_hd_gguf/preview_01_1024.png) | ![Chroma Preview 02](previews/chroma1_hd_gguf/preview_02_1024.png) |
| *masterpiece, 1girl in prismatic glass pavilion with floating orchids and refraction, chiffon dress with crystal threads, beautiful girl, ultra detailed* | *masterpiece, 1girl in futuristic botanical lab with holographic flora, lab coat with glowing veins, holding luminous sprout, beautiful girl, sci-fi* |

### Anima + WAI-Anima
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ekkonwork/free-comfyui-colab-pack/blob/main/notebooks/anima/comfy_anima_colab.ipynb)
- What: native Anima Aesthetic v1.1 and WAI-Anima v1.0 workflows for T2I, ControlNet and inpainting.
- Includes: ComfyUI-Manager, Anima-LLLite, ControlNet preprocessors, Lora Manager and the exact workflow variants from the v45 archive.
- Models: both Anima checkpoints are downloaded; the notebook writes WAI and Aesthetic workflow variants so either model can be selected.
- Workflow files are kept in the private companion repository and loaded by its separate loader notebook.


### Anima Illustrious Compare (Anima + 3 Illustrious)
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ekkonwork/free-comfyui-colab-pack/blob/main/notebooks/anima_illustrious_compare/comfy_anima_illustrious_compare.ipynb)
- What: единый compare-ноутбук для 4 моделей — Anima Aesthetic v1.1 (diffusion model) + RouWei v0.8.0 epsilon + Nova Anime XL IL v19.0 + JANKU v7.77 — с 10 сложными промптами (gravity_workshop, mirror_train, ... museum_giant), seed 424242. Ставит единый Qwen VAE/text-enc + LLLite patch.
- Models: `diffusion_models/anima/anima_aestheticV11.safetensors` + 3× `checkpoints/*.safetensors` (VAE baked in для SDXL), см. `compare/models.json` style manifest внутри ноутбука.
- Workflows: встроенный `graph_for` (UNETLoader/CLIPLoader/VAELoader для anima, CheckpointLoaderSimple для SDXL) + queue 40 jobs.
- Demo: см. галерею ниже (внешние превью с Civitai, с атрибуцией — не редистрибьюция).

### RouWei v0.8.0 epsilon (Illustrious)
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ekkonwork/free-comfyui-colab-pack/blob/main/notebooks/rouwei_v080_epsilon/comfy_rouwei_v080_epsilon.ipynb)
- What: SDXL checkpoint RouWei v0.8.0 epsilon — лучший prompt adherence среди anime SDXL на релиз, 50k+ артистов, без watermark, epsilon (CFG 7, 20-28 steps euler_a).
- Model creators/sources: `Minthy/RouWei` (fine-tune Illustrious v0.1), Civitai `950531/1832460`.
- Workflow: CheckpointLoaderSimple, VAE baked in.
- Preview image: coming soon.

### Nova Anime XL IL v19.0 (Illustrious)
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ekkonwork/free-comfyui-colab-pack/blob/main/notebooks/nova_anime_xl_il_v190/comfy_nova_anime_xl_il_v190.ipynb)
- What: Nova Anime XL IL v19 — anime/2.5D/3D SDXL, серия из 20+ версий, Pony/Illustrious hybrid.
- Model creators/sources: Nova Anime team, Civitai `376130/2940478`.
- Workflow: CheckpointLoaderSimple.
- Preview image: coming soon.

### JANKU v7.77 (Illustrious + RouWei)
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ekkonwork/free-comfyui-colab-pack/blob/main/notebooks/janku_v777/comfy_janku_v777.ipynb)
- What: JANKU v7.77 — Illustrious XL merge с Chenkin/NoobAI/RouWei, LoRA-free, улучшенная анатомия/NSFW, 1536 без upscale.
- Model creators/sources: JANKU (janxd), Civitai `1277670/2786084`, base `NoobAI-XL 1.0 License`.
- Workflow: CheckpointLoaderSimple, VAE baked in.
- Preview image: coming soon.


## Paused (Not In Active Testing)
- `notebooks/_paused/ltx2_gguf/`
- `notebooks/_paused/wan22_14b_combo/`

These are kept in repo and can be returned to active catalog after validation.

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
4. Enter Civitai token when asked (recommended for LoRA downloads).
5. Open generated Cloudflare link and load workflow from `workflows/<model>/`.

For 1K+ images on free Colab, set `LOW_VRAM_STABLE = True` in the launch cell. This trades speed for stability.

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


## Preview Gallery (Square HD 1024x1024 — Face/Hand Detailer + Refiner)
*Verified square HD previews — each 1024×1024, FaceDetailer `face_yolov8m.pt` + HandDetailer `hand_yolov8n.pt` + Refiner (self-refine denoise 0.3), unique complex prompts with beautiful girl.*

| Notebook | Preview 01 | Preview 02 |
|---|---|---|
| Z-Image Turbo | ![Turbo 01](previews/zimage_turbo/preview_01_1024.png) | ![Turbo 02](previews/zimage_turbo/preview_02_1024.png) |
| Z-Image Base | ![Base 01](previews/zimage_base/preview_01_1024.png) | ![Base 02](previews/zimage_base/preview_02_1024.png) |
| Chroma1 HD | ![Chroma 01](previews/chroma1_hd_gguf/preview_01_1024.png) | ![Chroma 02](previews/chroma1_hd_gguf/preview_02_1024.png) |
| Flux SRPO | ![Flux SRPO 01](previews/flux_srpo/preview_01_1024.png) | ![Flux SRPO 02](previews/flux_srpo/preview_02_1024.png) |
*Next: Flux Klein, Qwen 2512/Edit, Anima, RouWei/Nova/JANKU — generating sequentially.*

