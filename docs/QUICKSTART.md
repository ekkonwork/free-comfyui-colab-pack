# Quick Start

## Requirements
- Google Colab (Free T4 recommended)
- Hugging Face account/token
- Civitai API token (recommended for LoRA downloads)

## Run Steps
1. Pick a model notebook in `notebooks/<model>/`.
2. Upload/open it in Colab.
3. Run installation cell.
4. Enter HF token.
5. Enter Civitai token (if available).
6. Run model download cell.
7. Run launch cell and open the generated Cloudflare URL.
8. Import workflow JSON from `workflows/<model>/`.

## Tips
- If tunnel URL is not reachable, rerun only launch cell.
- Keep default quant settings unless you know your VRAM headroom.
- Use lower resolution first for faster first test.
