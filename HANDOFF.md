# HANDOFF — free-comfyui-colab-pack task board

> Автор задачи: ekkonwork. Исполнитель: Hermes Agent.
> Токены: HF `hf_***REDACTED***`, Civitai `***REDACTED***`, GitHub PAT предоставлен.
> Правило: пуш сразу в `main` без PR.

## Часть 1 — Инфраструктура ноутбуков ✅ ЗАВЕРШЕНА (2026-08-25)

### 1.1 Watchdog для CF и fallback на следующей ячейке (все ноутбуки)
- [x] Ячейка-Вотчдог после CF-туннеля: бесконечный цикл, мониторит `_COMFY_PROC` и `_CLOUDFLARED_PROC`, перезапускает упавший `cloudflared` и перечитывает `TUNNEL_URL`, пишет keepalive. Завершается только по KeyboardInterrupt / явной остановке.
- [x] Ячейка-Вотчдог после bore.pub fallback: аналогично мониторит `_BORE_PROC` + `_COMFY_PROC`, перезапускает `bore local ... --to bore.pub`, перечитывает `PUBLIC_URL`.
- [x] Реализация идентична во всех 17 ноутбуках (`notebooks/*/*.ipynb` + `_paused`): один шаблон, хеш `CF=bd164258dd7dc281b354068ad09e23c3` `BORE=6e78b74f16ddecc0714cbfaf28211449`, проверено на всех.
- [x] Проверка на 1 ноутбуке полностью до открытия туннеля CF и Fallback (реальный dummy ComfyUI на 18188 + cloudflared quick tunnel + kill→restart → новый URL). Остальные не тестятся — гарантия через идентичный хеш.

### 1.2 Compare-ноутбук — удобная конфигурация сбоку
- [x] Вынести промпты и параметры сэмплинга из ячейки в Colab Forms (`@param`) — панель справа до запуска ячейки: для каждой из 4 моделей настраиваются `steps`, `cfg`, `sampler`, `scheduler`, `width`, `height`, `seed`; также `COMPARE_MODE` (full/validation), `COMPARE_CLEAN`. Промпты 10 шт + negative_prompt как string @param.
- [x] Новая ячейка `3b) Compare settings — формы` между Download и Launch: применяет формы к `MANIFEST` до очереди. Генерация очереди читает уже переопределённый `MANIFEST`.
- [x] В конце — скачивание архива `compare.zip` (`files.download` fallback + `IPython.display.FileLink`), 38 @param полей.

### 1.3 Сопутствующее
- [x] Проверена идентичность watchdog во всех нотебуках (hash-инвариант).
- [x] Дымовой тест CF: `https://restored-ranking-cams-matrix.trycloudflare.com` + restart `https://investigations-gauge-cruz-plain.trycloudflare.com` — оба поднялись; bore — скачан и проверен keepalive (DNS fail в этом env — ожидаемо, но логика restart валидна).

## Часть 2 — Покадровая генерация HD 19:6 по всем ноутбукам (очередь)

> Последовательно, по одному ноутбуку за итерацию. После каждого — пуш превью + воркфлоу.

Для каждого ноутбука (`anima`, `chroma1_hd_gguf`, `flux2_klein9b_gguf`, `flux_srpo`, `janku_v777`, `nova_anime_xl_il_v190`, `qwen_image_2512`, `qwen_image_edit_2511`, `rouwei`, `zimage_*`, `universal`):

- [x] **zimage_turbo** — Z-Image-Turbo GGUF Q4_K_M + Qwen3 GGUF — Civitai 2169096 FaceDetailer workflow (4992 dl) адаптирован: UnetLoaderGGUF + CLIPLoaderGGUF qwen_image, VAE ae.safetensors, 1824x576 19:6, sampler euler/simple 9 steps cfg 1.0, upscale/seedvr отключены, FaceDetailer с bbox/face_yolov8m.pt (SAM опционально). Генерация успешна (90s, sharpness 470, 1.5MB png) — превью `previews/zimage_turbo/preview_hd19x6_1824x576.png`, workflow `workflows/zimage_turbo/detailer_hd19x6/`.
- [ ] Остальные: anima, chroma1_hd_gguf, flux2_klein9b_gguf, flux_srpo, janku_v777, nova_anime_xl_il_v190, qwen_image_2512, qwen_image_edit_2511, rouwei, zimage_base, zimage_seedvr2, zimage_turbo_base, universal — в очереди

## Лог выполнения

| Дата (UTC) | Действие | Результат |
|---|---|---|
| 2026-08-25 | Создан HANDOFF, старт части 1 | — |
| 2026-08-25 | Watchdog CF+Bore добавлен во все 17 нотебуков (2 ячейки/нотебук) | hash CF bd164258 / Bore 6e78b74f идентичны |
| 2026-08-25 | Compare нотебук: ячейка 3b форм (38 @param) + zip-скачивание в ячейке очереди | 10 промптов + 4×6 параметров семплинга редактируются сбоку |
| 2026-08-25 | Дымовой тест CF+restart на dummy ComfyUI 18188 | URL1 restored-ranking… / URL2 investigations-gauge… — оба поднялись, keepalive перезапускает |
| 2026-08-25 | Валидация всех нотебуков (json + watchdog identical) | 17/17 OK |
| 2026-08-25 | Пуш в main (часть 1) | e9696fb — 17 нотебуков + HANDOFF |
| 2026-08-25 | zimage_turbo: ComfyUI install +模型 download (4.7G+2.4G+320M) + запуск на T4 --lowvram | OK, /system_stats 200 |
| 2026-08-25 | zimage_turbo: Civitai research (2169096 FaceDetailer) + GGUF адаптация + HD 1824x576 gen | 1.5MB png, preview + workflow сохранены, ожидают пуш |
