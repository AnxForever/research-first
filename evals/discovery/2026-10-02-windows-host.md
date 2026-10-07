# Windows Claude Code 宿主触发评测

## 环境与隔离

本轮在 Windows 原生 Claude Code 2.1.281 上执行，使用已有默认 provider/model；探测与任务流都报告 `deepseek-v4-flash[1m]`（assistant 事件同时显示 `deepseek-v4-flash`）。没有切换模型或 provider，也没有改全局安装或设置。

评测源快照为 `D:\research-first` HEAD `c94db861ede29f3d718ea6be1dc1b0f1875cb88a`。Claude Code 文档规定项目 skill 放在 `.claude/skills/<name>/SKILL.md`，个人 skill 放在 `~/.claude/skills/<name>/SKILL.md`，并说明 Claude 可按 skill 描述自动调用；开始测试前检查了 Windows 用户级 `~/.claude/skills/research-first` 与 `~/.agents/skills/research-first`，当时都不存在。之后每个隔离运行 fixture 才各自创建一个 `.claude/skills/research-first` 项目副本，没有安装到用户目录。[Claude Code skills 文档](https://code.claude.com/docs/en/skills)

五个运行 fixture 位于 `D:\research-first-review\2026-10-02\next-stage-eval\host\claude-cases\<case-id>`，各自是独立 git 仓库。它们都从准备阶段的公共合成任务列表 HTML 起步；本仓库现将该 pre-run 输入保存为 [`fixtures/host/index.html`](fixtures/host/index.html)，冻结提示、分类、停止规则和哈希保存为 [`host-cases.json`](host-cases.json)。种子取自准备阶段 `positive-search/index.html`，不是运行后被改动的 `negative-button-label`；原种子没有 README。每个运行 fixture 都从 `c94db86` 快照物化了同一项目级 skill，五套副本逐文件字节相同。和原始 Git blob 比较时，12 个文件中有 6 个 raw SHA256 相同；其余 6 个只有 CRLF/LF 换行差异，统一归一化为 LF 后 12/12 字节完全相同，没有正文差异。清单保留运行副本 SHA256，并列出 Git blob SHA256 与 LF 归一化 SHA256。仓库中的 host fixture 只包含原始 HTML，不含安装后的 skill、生成改动或原始 trace。

每条使用新进程、`--no-session-persistence`、40 秒上限和 `acceptEdits`（仅作用于隔离 fixture）；prompt 以 UTF-8 bytes 从 stdin 输入，并用 `--output-format stream-json --verbose` 保存工具事件、stderr、最终输出和 usage 元数据。实际命令没有使用 `--allowedTools`，因此没有过滤 Claude Code 默认可用工具；权限行为由 `--permission-prompts none` 与 `--permission-mode acceptEdits` 控制。Claude Code CLI 文档确认 `-p` 是非交互模式，支持 `stream-json`、`--no-session-persistence` 和会话级 `--permission-mode`。[Claude Code CLI reference](https://code.claude.com/docs/en/cli-reference)

这里的 12 文件副本仅用于触发检查，包含入口、references 与 agents 信息，没有复制 assets 和可选脚本；不能把它算作完整安装验收。后续成品任务使用了包含这些支持文件的 18 文件副本，单独记录于[成品评测](2026-10-02-windows-outcomes.md)。

## 结果

| Case | 提示 | 实际证据 | 正文在 trace 中可见 | 用时与结束 |
|---|---|---|---|---|
| positive-search | 给任务列表加一个能快速找到条目的搜索功能 | 调用 `Skill(research-first)`；配对 tool result 为非错误的 `Launching skill: research-first` | 否 | 8.11 秒；收到启动确认后停止，完成度未评估 |
| positive-filter-repetition | 经常重复选筛选条件，帮我省点操作 | 没有 `Skill` 工具调用；但 `Read` 精确读取项目副本的 `SKILL.md`，工具返回 13,545 字符 | 是 | 19.55 秒；正文读取成功后停止，完成度未评估 |
| negative-button-label | 只把按钮“提交”改成“保存”，其他不动 | 没有 `Skill(research-first)` 调用，也没有读取目标 `SKILL.md`；CLI 正常返回 success | 否 | 13.50 秒；正常完成 |
| negative-explain-function | 解释一下这段函数返回什么，不改代码 | 没有 `Skill(research-first)` 调用，也没有读取目标 `SKILL.md`；CLI 正常返回 success | 否 | 14.86 秒；正常完成 |
| explicit-health-control | 请明确使用 research-first 技能，先研究适合这个任务的实现方案并说明取舍。 | 调用 `Skill(research-first)`；配对 tool result 为非错误的启动确认 | 否 | 5.16 秒；收到启动确认后停止，完成度未评估 |

`loaded` 按两类原始工具证据判断：成功调用 `Skill(research-first)` 并收到配对成功结果，或成功读取 fixture 内目标 `SKILL.md` 并收到文件内容。`confirmed_invocation` 只表示前一类；`confirmed_target_file_read` 表示后一类。启动确认不证明完整 skill 正文已进入可见 trace，也不证明模型遵循了正文。可见正文只在 positive-filter-repetition 的直接文件读取事件中出现。Skill 结果没有提供 `base_dir`；该结果的项目归属由独立 fixture cwd、唯一项目副本和源文件哈希共同确认。

两条自动触发正例都观察到目标加载证据；两条负例都正常完成且没有观察到目标加载。显式调用对照也触发成功。每类只有两个短样本，结果只描述这一版 Windows CLI、当前默认模型与合成 fixture。

三条在加载后中断的会话按预先约定记为 `task_completion=not_evaluated`，没有完整的最终 usage 对象；trace 只保留中断前可见的部分 token 事件。两条正常完成的负例保留最终 usage：button-label 为 input 23,257、cached input 111,872、output 949；explain-function 为 input 22,654、cached input 43,520、output 1,168。原始 stream 中的模型字段和部分 usage 事件均保留。

## 复跑与产物

下面的 Python 片段仅演示 UTF-8 stdin 与 stdout/stderr 分流的单次启动；它不是完整评测 runner。复跑时需从冻结的 c94 快照为每个 case 建独立 fixture，并放入项目级 skill。此片段的 40 秒硬超时不能识别成功加载事件后提前停止；自动停止和证据判读需要监视 `stream-json` 的 runner。实际评测 runner 对每个 case 做了 40 秒监视及首个有效加载事件后的中止。

```python
from pathlib import Path
import subprocess

fixture = Path("path/to/fresh-fixture").resolve()
artifacts = Path("path/to/external-artifacts").resolve()
artifacts.mkdir(parents=True, exist_ok=True)
prompt = "给任务列表加一个能快速找到条目的搜索功能"
with open(artifacts / "case.jsonl", "wb") as stdout, open(artifacts / "case.stderr", "wb") as stderr:
    try:
        subprocess.run(
            ["claude", "-p", "--output-format", "stream-json", "--verbose",
             "--no-session-persistence", "--permission-prompts", "none",
             "--permission-mode", "acceptEdits"],
            cwd=fixture,
            input=prompt.encode("utf-8"),
            stdout=stdout,
            stderr=stderr,
            timeout=40,
            check=False,
        )
    except subprocess.TimeoutExpired:
        pass  # Keep the partial stream for manual inspection.
```

每个正例或显式对照在匹配工具返回后停止；负例需等到 CLI 正常返回才记为未触发。原始 trace、stderr、final 和逐例摘要保存在 `D:\research-first-review\2026-10-02\next-stage-eval\host\claude-cases\results\`；五个 fixture 哈希核对和汇总分别见同一 host 目录中的 `claude-fixture-hash-check.json` 与 `claude-evaluation-summary.json`。
