set -u
cd /tmp/qwb-p3-check || exit 1
python3 -m http.server 8913 >/tmp/qwb-p3-http.log 2>&1 &
SERVER=$!
sleep 2
CHROME="google-chrome --headless=new --disable-gpu --no-sandbox --hide-scrollbars --force-device-scale-factor=1"
BASE=http://127.0.0.1:8913
OUT=/tmp/qwb-p3-shots
mkdir -p "$OUT"
echo "== owner DOM =="
timeout 120 $CHROME --window-size=1440,3400 --virtual-time-budget=25000 --dump-dom "$BASE/owner.html" > "$OUT/owner-dom.html" 2>/dev/null
echo "== visitor DOM =="
timeout 90 $CHROME --window-size=1440,3200 --virtual-time-budget=8000 --dump-dom "$BASE/visitor-report.html" > "$OUT/visitor-dom.html" 2>/dev/null
echo "== screenshots =="
timeout 90 $CHROME --window-size=1440,3200 --virtual-time-budget=12000 --screenshot="$OUT/visitor-home-1440.png" "$BASE/visitor.html" >/dev/null 2>&1
timeout 120 $CHROME --window-size=1440,3400 --virtual-time-budget=25000 --screenshot="$OUT/owner-home-1440.png" "$BASE/owner.html" >/dev/null 2>&1
kill $SERVER 2>/dev/null
wait $SERVER 2>/dev/null
ls -la "$OUT"
