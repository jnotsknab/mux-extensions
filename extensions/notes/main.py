import sys, json
sys.stdout.reconfigure(encoding="utf-8")
def send(o): print(json.dumps(o), flush=True)
def log(t): print(t, file=sys.stderr, flush=True)
notes = ["buy milk", "ship it"]
n = 0
def view():
    return {"type": "box", "gap": 1, "children": [
        {"type": "text", "text": f"{len(notes)} notes", "bold": True, "color": "accent"},
        {"type": "input", "key": "new", "placeholder": "add a note"},
        {"type": "list", "key": "notes", "items": [{"value": str(i), "label": t, "detail": f"#{i}"} for i, t in enumerate(notes)]},
        {"type": "box", "dir": "row", "gap": 2, "children": [
            {"type": "button", "key": "clear", "label": "Clear", "hotkey": "c"},
            {"type": "progress", "value": min(1, len(notes) / 5), "label": "of 5"}]},
        {"type": "markdown", "text": "**bold** and `code`"},
        {"type": "code", "text": "<script>alert(1)</script>"}]}
def req(method, params):
    global n; n += 1
    send({"jsonrpc": "2.0", "id": f"r{n}", "method": method, "params": params})
for line in sys.stdin:
    msg = json.loads(line); m = msg.get("method"); p = msg.get("params") or {}
    if "id" in msg and m is None:
        log("reply " + json.dumps(msg)); continue
    if m == "initialize":
        pass
    elif m == "ui/event":
        log("event " + json.dumps(p))
        if p.get("type") == "submit" and p.get("value"): notes.append(p["value"]); req("ui/update", {"id": "main", "view": view()})
        elif p.get("type") == "press" and p.get("key") == "clear": notes.clear(); req("ui/update", {"id": "main", "view": view()})
        elif p.get("type") == "select": req("ui/toast", {"text": "picked " + notes[int(p["value"])]})
    elif m == "command/run":
        req("ui/open", {"id": "main", "title": "Notes", "view": view()})
        send({"jsonrpc": "2.0", "id": msg["id"], "result": {}})
