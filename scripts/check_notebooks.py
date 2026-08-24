import json, pathlib, ast, sys
ok=True
for p in pathlib.Path("notebooks").rglob("*.ipynb"):
    if "_paused" in str(p): continue
    data=json.loads(p.read_text())
    txt="".join("".join(c["source"]) for c in data["cells"])
    if "Bearer ***" in txt or "Bearer ***" in p.read_text():
        print(f"FAIL {p}: Bearer *** found")
        ok=False
    for c in data["cells"]:
        if c["cell_type"]!="code": continue
        src="".join(c["source"])
        clean="\n".join(l for l in src.splitlines() if not l.strip().startswith(("!","%")))
        try: ast.parse(clean)
        except SyntaxError as e:
            print(f"SYNTAX {p} {e}")
            ok=False
sys.exit(0 if ok else 1)
