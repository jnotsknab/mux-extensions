import sys, os, json, glob, threading, time, gzip, urllib.request
sys.stdout.reconfigure(encoding="utf-8")
URL = "https://api.anthropic.com/api/oauth/usage"
MIN_GAP = 60      # endpoint 429s if polled faster than ~1/min
POLL = 90         # background refresh
lock = threading.Lock()
last = 0.0
def send(o):
    with lock: print(json.dumps(o), flush=True)
def chip(text):
    send({"jsonrpc": "2.0", "method": "footer/set", "params": {"id": "q", "text": text}})
def auth_token():
    base = os.environ.get("MUX_CLIPROXY_HOME") or os.path.join(os.environ.get("LOCALAPPDATA", ""), "Mux-Swarm", "cliproxy")
    files = [f for f in glob.glob(os.path.join(base, "auth", "claude-*.json")) if not f.endswith(".bak")]
    files.sort(key=os.path.getmtime, reverse=True)
    for f in files:
        try:
            a = json.load(open(f, encoding="utf-8"))
        except Exception:
            continue
        if not a.get("disabled") and a.get("access_token"):
            return a["access_token"]
def pct(w):
    try: return f"{float((w or {})['utilization']):.0f}%"
    except Exception: return "?"
def refresh():
    global last
    if time.time() - last < MIN_GAP: return
    last = time.time()
    try:
        tok = auth_token()
        if not tok: return chip("claude: no auth")
        req = urllib.request.Request(URL, headers={"Authorization": "Bearer " + tok,
            "anthropic-beta": "oauth-2025-04-20", "User-Agent": "claude-code/2.0.32",
            "Accept-Encoding": "gzip"})
        with urllib.request.urlopen(req, timeout=15) as r:
            raw = r.read()
            if r.headers.get("Content-Encoding", "").lower() == "gzip": raw = gzip.decompress(raw)
        u = json.loads(raw)
        chip(f"5h {pct(u.get('five_hour'))} 7d {pct(u.get('seven_day'))}")
    except Exception as e:
        print("usage fetch failed: " + str(e), file=sys.stderr, flush=True)
def loop():
    while True:
        refresh(); time.sleep(POLL)
threading.Thread(target=loop, daemon=True).start()
for line in sys.stdin:
    try: msg = json.loads(line)
    except Exception: continue
    if msg.get("method") == "event" and (msg.get("params") or {}).get("event") == "turn_end":
        threading.Thread(target=refresh, daemon=True).start()
