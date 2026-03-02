#!/usr/bin/env python3
"""
Chrome MCP Tool - 通过 CDP 控制浏览器
用于 OpenCode MCP 集成
"""

import json
import subprocess
import sys
from typing import Any, Optional

CDP_HOST = "127.0.0.1"
CDP_PORT = 18799


def cdp_request(method: str, params: dict = None) -> dict:
    """发送 CDP 请求"""
    import urllib.request
    import urllib.parse

    url = f"http://{CDP_HOST}:{CDP_PORT}/json/{method}"
    if params:
        url += "?" + urllib.parse.urlencode(params)

    try:
        with urllib.request.urlopen(url, timeout=10) as resp:
            return json.loads(resp.read().decode())
    except Exception as e:
        return {"error": str(e)}


def get_tabs() -> list:
    """获取所有标签页"""
    return cdp_request("list")


def create_tab(url: str = "about:blank") -> dict:
    """创建新标签页"""
    return cdp_request("new", {"url": url})


def close_tab(tab_id: str) -> dict:
    """关闭标签页"""
    return cdp_request("close", {"id": tab_id})


def navigate(tab_id: str, url: str) -> dict:
    """导航到 URL"""
    return cdp_request("navigate", {"id": tab_id, "url": url})


def take_screenshot(tab_id: str = None) -> Optional[str]:
    """截图"""
    if not tab_id:
        tabs = get_tabs()
        if not tabs:
            return None
        tab_id = tabs[0]["id"]

    import urllib.request

    url = f"http://{CDP_HOST}:{CDP_PORT}/screenshot?id={tab_id}&format=png"
    try:
        with urllib.request.urlopen(url, timeout=10) as resp:
            import base64

            return base64.b64encode(resp.read()).decode()
    except Exception as e:
        return None


def eval_js(tab_id: str, script: str) -> Any:
    """执行 JavaScript"""
    import urllib.request
    import urllib.parse

    url = f"http://{CDP_HOST}:{CDP_PORT}/json/evaluate?id={tab_id}"
    data = json.dumps({"expression": script}).encode()

    req = urllib.request.Request(
        url, data=data, headers={"Content-Type": "application/json"}
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            result = json.loads(resp.read().decode())
            return result.get("result", {}).get("value")
    except Exception as e:
        return {"error": str(e)}


def main():
    if len(sys.argv) < 2:
        print("Usage: chrome-mcp <command> [args...]")
        print("Commands:")
        print("  tabs              - 列出所有标签页")
        print("  navigate <url>    - 导航到 URL")
        print("  screenshot        - 截图 (base64)")
        print("  eval <js>         - 执行 JavaScript")
        print("  new <url>         - 创建新标签页")
        sys.exit(1)

    cmd = sys.argv[1]

    if cmd == "tabs":
        print(json.dumps(get_tabs(), indent=2, ensure_ascii=False))
    elif cmd == "screenshot":
        result = take_screenshot()
        if result:
            print(result)
        else:
            print(json.dumps({"error": "截图失败"}))
    elif cmd == "navigate" and len(sys.argv) > 2:
        tabs = get_tabs()
        if tabs:
            print(
                json.dumps(
                    navigate(tabs[0]["id"], sys.argv[2]), indent=2, ensure_ascii=False
                )
            )
    elif cmd == "eval" and len(sys.argv) > 2:
        tabs = get_tabs()
        if tabs:
            print(
                json.dumps(
                    eval_js(tabs[0]["id"], " ".join(sys.argv[2:])),
                    indent=2,
                    ensure_ascii=False,
                )
            )
    elif cmd == "new" and len(sys.argv) > 2:
        print(json.dumps(create_tab(sys.argv[2]), indent=2, ensure_ascii=False))
    else:
        print(json.dumps({"error": "未知命令"}))


if __name__ == "__main__":
    main()
