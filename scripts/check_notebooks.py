import json, pathlib, ast, sys
ok=True
for p in pathlib.Path("notebooks").rglob("*.ipynb"):
    if "_paused" in str(p): continue
    data=json.loads(p.read_text(encoding="utf-8"))
    txt="".join("".join(c["source"]) for c in data["cells"])
    if "Bearer ***" in txt or "Bearer ***" in p.read_text(encoding="utf-8"):
        print(f"FAIL {p}: Bearer *** found")
        ok=False
    for c in data["cells"]:
        if c["cell_type"]!="code": continue
        src="".join(c["source"])
        # Replace Colab magics (!, %) with 'pass' preserving indentation,
        # so that if/else blocks containing only magics remain syntactically valid.
        cleaned_lines = []
        for l in src.splitlines():
            stripped = l.strip()
            if stripped.startswith(("!", "%")):
                indent = l[:len(l)-len(l.lstrip())]
                cleaned_lines.append(f"{indent}pass  # {stripped[:80]}")
            else:
                cleaned_lines.append(l)
        clean = "\n".join(cleaned_lines)
        try: ast.parse(clean)
        except SyntaxError as e:
            print(f"SYNTAX {p} {e}")
            ok=False
sys.exit(0 if ok else 1)
