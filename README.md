# Chrome VNC 容器

🥚 有头 Chrome 浏览器 + VNC 远程访问 + CDP 协议支持，可被 OpenClaw 等 AI 工具控制。

## 特性

- 🖥️ 有头 Chrome（非 headless），可交互
- 🌐 VNC/noVNC 可视化访问
- 🔌 CDP 协议支持，AI 可控制
- 📱 中文界面 + 中文字体
- 🔒 默认只监听本地，安全

---

## 快速开始（AI 用）

### 部署

```bash
git clone <本仓库地址>
cd chrome-vnc
docker compose up -d --build
```

等待 2-3 分钟构建完成。

### 验证

```bash
curl -s http://127.0.0.1:18800/json/version
curl -s http://127.0.0.1:6080/vnc.html | head -5
```

### OpenClaw 配置

```bash
openclaw config set browser.enabled true
openclaw config set browser.cdpUrl "http://127.0.0.1:18800"
openclaw config set browser.headless false
openclaw config set browser.noSandbox true
openclaw config set browser.defaultProfile openclaw
openclaw gateway restart
```

### 验证连接

```bash
openclaw browser status
openclaw browser tabs
```

---

## 人用：常用操作

```bash
# 重启浏览器容器
docker restart chrome-vnc

# 查看日志
docker logs chrome-vnc

# 清理标签页
openclaw browser tabs
openclaw browser close <tab_id>
```

### 公网访问

在 1Panel 创建反向代理：
- 目标地址：`http://127.0.0.1:6080`
- 建议开启密码认证

---

## 目录结构

```
chrome-vnc/
├── Dockerfile          # 镜像构建
├── docker-compose.yml # 编排配置
├── start.sh           # 启动脚本
├── mcp/               # MCP 工具（可选）
└── data/              # 浏览器数据持久化
```

## 注意事项

- CDP 端口：18800
- noVNC 端口：6080
- 浏览器数据保存在 `data/`
- 不需要可删除 `data/` 目录重置
