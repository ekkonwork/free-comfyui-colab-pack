import re
from pathlib import Path

readme_path = Path("README.md")
content = readme_path.read_text(encoding="utf-8")

# Mapping of section header patterns to preview folder and title
mapping = [
    ("### Flux SRPO", "flux_srpo", "Flux SRPO"),
    ("### Flux2 Klein 9B GGUF", "flux2_klein9b_gguf", "Flux2 Klein 9B"),
    ("### Z-Image Base", "zimage_base", "Z-Image Base"),
    ("### Z-Image Turbo\n", "zimage_turbo", "Z-Image Turbo"),
    ("### Z-Image Turbo + Base", "zimage_turbo_base", "Z-Image Turbo + Base"),
    ("### Z-Image Turbo notebook (SeedVR2 excluded from bundled flow)", "zimage_seedvr2", "Z-Image SeedVR2"),
    ("### Qwen Image 2512", "qwen_image_2512", "Qwen Image 2512"),
    ("### Qwen Image Edit 2511", "qwen_image_edit_2511", "Qwen Image Edit 2511"),
    ("### Chroma1 HD GGUF", "chroma1_hd_gguf", "Chroma1 HD"),
    ("### Anima + WAI-Anima", "anima", "Anima"),
    ("### Anima Illustrious Compare (Anima + 3 Illustrious)", "anima_illustrious_compare", "Anima Compare"),
    ("### RouWei v0.8.0 epsilon (Illustrious)", "rouwei_v080_epsilon", "RouWei v0.8.0 epsilon"),
    ("### Nova Anime XL IL v19.0 (Illustrious)", "nova_anime_xl_il_v190", "Nova Anime XL"),
    ("### JANKU v7.77 (Illustrious + RouWei)", "janku_v777", "JANKU v7.77"),
]

# 1. Remove the bottom Preview Gallery section
gallery_idx = content.find("## Preview Gallery")
if gallery_idx != -1:
    content = content[:gallery_idx].rstrip() + "\n"

# 2. In each section, inject the 2-column square preview table under the Colab badge line
for header, folder, title in mapping:
    # Find header
    idx = content.find(header)
    if idx == -1:
        print(f"Warning: header not found: {header}")
        continue
    # Find badge line start
    badge_start = content.find("[![Open In Colab]", idx)
    if badge_start == -1 or badge_start > idx + 200:
        print(f"Warning: badge not found for {header}")
        continue
    # Find end of that badge line
    line_end = content.find("\n", badge_start)
    if line_end == -1:
        line_end = len(content)
    
    table = f"\n\n| Preview 01 (1024×1024) | Preview 02 (1024×1024) |\n|:---:|:---:|\n| ![{title} 01](previews/{folder}/preview_01_1024.png) | ![{title} 02](previews/{folder}/preview_02_1024.png) |"
    
    # Check if table already inserted
    snippet_after = content[line_end:line_end+150]
    if f"previews/{folder}" not in snippet_after:
        content = content[:line_end] + table + content[line_end:]

readme_path.write_text(content, encoding="utf-8")
print("README.md updated successfully.")
