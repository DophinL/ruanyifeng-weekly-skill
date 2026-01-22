> **✨ Sponsored by [YouMind.com](https://youmind.com) — 你的第一款 Vibe Creating 工具**

---
# 阮一峰周刊工具搜索 Skill

搜索[阮一峰科技爱好者周刊](https://github.com/ruanyf/weekly/issues)中社区提交的数千个工具和资源。

## 功能

- 通过关键词搜索周刊 issues 中的工具推荐
- 返回 5 条最相关结果
- 支持按分类筛选：`【工具自荐】`、`【开源自荐】`、`【网站自荐】` 等

## 安装

### 方式一：使用 skills CLI（推荐）

自动检测所有 AI 助手（Claude Code、Cursor、Codex、Gemini CLI、Windsurf 等）：

```bash
npx skills i DophinL/ruanyifeng-weekly-skill
```

### 方式二：使用 openskills CLI

```bash
npx openskills i DophinL/ruanyifeng-weekly-skill
```

### 方式三：让 Claude Code 自行安装

直接告诉 Claude Code：

> 帮我安装这个 skill: https://github.com/DophinL/ruanyifeng-weekly-skill

### 方式四：Claude 桌面端手动安装

1. 下载本仓库到本地
2. 打开 Claude 桌面端，进入 **Settings（设置）**
3. 切换到 **Capabilities** 标签页
4. 点击 **Add Skill** 按钮
5. 将 `ruanyifeng-weekly-skill.skill` 文件拖入安装

## 更新

```bash
npx skills u DophinL/ruanyifeng-weekly-skill
```

## 使用示例

安装后，直接向 AI 助手提问即可触发：

- "帮我找一个 AI 内容创作工具"
- "有没有好用的 Nano Banana Pro 提示词网站？"
- "搜索阮一峰周刊里的 OCR 工具"
- "找一个开源的视频剪辑工具"

## License

MIT
