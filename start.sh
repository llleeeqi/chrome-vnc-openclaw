#!/bin/bash

pkill -9 chrome 2>/dev/null
pkill -9 Xvfb 2>/dev/null
pkill -9 x11vnc 2>/dev/null
pkill -9 websockify 2>/dev/null
sleep 1

rm -f /tmp/.X10-lock /tmp/.X11-unix/X10 2>/dev/null

fc-cache -f -v > /tmp/font-cache.log 2>&1 &

mkdir -p /root/chrome-data/Default
if [ ! -f /root/chrome-data/Default/Preferences ]; then
cat > /root/chrome-data/Default/Preferences << 'PREFS'
{
  "intl": {
    "accept_languages": "zh-CN,zh"
  },
  "browser": {
    "custom_chrome_frame_model": {}
  },
  "profile": {
    "default_content_setting_values": {
      "geolocation": 1
    }
  }
}
PREFS
fi

if [ ! -f /root/chrome-data/Local\ State ]; then
cat > /root/chrome-data/Local\ State << 'STATE'
{
  "intl": {
    "selected_languages": "zh-CN,zh"
  }
}
STATE
fi

Xvfb :10 -screen 0 1920x1080x24 -ac +extension GLX +render -noreset > /tmp/xvfb.log 2>&1 &
sleep 1

DISPLAY=:10 /opt/google/chrome/chrome \
    --remote-debugging-port=18800 \
    --remote-debugging-addr=127.0.0.1 \
    --user-data-dir=/root/chrome-data \
    --no-first-run \
    --no-default-browser-check \
    --window-size=1920,1080 \
    --disable-popup-blocking \
    --disable-extensions \
    --no-sandbox \
    --disable-gpu \
    --disable-dev-shm-usage \
    --lang=zh-CN \
    --accept-lang=zh-CN,zh \
    > /tmp/chrome.log 2>&1 &

sleep 2

x11vnc -display :10 -shared -forever -bg -nopw -rfbport 5900 > /tmp/x11vnc.log 2>&1 &

sleep 2

for i in {1..10}; do
    if curl -s http://127.0.0.1:18800/json/version > /dev/null 2>&1; then
        curl -s -X POST "http://127.0.0.1:18800/json/setPreference?cdp-Protocol-Version=0.1" \
            -H "Content-Type: application/json" \
            -d '{"name":"intl.selected_languages","value":"zh-CN,zh"}' 2>/dev/null
        break
    fi
    sleep 1
done

websockify --web /usr/share/novnc 6080 localhost:5900 > /tmp/novnc.log 2>&1 &

echo "Chrome+VNC started on display :10"
echo "VNC: 5900, noVNC: 6080, CDP: 18800"

wait
