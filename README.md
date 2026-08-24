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
- What: FLUX-based SRPO GGUF text-to-image notebook tuned for quick T4 runs.
- Model creators/sources: FLUX.1 family by Black Forest Labs, SRPO model by Tencent Hunyuan (`tencent/SRPO`), GGUF conversion pack by `befox`.
- Workflow: `workflows/flux_srpo/flux_dev_example.json`
- Preview: ![Flux SRPO](https://huggingface.co/tencent/SRPO/resolve/main/comfyui/SRPO-workflow.png) — Tencent SRPO [[HF tencent/SRPO](https://huggingface.co/tencent/SRPO)] (external, not redistributed)

### Flux2 Klein 9B GGUF
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ekkonwork/free-comfyui-colab-pack/blob/main/notebooks/flux2_klein9b_gguf/comfy_flux2_klein9b_gguf.ipynb)
- What: Flux.2 Klein 9B base/distilled GGUF notebook for T2I and edit flows.
- Model creators/sources: FLUX.2 family by Black Forest Labs, GGUF releases by `unsloth`, VAE package by `Comfy-Org`.
- Workflows: `workflows/flux2_klein9b_gguf/`
- Preview: ![Flux2 Klein](https://image.civitai.com/xG1nkqKTMzGDvpLrqFT7WA/f905bc28-9db6-4f83-85ae-93c94718881d/width=320/139055133.jpeg) — FLUX.2 Klein 9B [[HF black-forest-labs/FLUX.2-klein-9B](https://huggingface.co/black-forest-labs/FLUX.2-klein-9B)] / GGUF `unsloth/FLUX.2-klein-9B-GGUF`

### Z-Image Base
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ekkonwork/free-comfyui-colab-pack/blob/main/notebooks/zimage_base/comfy_zimage_base.ipynb)
- What: Z-Image base GGUF setup for quality-oriented generation.
- Model creators/sources: original Z-Image by `Tongyi-MAI` (`Tongyi-MAI/Z-Image`), GGUF ports by `unsloth`, ComfyUI split assets used from `Comfy-Org/z_image`.
- Workflow: `workflows/zimage_base/Text to Image (Z-Image-Base).json`
- Preview: ![Z-Image Base](https://huggingface.co/Tongyi-MAI/Z-Image/resolve/main/teaser.jpg) — Tongyi-MAI Z-Image [[HF Tongyi-MAI/Z-Image](https://huggingface.co/Tongyi-MAI/Z-Image)]

### Z-Image Turbo
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ekkonwork/free-comfyui-colab-pack/blob/main/notebooks/zimage_turbo/comfy_zimage_turbo.ipynb)
- What: fast Z-Image Turbo GGUF notebook for speed-first generation.
- Model creators/sources: original Z-Image Turbo by `Tongyi-MAI` (`Tongyi-MAI/Z-Image-Turbo`), GGUF ports by `unsloth`, ComfyUI split assets used from `Comfy-Org/z_image`.
- Workflows: `workflows/zimage_turbo/`
- Preview: ![Z-Image Turbo](https://huggingface.co/Tongyi-MAI/Z-Image-Turbo/resolve/main/assets/DMDR.webp) — Tongyi-MAI Z-Image-Turbo [[HF Tongyi-MAI/Z-Image-Turbo](https://huggingface.co/Tongyi-MAI/Z-Image-Turbo)]

### Z-Image Turbo + Base
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ekkonwork/free-comfyui-colab-pack/blob/main/notebooks/zimage_turbo_base/comfy_zimage_turbo_base.ipynb)
- What: combo notebook with Turbo + Base variants in one setup.
- Model creators/sources: original Z-Image models by `Tongyi-MAI` (`Tongyi-MAI/Z-Image` and `Tongyi-MAI/Z-Image-Turbo`), GGUF variants by `unsloth`, ComfyUI split assets used from `Comfy-Org/z_image`.
- Workflows: `workflows/zimage_turbo_base/`
- Preview: см. Z-Image Base + Turbo выше (оба варианта в одном ноутбуке)

### Z-Image Turbo + SeedVR2 Upscaler
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ekkonwork/free-comfyui-colab-pack/blob/main/notebooks/zimage_seedvr2/comfy_zimage_seedvr2.ipynb)
- What: two-stage pipeline (Z-Image generation + SeedVR2 upscaling).
- Model creators/sources: original Z-Image Turbo by `Tongyi-MAI` (`Tongyi-MAI/Z-Image-Turbo`) with GGUF ports by `unsloth`, SeedVR2 node/files by `numz` and GGUF pack by `cmeka`.
- Workflows: `workflows/zimage_seedvr2/`
- Preview: ![SeedVR2](https://huggingface.co/Tongyi-MAI/Z-Image-Turbo/resolve/main/assets/DMDR.webp) — SeedVR2 [[HF numz/SeedVR2-3B](https://huggingface.co/numz/SeedVR2-3B)] + Z-Image Turbo

### Qwen Image 2512
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ekkonwork/free-comfyui-colab-pack/blob/main/notebooks/qwen_image_2512/comfy_qwen_image_2512.ipynb)
- What: Qwen Image 2512 GGUF generation notebook with optional Lightning LoRA.
- Model creators/sources: Qwen family by Alibaba/Qwen team, GGUF packs by `unsloth` and `ggml-org`, Lightning LoRA by `lightx2v`.
- Workflows: `workflows/qwen_image_2512/`
- Preview: ![Qwen Image 2512](https://huggingface.co/circlestone-labs/Anima/resolve/main/montage.jpg) — Qwen Image [[HF Qwen/Qwen-Image](https://huggingface.co/Qwen/Qwen-Image)]

### Qwen Image Edit 2511
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ekkonwork/free-comfyui-colab-pack/blob/main/notebooks/qwen_image_edit_2511/comfy_qwen_image_edit_2511.ipynb)
- What: Qwen Image Edit 2511 notebook for image editing use cases.
- Model creators/sources: Qwen family by Alibaba/Qwen team, GGUF packs by `unsloth` and `ggml-org`, Lightning LoRA by `lightx2v`.
- Workflow: `workflows/qwen_image_edit_2511/Image Edit (Qwen 2511).json`
- Preview: ![Qwen Edit](https://huggingface.co/circlestone-labs/Anima/resolve/main/montage.jpg) — Qwen Image Edit [[HF Qwen/Qwen-Image-Edit](https://huggingface.co/Qwen/Qwen-Image-Edit)]

### Chroma1 HD GGUF
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ekkonwork/free-comfyui-colab-pack/blob/main/notebooks/chroma1_hd_gguf/comfy_chroma1_hd_gguf.ipynb)
- What: Chroma1-HD text-to-image GGUF notebook.
- Model creators/sources: Chroma1-HD by `lodestones`, GGUF package by `silveroxides`.
- Workflow: `workflows/chroma1_hd_gguf/ComfyUI_Chroma1-HD_T2I-workflow.json`
- Preview: ![Chroma1-HD](https://huggingface.co/lodestones/Chroma/resolve/main/ComfyUI_Chroma1-HD_T2I-overview.png) — Chroma1-HD [[HF lodestones/Chroma](https://huggingface.co/lodestones/Chroma)] / GGUF `silveroxides/Chroma1-HD-GGUF`

### Anima + WAI-Anima
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ekkonwork/free-comfyui-colab-pack/blob/main/notebooks/anima/comfy_anima_colab.ipynb)
- What: native Anima Aesthetic v1.1 and WAI-Anima v1.0 workflows for T2I, ControlNet and inpainting.
- Includes: ComfyUI-Manager, Anima-LLLite, ControlNet preprocessors, Lora Manager and the exact workflow variants from the v45 archive.
- Models: both Anima checkpoints are downloaded; the notebook writes WAI and Aesthetic workflow variants so either model can be selected.
- Workflow files are kept in the private companion repository and loaded by its separate loader notebook.
- Preview: ![Anima](https://huggingface.co/circlestone-labs/Anima/resolve/main/example.png) — Anima [[HF circlestone-labs/Anima](https://huggingface.co/circlestone-labs/Anima)] / Kirazuri v2 [[Civitai 2495369](https://civitai.com/models/2495369/kirazuri-anima)]


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
- Preview: ниже (Civitai превью, CC — линк на оригинал).

### Nova Anime XL IL v19.0 (Illustrious)
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ekkonwork/free-comfyui-colab-pack/blob/main/notebooks/nova_anime_xl_il_v190/comfy_nova_anime_xl_il_v190.ipynb)
- What: Nova Anime XL IL v19 — anime/2.5D/3D SDXL, серия из 20+ версий, Pony/Illustrious hybrid.
- Model creators/sources: Nova Anime team, Civitai `376130/2940478` [[Civitai 376130](https://civitai.com/models/376130/nova-anime-xl)].
- Workflow: CheckpointLoaderSimple.
- Preview: ![Nova Anime XL](https://image.civitai.com/xG1nkqKTMzGDvpLrqFT7WA/f0be436e-025f-4b93-89d1-f16b893fe197/width=320/130519332.jpeg) — [[Civitai Image 130519332](https://civitai.com/images/130519332)] by Crody

### JANKU v7.77 (Illustrious + RouWei)
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ekkonwork/free-comfyui-colab-pack/blob/main/notebooks/janku_v777/comfy_janku_v777.ipynb)
- What: JANKU v7.77 — Illustrious XL merge с Chenkin/NoobAI/RouWei, LoRA-free, улучшенная анатомия/NSFW, 1536 без upscale.
- Model creators/sources: JANKU (janxd), Civitai `1277670/2786084`, base `NoobAI-XL 1.0 License`.
- Workflow: CheckpointLoaderSimple, VAE baked in.
- Preview: ниже.

### Demo Gallery (внешние превью — не редистрибьюция, только линки с атрибуцией)

> **Авторские права:** все превью — собственность авторов моделей на Civitai/HuggingFace. Изображения здесь **не копируются** в репозиторий, а линкуются внешними URL с прямой ссылкой на источник. Лицензии: Anima — [CircleStone Labs Non-Commercial](https://huggingface.co/circlestone-labs/Anima/blob/main/LICENSE.md), RouWei — Illustrious, Nova — non-commercial без эдита, JANKU — [NoobAI-XL 1.0](https://huggingface.co/Laxhar/noobai-XL-1.0/blob/main/README.md#model-license). При генерации соблюдайте лицензии.

| Модель | Что умеет (из описания) | Превью (клик — источник) |
|---|---|---|
| **Anima Aesthetic v1.1**<br/>`kirazuri-anima` [[Civitai 2495369](https://civitai.com/models/2495369/kirazuri-anima)] | High-res 1536, aesthetic bias (`very aesthetic`), improved character/outfit separation, fix small details | [![Anima preview](https://image.civitai.com/xG1nkqKTMzGDvpLrqFT7WA/8b3ecb37-f3cd-4cc3-8214-497e33952024/width=320/136180088.jpeg)](https://civitai.com/models/2495369/kirazuri-anima) |
| **RouWei v0.8.0 epsilon**<br/>[[Civitai 950531](https://civitai.com/models/950531/rouwei)] | 50k артистов, лучший prompt adherence, без bleed, natural text + tags, `by artist` в отдельном CLIP чанке | [![RouWei preview](https://image.civitai.com/xG1nkqKTMzGDvpLrqFT7WA/1adb75a9-9bcb-4250-9e83-9ddb4a5abffa/width=320/81195856.jpeg)](https://civitai.com/models/950531/rouwei) |
| **Nova Anime XL v19**<br/>[Civitai 376130](https://civitai.com/models/376130/nova-anime-xl) | Anime/2.5D/3D, 20+ версий, Pony→Illustrious, 4k/aesthetic теги | [![Nova preview](https://image.civitai.com/xG1nkqKTMzGDvpLrqFT7WA/f0be436e-025f-4b93-89d1-f16b893fe197/width=320/130519332.jpeg)](https://civitai.com/images/130519332) |
| **JANKU v7.77**<br/>[[Civitai 1277670](https://civitai.com/models/1277670/janku-trained-chenkin-and-noobai-rouwei-illustrious-xl)] | LoRA-free, NSFW анатомия, 35k стилей `by artist`, 1536 без upscale | [![JANKU preview](https://image.civitai.com/xG1nkqKTMzGDvpLrqFT7WA/573cab67-bc20-4bdc-ae8d-d5caa1ba42d4/width=320/124686956.jpeg)](https://civitai.com/models/1277670/janku-trained-chenkin-and-noobai-rouwei-illustrious-xl) |

*Все превью — внешние hotlink с Civitai CDN (`image.civitai.com`), не хранятся в репо. При недоступности CDN открой ссылку на Civitai.*

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
