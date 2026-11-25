# GitHub 私有仓库同步

> 方法来源：视频 7708632974811463716 口播；仓库形态参考 `obra/superpowers` 与 `anthropics/skills` 的 skill 目录结构。
> 本文件只给命令，不代为执行。任何 push、公开、分享都要先取得明确确认。

## 一、为什么用 GitHub

视频的定位：把它当成自带修改记录的云端私有文件夹。改一个标点也留快照，AI 改乱或误删可一键回退。换模型、换 harness、换电脑、换 Windows 或 macOS，只要连上 GitHub，积累即可取回。

本地目录本身就是底稿。GitHub 只解决跨设备与审计，不改变技能内容。

当前状态（2026-11-25）：本地 git 已初始化；用户手动建立私有空仓库，远端同步已启用，所有本地提交均已推送到 `origin/main`。连接器建仓接口返回 `403 Resource not accessible by integration`，故改由用户在网页建仓，本地 push 完成首次同步。

## 二、仓库结构

```
chenxiaolei-profile/
  SKILL.md
  README.md
  references/
    profile.md
    style-writing.md
    style-visual.md
    workflows.md
    self-evolution.md
    github-sync.md
  scripts/
    redact_check.py
    append_evolution.py
  tests/
    test_skill_invariants.py
  evolution/
    LOG.md
```

## 三、首次建仓（需用户确认后执行）

```bash
cd ~/.workbuddy/skills/chenxiaolei-profile
git init
git remote add origin <你的私有仓库地址>
python scripts/redact_check.py .
git add .
git commit -m "init: chenxiaolei-profile v1.0.0"
git push -u origin main
```

仓库必须设为 Private。地址不要写进任何文件。

## 四、日常同步

```bash
cd ~/.workbuddy/skills/chenxiaolei-profile
git pull --rebase origin main
python scripts/redact_check.py .
python -m unittest discover -s tests -v
git add .
git commit -m "evolve: <一句话说明本次写回>"
git push origin main
```

禁止 `git push --force`。冲突时停止，人工比对两边 `evolution/LOG.md`，保留两份记录，再重跑测试。

## 五、跨 Agent 导入

| 环境 | 技能目录 | 动作 |
|---|---|---|
| WorkBuddy | `~/.workbuddy/skills/` | 本目录原位使用 |
| Claude Code | `~/.claude/skills/` | 复制或软链同一目录 |
| Codex / Copilot CLI / Gemini CLI | `~/.agents/skills/` | 该路径为跨运行时别名，导入同一文件夹 |
| 云端 Agent | 对话附件或仓库拉取 | 上传整个文件夹，或拉取私有仓库后按上述目录放入 |

来源：`obra/superpowers` 的 `skills/writing-skills/SKILL.md` 明确个人技能位于运行时 skills 目录，且 Codex、Copilot CLI、Gemini CLI 识别 `~/.agents/skills/` 作为跨运行时别名。

## 六、脱敏与合规

- 禁止入库：学生真实姓名、成绩排名、家庭情况、手机号、身份证号、家校沟通原文中的可识别信息。
- `scripts/redact_check.py` 是推送前硬门禁，命中即退出码 1。
- 合法写回内容：抽象规则，例如涉及家长面谈时每点须附法律或校内管理依据。
- 不要把 ima 凭证、API Key、COS 签名凭据写入仓库。凭据只走环境变量或本地未入库文件。
- 门禁只检查工作区当前文本，不检查 git 历史。若曾误提交敏感内容，按泄露处理：先移除仓库访问权限，再清理历史并轮换相关凭据，不能只在当前分支删文件。
- 仓库根目录保留 `.gitignore`，排除临时文件、凭证文件和本机缓存。

## 七、回退

```bash
git log --oneline -- references/profile.md
git checkout <上一版提交> -- references/profile.md
git commit -m "rollback: profile.md 回退到 <提交号>"
```

回退只针对具体文件，不整体 reset，避免抹掉 `evolution/LOG.md` 的审计记录。

## 八、失效与降级

- 无网络或 GitHub 不可达：本目录照常用，等恢复后按第四节补同步。
- 仓库不可访问：不要改用公开仓库，不要绕过脱敏门禁。
- 某 Agent 不支持 skills 目录：把 SKILL.md 与所需 reference 作为上下文文件显式喂入，仍读同一份底稿。

## 自进化增量（自动生成）

<!-- EVOLUTION-START -->
- [E-20261125-001][C1] 个人档案 Skill 默认启用 GitHub 私有仓库作为跨设备同步与版本回退介质；推送前必须通过脱敏门禁
<!-- EVOLUTION-END -->
