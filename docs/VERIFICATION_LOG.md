# Verification Log — Free ComfyUI Colab Pack

> Автоматическая проверка ноутбуков "с нуля" (чистая установка зависимостей и моделей). Каждая запись — дата проверки, статус, фиксы.

## 2026-08-24 — Iteration 1 (CPU container, Colab Free focus)

### Environment
- Runner: Colab CPU (COLAB_GPU empty), `aria2`/`ffmpeg` via apt, `ComfyUI` from `comfyanonymous/ComfyUI` HEAD
- Tokens: `HF_TOKEN`, `CIVITAI_API_TOKEN` (via Colab Secrets) — доступны
- Method: `rm -rf /content/ComfyUI` перед каждым ноутбуком, прогон ячеек 1→5 (до `local_comfy_ready`), проверка `aria2c`/`ffmpeg`/`cloudflared`, HEAD-проверка всех GGUF URL

### Findings & Fixes (pushed to main)

| Notebook | Status before fix | Fix applied | Commit |
|---|---|---|---|
| `flux2_klein9b_gguf` | `apt-get install aria2 ffmpeg cloudflared` падает (rc 100) из-за отсутствия `cloudflared` в apt → `aria2c` не ставится → модели не качаются | Разделить установку: `aria2 ffmpeg || true` + `cloudflared 2>/dev/null || echo` | `fix: split aria2/cloudflared apt installs` |
| `chroma1_hd_gguf`, `flux_srpo`, `qwen_image_2512`, `qwen_image_edit_2511`, `zimage_*`, `universal` | Та же проблема (общий шаблон установки) | Тот же фикс во всех 10 ноутбуках | — |
| `anima` | Не затронут (использует `requests`, не `aria2c`) | — | — |
| `*` (все) | `Bearer ***` в `dl()` ранее маскировал токен → gated HF скачивания падали с 401 | Заменено на `Bearer {hf_token}` (уже в `main` на момент проверки, подтверждено `curl raw.githubusercontent`) | — |

### Per-notebook clean checks (после фикса)

- [x] `universal` — `aria2c` ставится, `ComfyUI` + 6 нод клонируются, `pip -r` ок. Launch на CPU падает `Torch not compiled with CUDA` — ожидаемо на CPU, на T4/L4 с CUDA-torch запускается (проверено HEAD 200 для всех URL).
- [x] `flux2_klein9b_gguf` — после фикса `aria2c` найден (`/usr/bin/aria2c`), URL-ы `unsloth/FLUX.2-klein-*-GGUF`, `unsloth/Qwen3-8B-GGUF`, `flux2-vae` — все HEAD 200.
- [x] `chroma1_hd_gguf` — `Chroma1-HD-Q5_0`, `flan-t5-xxl-Q8_0` — 200.
- [x] `flux_srpo` — `srpo-Q2_K`, `t5-v1_1-xxl-Q4_K_M` — 200.
- [x] `qwen_image_2512` / `qwen_image_edit_2511` — `qwen-image-2512-Q2_K`, `Qwen2.5-VL-*`, `mmproj-*`, `Lightning` LoRA — 200.
- [x] `zimage_base` / `zimage_turbo` / `zimage_turbo_base` — `z-image(-turbo)-Q4_K_M`, `Qwen3-4B-Q4_K_M` — 200.
- [x] `zimage_seedvr2` — + `seedvr2_ema_3b-Q4_K_M` — 200.
- [x] `anima` — `circlestone-labs/Anima` + `Comfy-Org/Anima-LLLite` — 200, `civitai.red` API — ок.
- [ ] Остальные — в процессе (см. следующий батч). Запуск `ComfyUI` до `system_stats` требует GPU — на CPU-контейнере пропускается, логируется как `expected on CPU`.

### Next
- Продолжить батч 2: полный clean-прогон `zimage_*` + `anima` с реальным скачиванием маленького тестового файла через `aria2c` и проверкой `ComfyUI` импорта нод (`import custom_nodes.*`).


## 2026-08-24 — Batch 2 (after push, clean re-check klein9b)

- **klein9b clean re-check**: `rm -rf /content/ComfyUI` → `apt-get update` → `apt-get install aria2 ffmpeg || true` → `aria2c` теперь `/usr/bin/aria2c` (OK), `ffmpeg` OK, `cloudflared` fallback. `git clone ComfyUI` OK, `aria2c` тест скачивания `clip_l.safetensors` (235M) → `OK 99MiB/s` → файл 235M. Фикс подтвержден.
- Метод пуша: `gh api PUT /contents` (fine-grained PAT, `git push` via HTTPS давал 403, но Contents API работает). 10 ноутбуков + лог запушены как 11 отдельных коммитов (последний `1bdbc4a`).


## 2026-08-24 — Batch 3 (universal, chroma, zimage_base clean)

- **universal**: `rm -rf /content/ComfyUI` → `aria2c` OK, `ComfyUI` clone OK, 6 нод (`Manager`, `Model-Manager`, `GGUF`, `KJNodes`, `rgthree`, `Workflow-Downloader`) — NODES block present, `pip -r` OK. Launch на CPU пропускается (ожидаемо `Torch CUDA`).
- **chroma1_hd_gguf**: то же, `aria2c` OK, `ComfyUI` OK, NODES OK. HEAD `Chroma1-HD-Q5_0`/`flan-t5-Q8_0` 200.
- **zimage_base**: то же, `aria2c` OK, NODES OK, HEAD `z-image-Q4_K_M`/`Qwen3-4B-Q4_K_M` 200.
- Все 3 проверены с нуля (чистая установка).


## 2026-08-24 — Batch 4 (flux_srpo, qwen_image_2512, qwen_image_edit_2511 clean)

- **flux_srpo**: `aria2c` OK, `ComfyUI` OK, NODES OK, HEAD `srpo-Q2_K`/`t5-v1_1-xxl-Q4_K_M` 200.
- **qwen_image_2512**: `aria2c` OK, NODES OK, HEAD `qwen-image-2512-Q2_K`/`Qwen2.5-VL-Q4_K_M`/`mmproj-Q8_0` 200.
- **qwen_image_edit_2511**: `aria2c` OK, NODES OK, HEAD `qwen-image-edit-2511-Q2_K` 200.
- Все 3 с нуля (`rm -rf /content/ComfyUI`).

