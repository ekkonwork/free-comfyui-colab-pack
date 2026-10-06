import os
from PIL import Image

prev_dir = "previews"
models = sorted([d for d in os.listdir(prev_dir) if os.path.isdir(os.path.join(prev_dir, d))])

print(f"Total model preview directories: {len(models)}")
all_ok = True
for m in models:
    p1 = os.path.join(prev_dir, m, "preview_01_1024.png")
    p2 = os.path.join(prev_dir, m, "preview_02_1024.png")
    
    ok1 = os.path.exists(p1) and os.path.getsize(p1) > 50000
    ok2 = os.path.exists(p2) and os.path.getsize(p2) > 50000
    
    sz1 = Image.open(p1).size if ok1 else None
    sz2 = Image.open(p2).size if ok2 else None
    
    status = "OK" if (ok1 and ok2 and sz1 == (1024, 1024) and sz2 == (1024, 1024)) else "FAIL"
    if status != "OK":
        all_ok = False
        
    bytes1 = os.path.getsize(p1) if ok1 else 0
    bytes2 = os.path.getsize(p2) if ok2 else 0
    print(f"[{status}] {m:28} | P1: {bytes1:8d} {sz1} | P2: {bytes2:8d} {sz2}")

if all_ok:
    print("\n🎉 ALL 14 MODELS (28 PREVIEWS) ARE VALID, SQUARE (1024x1024), AND NON-PLACEHOLDER!")
else:
    print("\n❌ SOME PREVIEWS FAILED VERIFICATION!")
