---
name: chenxiaolei-profile
description: "Use when 陈小磊要求按其个人习惯、风格、工作流办事，或要求创建、更新、跨设备同步个人档案 Skill。触发词：按我的习惯、我的风格、个人档案、记住我的偏好、蒸馏我的个人 skill、换设备接手、跨端同步。不用于与其无关的一般问答。"
version: "1.0.0"
updated: "2026-11-25"
---

# 陈小磊个人档案（Self-Evolving Profile）

## 定位

本技能是陈小磊的可迁移个人底稿。它把散落在历史对话、本地记忆、ima 知识库和工作习惯中的偏好，收束为一份可被任意 Agent 读取、可随对话生长、可经 GitHub 私有仓库跨设备迁移的文件夹。

三层职责：

- 本目录：蒸馏后的当前状态与执行入口。
- 用户级 `MEMORY.md`：硬规则唯一正本。本技能只引用，不擅自改写。
- `evolution/LOG.md`：每次对话新提炼的偏好、证据与等级。

## 每次任务开始的执行顺序

1. 读 `references/profile.md`，确认身份、角色边界、当前主线。
2. 按任务类型读对应参考：写作读 `style-writing.md`；PPT、图表、看板读 `style-visual.md`；书籍蒸馏、周报、PBL、家校材料读 `workflows.md`。
3. 凡非平凡任务，先按 `workflows.md` 的 GitHub-first 纪律检索开源做法。
4. 涉及学生真实姓名、成绩、家庭情况，先脱敏。涉及对外发布、上传、推送，先取得明确确认。
5. 交付前跑 `verifiable-delivery` 四关，并附收尾拓展①②③。

## 不可覆盖的硬规则

- 中文交付，中文引号""，学术口气，数字一律阿拉伯数字。
- 一手材料优先。推断标 C2，待核标 C3，不把推断写成事实。
- 交付必给方法与工具、可复算路径、测试或校验结果。
- 完成后从行业顶级专家视角再审并实际修改，不只写建议。
- 不擅自发布、上传、推送。GitHub 同步只准备命令，执行前确认。

## 自进化触发点

详见 `references/self-evolution.md`。简表：

- 项目节点结束、用户改了工作注意事项、对润色或排版提了新要求、明确说以后都这样、连续两次同类纠正。
- 动作：提炼字段 → 写 `evolution/LOG.md` → 必要时更新 `references/profile.md` 对应小节 → 跑校验脚本。
- 硬规则不在对话中直接改。要先建议更新 `MEMORY.md`，等确认后再动。

## 跨设备与跨 Agent

详见 `references/github-sync.md`。核心：同一目录即底稿；Codex、WorkBuddy、云端 Agent 导入同一文件夹；GitHub 私有仓库只作带版本记录的同步介质；pull --rebase，禁止 force push；推送前跑脱敏检查。

## 来源与版本

- 视频方法：今日头条视频 `7708632974811463716`，AI工具科普社，2026-11-16。口播 ASR 已转写；结尾画面提示词未纳入转写，相关模板属重构，标 C2。
- 规范来源：用户级 `MEMORY.md`、`USER.md`、`SOUL.md`；ima 知识库风格文档；`anthropics/skills`；`obra/superpowers`。
- 版本：1.0.0 / 2026-11-25。
