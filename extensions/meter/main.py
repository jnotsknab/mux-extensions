import sys, json, threading, time
sys.stdout.reconfigure(encoding="utf-8")
lock = threading.Lock()
def send(o):
    with lock: print(json.dumps(o), flush=True)
def log(t): print(t, file=sys.stderr, flush=True)
tools, ticks, clicks, place, n = 0, 0, 0, "side", 0
def view():
    return {"type": "box", "gap": 1, "children": [
        {"type": "text", "text": f"tools {tools}  ticks {ticks}  clicks {clicks}", "bold": True, "color": "accent"},
        {"type": "progress", "value": (ticks % 20) / 20, "label": "heartbeat"},
        {"type": "button", "key": "hit", "label": "Hit me", "hotkey": "h"},
        {"type": "input", "key": "say", "placeholder": "say something"}]}
def req(method, params):
    global n; n += 1
    send({"jsonrpc": "2.0", "id": f"r{n}", "method": method, "params": params})
opened = False
def ticker():
    global ticks
    while True:
        time.sleep(1); ticks += 1
        if opened: req("ui/update", {"id": "m", "view": view()})
threading.Thread(target=ticker, daemon=True).start()
for line in sys.stdin:
    msg = json.loads(line); m = msg.get("method"); p = msg.get("params") or {}
    if "id" in msg and m is None:
        if "error" in msg: log("err " + json.dumps(msg))
        continue
    if m == "event":
        if p.get("event") == "tool_call": tools += 1
    elif m == "ui/event":
        log("event " + json.dumps(p))
        if p.get("type") == "press": clicks += 1
        elif p.get("type") == "submit": req("ui/toast", {"text": "said " + str(p.get("value"))})
        elif p.get("type") == "close": opened = False
    elif m == "command/run":
        place = (p.get("args") or "side").strip() or "side"
        opened = True
        send({"jsonrpc": "2.0", "id": msg["id"], "result": {"open": {"id": "m", "title": "Meter", "placement": place, "columns": 44, "rows": 5, "view": view()}}})
