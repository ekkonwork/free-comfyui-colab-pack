# Bundled workflow sources

Each active notebook has exactly one selectable file at `workflows/<model>/workflow.json`.
The notebook installs that file into `/content/ComfyUI/user/default/workflows/` after model download and rewrites model names to the quant files actually selected at runtime.

| Folder | Primary workflow source | Local adaptation |
|---|---|---|
| `flux_srpo` | [Tencent SRPO](https://huggingface.co/tencent/SRPO/blob/main/comfyui/SRPO-workflow.json) | FLUX UNET and T5 loaders changed to ComfyUI-GGUF |
| `chroma1_hd_gguf` | [Lodestones Chroma1-HD](https://huggingface.co/lodestones/Chroma/blob/main/ComfyUI_Chroma1-HD_T2I-workflow.json) | Chroma UNET and FLAN-T5 loaders changed to ComfyUI-GGUF |
| `flux2_klein9b_gguf` | [Comfy-Org Flux.2 Klein 9B](https://github.com/Comfy-Org/workflow_templates/blob/main/templates/image_flux2_text_to_image_9b.json) | UNET and Qwen3 loaders changed to ComfyUI-GGUF |
| `qwen_image_2512` | [Comfy-Org Qwen Image 2512](https://github.com/Comfy-Org/workflow_templates/blob/main/templates/image_qwen_Image_2512.json) | UNET and Qwen2.5-VL loaders changed to ComfyUI-GGUF; runtime LoRA filename synchronized |
| `qwen_image_edit_2511` | [Comfy-Org Qwen Image Edit 2511](https://github.com/Comfy-Org/workflow_templates/blob/main/templates/image_qwen_image_edit_2511.json) | UNET and Qwen2.5-VL loaders changed to ComfyUI-GGUF; runtime LoRA filename synchronized |
| `zimage_base` | [Comfy-Org Z-Image Base](https://github.com/Comfy-Org/workflow_templates/blob/main/templates/image_z_image.json) | UNET and Qwen3 loaders changed to ComfyUI-GGUF |
| `zimage_turbo` | [Comfy-Org Z-Image Turbo](https://github.com/Comfy-Org/workflow_templates/blob/main/templates/image_z_image_turbo.json) | UNET and Qwen3 loaders changed to ComfyUI-GGUF |
| `zimage_turbo_base` | Same two Comfy-Org Z-Image templates | Both branches share one canvas/file; each keeps its own sampler path |
| `zimage_seedvr2` | Comfy-Org Z-Image Turbo template | Clean Z-Image Turbo only; SeedVR2 is explicitly absent by user request |
| `anima` | [Comfy-Org Anima Base](https://github.com/Comfy-Org/workflow_templates/blob/main/templates/image_anima_base_v1.json) | Model filename aligned with the notebook download |
| `anima_illustrious_compare` | Comfy-Org Anima graph plus the three SDXL adaptations below | Four exact independent branches on one canvas; no unrelated author-comparison branches or grid custom node |
| `janku_v777`, `nova_anime_xl_il_v190`, `rouwei_v080_epsilon` | [Impact Pack FaceDetailer example](https://github.com/ltdrdata/ComfyUI-Impact-Pack/blob/Main/example_workflows/1-FaceDetailer.json) plus the Comfy-Org SDXL refiner example | Exact checkpoint + base sampler + second sampler/refiner + face detector/detailer + hand detector/detailer |

There are no separately published author JSON files for the exact JANKU v7.77, Nova Anime XL IL v19, or RouWei v0.8 epsilon versions. Their bundled graphs are therefore labeled adaptations of primary ComfyUI/Impact examples, not official model-author workflows.
