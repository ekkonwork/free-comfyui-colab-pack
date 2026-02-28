# Core Features

## 1) Auto Quant by VRAM
Notebooks estimate VRAM budget and auto-pick GGUF quant defaults to fit Colab T4 constraints.

## 2) GGUF-First Strategy
Model choices focus on GGUF variants to reduce VRAM pressure and keep generation practical on free tiers.

## 3) Match-Only Lenovo LoRA Download
Lenovo UltraReal LoRAs are filtered by current base-model tags. Only matching LoRA files are downloaded.

## 4) Token UX
Both HF and Civitai token prompts are integrated in setup cells.

## 5) Stable Tunnel Logic
Launch cells include Cloudflare tunnel retries and readiness checks before link output.

## 6) Low-VRAM Defaults
Notebook defaults are tuned for memory-limited sessions and practical first generation success.

## 7) Workflows Included
Each model has workflow JSON files in `workflows/<model>/` aligned with its notebook.
