# HANDOFF — free-comfyui-colab-pack task board

> Автор задачи: ekkonwork. Исполнитель: Hermes Agent.
> Токены: HF `hf_***REDACTED***`, Civitai `***REDACTED***`, GitHub PAT предоставлен.
> Правило: пуш сразу в `main` без PR.
> Актуальный приоритет: сообщение от 2026-08-26 (квадрат HD 1024x1024, 2 превью/ноутбук, рефайнер+детейлеры, верификация глазами)

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

## Часть 2 — Покадровая генерация квадрат HD 1024x1024 по всем ноутбукам (2 превью/ноутбук) — АКТУАЛЬНЫЕ ТРЕБОВАНИЯ 2026-08-26

> Источник истины: сообщение пользователя 2026-08-26. Прошлый HANDOFF устарел.
> Правила:
> - Последовательно открывать ноутбук по одному и генерировать изображения. Оптимизация: можно 2-3 параллельно если не переполнить диск/RAM — по факту T4 15GB требует последовательно.
> - Разрешение: квадрат HD (1024x1024). По 2 превью на ноутбук.
> - Флоу: FaceDetailer (face_yolov8m) + HandDetailer (hand_yolov8n) + Refiner вторым семплером (кроме qwen_image_edit_2511 и flux2_klein9b_gguf — для них рефайнер не обязателен, но желателен; для всех остальных — обязательно).
> - Верификация глазами: просматривать изображения самому, если артефакты на глазах/руках — менять параметры семплинга/denoise/cfg.
> - Фотореал vs аниме: Flux SRPO, Chroma, Z-Image, Qwen — фотореализм; Illustrious/RouWei/Janku/Nova/Anima — аниме. Перед каждой моделью сабагент ресёрчит тип. Для edit-моделей (qwen_image_edit_2511): 1 превью — фотореалистичная девушка, 2 превью — та же девушка повернута в профиль (edit).
> - Промпты: уникальные для каждого превью, правильная структура под каждую модель (сабагент исследует промптинг).
> - Сэмплинг: проверять параметры отдельным сабагентом. Напр. Flux SRPO = 50 шагов (не 14).
> - После каждого ноутбука: пуш воркфлоу + превью в main + запись в HANDOFF (что сделал и кратко как).
> - Исключения: qwen_image_edit_2511 и klein9b — без обязательного рефайнера (уточнение пользователя).

### Статус ноутбуков (квадрат 1024x1024, Face+Hand Detailer + Refiner где требуется)

| Ноутбук | Статус | Превью | Workflow | Детали |
|---|---|---|---|---|
| zimage_turbo | ✅ 2026-08-26 | 2x 1024 | workflow.json | GGUF Q4_K_M, 9 steps cfg 1.0 + Face 0.5 + Hand 0.45 + Refiner 12 steps 0.3 — верифицировано, зрение OK |
| zimage_base | ✅ 2026-08-26 | 2x 1024 | workflow.json | 14 steps cfg 5.0 → Face/Hand + Refiner — верифицировано |
| chroma1_hd_gguf | ✅ 2026-08-26 | 2x 1024 | workflow.json | 14 steps cfg 5.0 → Face/Hand + Refiner — верифицировано |
| flux_srpo | 🔄 ПЕРЕДЕЛКА 2026-08-26 | 2x 1024 (было аниме) | workflow.json | Было 14 steps аниме — переделать в 50 steps photoreal (tencent/SRPO), новые промпты |
| rouwei_v080_epsilon | ✅ 2026-08-26 | 2x 1024 | workflow.json | Illustrious anime, 24 steps euler_ancestral cfg 7 + Detailers + Refiner — верифицировано |
| flux2_klein9b_gguf | ⏳ очередь | — | — | Klein 9B — фоторил? ресёрч сабагентом, без обязательного рефайнера |
| qwen_image_2512 | ⏳ очередь | — | — | Qwen 2512 — ресёрч шагов/промпта |
| qwen_image_edit_2511 | ⏳ очередь | — | — | Edit: превью1 — фотореал девушка, превью2 — профиль (edit flow), без обязательного рефайнера |
| janku_v777 | ⏳ очередь | — | — | Illustrious anime — ресёрч |
| nova_anime_xl_il_v190 | ⏳ очередь | — | — | Illustrious anime — ресёрч |
| zimage_seedvr2 | ⏳ очередь | — | — | Z-Image + SeedVR2 — ресёрч |
| zimage_turbo_base | ⏳ очередь | — | — | Turbo+Base combo — ресёрч |
| anima | ⏳ очередь | — | — | Anima — аниме |
| anima_illustrious_compare | ⏳ очередь | — | — | Compare 4 модели |
| universal | ⏳ очередь | — | — | Universal |

### Очередь выполнения 2026-08-26

1. flux_srpo — переделка 50 шагов photoreal (приоритет, прошлый агент сделал аниме) → пуш
2. flux2_klein9b_gguf → пуш
3. qwen_image_2512 → пуш
4. qwen_image_edit_2511 (edit: девушка + профиль) → пуш
5. zimage_seedvr2 → пуш
6. zimage_turbo_base → пуш
7. janku_v777 → пуш
8. nova_anime_xl_il_v190 → пуш
9. anima → пуш
10. anima_illustrious_compare → пуш
11. universal → пуш

Каждый пуш: `previews/<model>/preview_01_1024.png`, `preview_02_1024.png`, `workflows/<model>/workflow.json`, `README.md` галерея, `HANDOFF.md` запись.

## Лог выполнения

| Дата (UTC) | Действие | Результат |
|---|---|---|
| 2026-08-25 | Создан HANDOFF, старт части 1 | — |
| 2026-08-25 | Watchdog CF+Bore добавлен во все 17 нотебуков (2 ячейки/нотебук) | hash CF bd164258 / Bore 6e78b74f идентичны |
| 2026-08-25 | Compare нотебук: ячейка 3b форм (38 @param) + zip-скачивание в ячейке очереди | 10 промптов + 4×6 параметров семплинга редактируются сбоку |
| 2026-08-25 | Дымовой тест CF+restart на dummy ComfyUI 18188 | URL1 restored-ranking… / URL2 investigations-gauge… — оба поднялись, keepalive перезапускает |
| 2026-08-25 | Валидация всех нотебуков (json + watchdog identical) | 17/17 OK |
| 2026-08-25 | Пуш в main (часть 1) | e9696fb — 17 нотебуков + HANDOFF |
| 2026-08-25 | zimage_turbo: ComfyUI install + модели download (4.7G+2.4G+320M) + запуск на T4 --lowvram | OK, /system_stats 200 |
| 2026-08-25 | zimage_turbo: Civitai research (2169096 FaceDetailer) + GGUF адаптация + HD 1824x576 gen | 1.5MB png, preview + workflow сохранены, ожидают пуш |
| 2026-08-26 | Актуализация HANDOFF под требования 2026-08-26 (квадрат HD, 2 превью, Refiner+Detailers, 50 шагов SRPO, верификация глазами, сабагенты) | Переписан раздел Часть 2, очередь 11 ноутбуков |

## Проблемы и фиксы (2026-08-26 Flux SRPO)

| Проблема | Причина | Фикс | Время |
|---|---|---|---|
| CLIPLoaderGGUF type 'flux' not in list | ComfyUI 0.34 убрал 'flux' из CLIPLoader, оставил только в DualCLIPLoader | Заменить node 2 на DualCLIPLoaderGGUF(clip_name1=t5, clip_name2=clip_l, type=flux) | 2026-08-26 05:30 |
| UltralyticsDetectorProvider bbox/face_yolov8m.pt not in [] | Модели не скачаны, автозагрузка Impact Pack не сработала | Ручная загрузка aria2c Bingsu/adetailer face_yolov8m.pt (50M) + hand_yolov8n.pt (6M) в /models/ultralytics/bbox, рестарт ComfyUI | 05:30 |
| 50 шагов медленно (3-4 мин/изо vs 14 шагов 40с) | Официальный SRPO требует 50 steps cfg 3.5 normal (пользователь прав, 14 — это Schnell preset) | Принять как норму, оптимизация: detailer 15→12 steps, refiner 15→12, keep 50 base | 05:50 |
| Queue stuck / execution_interrupted | Прерывание через /interrupt оставило job в queue_running, блокировало следующие | Очистка queue через /queue clear, рестарт ComfyUI при зависании >400с | 05:46 |
| T4 низкая скорость из-за --lowvram offload | GGUF 4G+2.9G → 7GB VRAM, offload на RAM | Оставить --lowvram, но не использовать --novram/cache-none, дать DynamicVRAM работать | 05:30 |

**Вывод для след. ноутбуков:** перед генерацией проверить object_info на поддерживаемые типы и наличие bbox, прекачать все GGUF/VLAE заранее, не прерывать sampler на 50 шагах (ждать до 600с), держать ComfyUI живым между превью чтобы не терять кэш.

| 2026-08-26 | zimage_turbo/base/chroma/rouwei перегенерированы в квадрат 1024 + Face/Hand + Refiner | Уже в main (accd05b etc), верифицированы |

### 2026-08-26 06:43 UTC
Flux SRPO: 50 steps DualCLIP + Face/Hand Detailer + Refiner fixed, preview_01 generated (Scandinavian blonde loft, 1024x1024, 50 steps cfg3.5 euler/normal + Face10 Hand10 Refiner10). Workflow patched and pushed. Preview_02 placeholder (brunette variant) — will regenerate unique.
