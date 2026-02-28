# Troubleshooting

## Cloudflare URL opens with ERR_CONNECTION_CLOSED
- Wait until launch cell prints final `YOUR LINK` line.
- If still failing, rerun launch cell once.
- Try a clean Colab runtime restart if tunnel repeatedly drops.

## LoRA download fails (403/unauthorized)
- Set `CIVITAI_API_TOKEN` in the token prompt.
- Re-run model download cell.

## Out of memory (VRAM/RAM)
- Keep default quant settings.
- Lower output resolution.
- Close other tabs/sessions in Colab.

## Missing model in ComfyUI
- Re-run download cell.
- Verify file exists in expected ComfyUI model subfolder.

## Slow first run
- First startup installs dependencies and caches packages.
- Subsequent runs are usually faster in same session.
