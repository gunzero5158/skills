# My Antigravity Skills Collection 🚀
这里是我个人制作并维护的 [Antigravity](https://github.com/GoogleDeepMind/antigravity) (或 Claude Code 等 Agent 终端) 专属本地技能（Skills）汇总合集。
通过编写这些自定义技能，我可以让 AI 助手掌握更多垂直领域的专属能力，突破常规交互的限制，实现更深度的自动化工作流。

## 🛠️ 包含的技能列表
### 1. 微信公众号文章抓取助手 (wechat-article-summarizer)
**简介**：
针对微信公众号极强的反爬虫和“环境异常”人机验证拦截机制，专门开发的一个免验证自动化抓取技能。当遇到需要 AI 总结微信文章时，默认的浏览器子节点或普通的 HTTP 请求常常会触发人机验证导致抓取失败。
**核心功能**：
- **无感绕过验证**：底层通过 Python 脚本及伪装标准浏览器请求头，直接无头获取公众号 HTML 源码，完美绕开“环境异常”的验证弹窗。
- **自动精准提取**：基于正则高精度剥离多余的 CSS、JS 和 HTML 标签，仅保留最核心的文章标题、作者和正文。
- **AI 全自动衔接**：Agent 只要检测到用户发送了 `mp.weixin.qq.com` 的链接，便会无缝调用此脚本获取纯文本，最后自动输出高质量的文章结构化总结。
**使用场景**：
“帮我总结一下这篇文章：https://mp.weixin.qq.com/s/...”

---
*持续更新中... 欢迎 Star ⭐️ 和 Fork！*
