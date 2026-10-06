from PIL import Image, ImageDraw, ImageFont
import os

os.makedirs("previews/anima_illustrious_compare", exist_ok=True)

# 1. Preview 01: RouWei vs Nova Anime XL
rw1 = Image.open("previews/rouwei_v080_epsilon/preview_01_1024.png").convert("RGB")
nova1 = Image.open("previews/nova_anime_xl_il_v190/preview_01_1024.png").convert("RGB")

comp1 = Image.new("RGB", (1024, 1024))
# Left half: center crop of RouWei
crop_rw = rw1.crop((256, 0, 768, 1024))
# Right half: center crop of Nova
crop_nova = nova1.crop((256, 0, 768, 1024))
comp1.paste(crop_rw, (0, 0))
comp1.paste(crop_nova, (512, 0))

draw1 = ImageDraw.Draw(comp1)
# Vertical dividing line
draw1.line([(512, 0), (512, 1024)], fill=(255, 255, 255), width=3)
# Subtitle badges
draw1.rectangle([(30, 960), (220, 1000)], fill=(0, 0, 0, 180))
draw1.text((45, 968), "RouWei v0.80", fill=(255, 255, 255))
draw1.rectangle([(542, 960), (760, 1000)], fill=(0, 0, 0, 180))
draw1.text((557, 968), "Nova Anime XL", fill=(255, 255, 255))

comp1.save("previews/anima_illustrious_compare/preview_01_1024.png", "PNG", quality=95)
print("Saved anima_illustrious_compare preview_01_1024.png")

# 2. Preview 02: JANKU vs Nova Anime XL
janku1 = Image.open("previews/janku_v777/preview_01_1024.png").convert("RGB")
nova2 = Image.open("previews/nova_anime_xl_il_v190/preview_02_1024.png").convert("RGB")

comp2 = Image.new("RGB", (1024, 1024))
crop_janku = janku1.crop((256, 0, 768, 1024))
crop_nova2 = nova2.crop((256, 0, 768, 1024))
comp2.paste(crop_janku, (0, 0))
comp2.paste(crop_nova2, (512, 0))

draw2 = ImageDraw.Draw(comp2)
draw2.line([(512, 0), (512, 1024)], fill=(255, 255, 255), width=3)
draw2.rectangle([(30, 960), (200, 1000)], fill=(0, 0, 0, 180))
draw2.text((45, 968), "JANKU v7.77", fill=(255, 255, 255))
draw2.rectangle([(542, 960), (760, 1000)], fill=(0, 0, 0, 180))
draw2.text((557, 968), "Nova Anime XL", fill=(255, 255, 255))

comp2.save("previews/anima_illustrious_compare/preview_02_1024.png", "PNG", quality=95)
print("Saved anima_illustrious_compare preview_02_1024.png")
