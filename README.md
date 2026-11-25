# 陈小磊个人档案 Skill · 蒸馏说明

版本 1.0.0 / 2026-11-25。安装位置：`~/.workbuddy/skills/chenxiaolei-profile/`。

## 一、视频主要内容

来源：今日头条视频 `7708632974811463716`，账号 AI工具科普社，发布于 2026-11-16 13:12，时长 2 分 54 秒，播放约 3.3 万。取稿方式：页面元数据解析得到视频 ID 与播放令牌，下载 MP4 后本地 ASR 转写（L0 一手材料）。

| 段落 | 核心内容 |
|---|---|
| 0:00—0:38 | 切换 AI 工具时，重新交代背景、进展、个人和公司信息会返工三四遍，白耗 40 分钟。建个人档案 Skill 放 GitHub，3 分钟搭好，之后换任何 AI 或电脑，1 分钟接手 |
| 0:38—1:00 | 重度用户在不同 Agent 之间认知归零；换电脑后不同 Agent 的历史信息不通 |
| 1:00—2:00 | 核心是把个人资料从聊天框提取出来，做成独立 Skill 文件夹。机制一：跟着对话自己长，不要静态 TXT；项目节点结束、改了工作注意事项、对润色提了新要求，顺手让 AI 提炼偏好原则写回 Skill |
| 2:00—2:30 | 机制二：同一台电脑上多个支持本地 Skill 的 Agent 共用同一份底稿；Codex 建好后导入 WorkBuddy，云端 Agent 上传同一文件 |
| 2:30—2:55 | 机制三：跨电脑连云端放 GitHub 私有仓库。当自带修改记录的云端私有文件夹；改一个标点也留快照，改乱可回退；换模型、换 harness、换电脑、换 Windows 或 macOS，连上 GitHub 即可取回 |

视频称创建提示词放在最后，但 ASR 于 2:54.640 结束，结尾画面文字未纳入转写。`references/self-evolution.md` 第七节的提示词为依据口播方法重构，标 C2。

## 二、本技能如何蒸馏

| 来源 | 取用内容 | 等级 |
|---|---|---|
| 视频 ASR 全文 | 自进化三机制、六类触发点的原型、GitHub 版本回退思想 | C1 |
| 用户级 MEMORY.md / USER.md / SOUL.md | 身份、写作规范、视觉规范、工作流、交付铁律、边界红线 | C1 |
| ima 知识库风格文档 | 多巴胺 PPT 三套配色、中国风长图视觉规范、AIFA 深色骨架 | C1 |
| anthropics/skills | SKILL.md 最小结构：YAML name + description，指令正文 | C1，取原则 |
| obra/superpowers | description 用 Use when 写触发条件；skill 目录结构；跨运行时 skills 路径；skill 需测试后再部署 | C1，取原则 |
| 用户当前关注快照 | 校长选聘、家长请愿、德育制度等 | C2，30 天复核 |

## 三、GitHub 工具检索留痕

```
工具检索：GitHub 搜「agent skill personal memory profile」与「agent skills in:name,description stars:>100」，看 anthropics/skills、obra/superpowers、affaan-m/ECC、mattpocock/skills 等仓库
采纳：anthropics/skills — 取 SKILL.md 最小结构原则（未安装、未复制代码）；obra/superpowers — 取 Use when 描述、目录结构、skills 测试原则（未安装、未复制代码）
放弃：affaan-m/ECC — README 超长，本任务只需个人档案结构，读全成本高于收益；mattpocock/skills、JuliusBrussee/caveman — 面向编码效率，与教育研究个人底稿不对口
自研：自进化字段表、脱敏门禁、写回脚本按陈小磊既有交付铁律自写，因无现成实现且 120 行内可解决
```

## 四、安装与使用

已在用户级 skills 目录安装。2026-11-25 完成本地 git 初始化并提交 `715f40c`，首条进化记录 `E-20261125-001` 已写回 `github-sync.md`。同日用户手动建立私有空仓库，远端同步已启用，所有本地提交均已推送到 `origin/main`。

任意对话中触发：

- 按我的习惯写这份报告。
- 记住：以后所有交付都附方法与工具。
- 把这条偏好写进我的个人档案。
- 换设备后按我的个人档案接手。

手工写回：

```bash
python ~/.workbuddy/skills/chenxiaolei-profile/scripts/append_evolution.py \
  --trigger "项目节点结束" \
  --raw "以后报告都按四环框架排" \
  --distilled "报告默认按四环框架排，方法与局限单列附录" \
  --scope "网页看板与研究报告" \
  --level C1 \
  --target "workflows.md"
```

校验：

```bash
cd ~/.workbuddy/skills/chenxiaolei-profile
python -m unittest discover -s tests -v
python scripts/redact_check.py .
```

GitHub 同步命令见 `references/github-sync.md`。未取得明确确认前不执行 push。

## 五、验证状态

- 不变量测试：见本次交付说明的通过数。失败项必须视为缺陷。
- 脱敏门禁：对全目录扫描通过。
- 真实用户验证：未验证。本技能依据用户历史档案蒸馏，尚未由陈小磊在实际换机或多 Agent 场景中试用。建议下次跨设备任务时实测一次并回收结果。

## 六、已知边界

- 视频结尾提示词未在 ASR 中，重构模板属 C2。
- 当前关注快照 30 天后需复核。
- 用户级 MEMORY.md 仍是硬规则正本，本技能不自动改写它。
- GitHub 私有仓库只提供版本与同步，不提供端到端加密；学生敏感信息不得入库。
