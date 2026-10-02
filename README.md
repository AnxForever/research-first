# research-first

**简体中文** · [English](README.en.md)

让 AI agent 在实现功能前，先理解你的目的，调查相关产品、开源方案和技术资料，再把有依据的选择呈现给你。

**可以不复用，但必须调查；可以自己实现，但不能默认从零造轮子。**

用户往往只说得出一个想法，不会顺带列出所有可用的组件库、动画库、成熟产品和实现技巧。`research-first` 把这部分发现工作交给 agent，并要求调研真正影响选型、实现和验证。

[快速开始](#快速开始) · [行为示例](#行为示例) · [你应该看到什么](#你应该看到什么) · [适用边界](#适用边界) · [可选的-jev-复核](#可选的-jev-复核) · [文件导航](#文件导航)

## 行为示例

你说：**「给后台加一个支持筛选、排序的数据表。」**

| 环节 | 需要纠正的行为 | 使用 research-first 后的预期行为 |
|---|---|---|
| 理解需求 | 把一句话直接当成完整规格 | 结合项目确认操作流程、数据规模、关键状态和约束 |
| 找方案 | 凭已有知识手写表格和交互 | 检查现有组件，调查同类产品、可复用的表格方案和官方资料 |
| 作选择 | 写完后才解释为什么这样做 | 实现前展示候选、来源、取舍、推荐及仍需自研的部分 |
| 做验证 | 页面能显示就算完成 | 把调研发现落实到相关筛选、排序、空态和键盘操作等验收条件 |

前端调研也包括合适的组件库、专用组件，以及在确有动效需求时的动画库。选型要考虑现有技术栈、样式控制、交互状态、可访问性、维护和接入成本。可以复用、改造、组合，也可以在比较后自行实现。

同样的原则也适用于后端、架构、集成、文档和方案决策：寻找能解决当前问题的产品、实现与资料，补齐你没说出的关键问题，同时尊重明确指定的技术和范围。

## 快速开始

通过 Skills CLI 安装：

```bash
npx skills add AnxForever/research-first
```

也可手动克隆到 agent 的技能发现目录。`npx skills add` 适用于已安装 Node.js/npm 的常见 shell。手动克隆时，目标文件夹必须尚不存在；以下示例以 `~/.agents/skills/research-first` 为目标：

```bash
mkdir -p "$HOME/.agents/skills"
git clone https://github.com/AnxForever/research-first.git "$HOME/.agents/skills/research-first"
```

Windows PowerShell：

```powershell
$skillRoot = Join-Path $HOME ".agents/skills"
New-Item -ItemType Directory -Force -Path $skillRoot | Out-Null
git clone https://github.com/AnxForever/research-first.git (Join-Path $skillRoot "research-first")
```

Windows 命令提示符（cmd）：

```bat
if not exist "%USERPROFILE%\.agents\skills" mkdir "%USERPROFILE%\.agents\skills"
git clone https://github.com/AnxForever/research-first.git "%USERPROFILE%\.agents\skills\research-first"
```

其他环境请将仓库克隆到该 agent 的技能发现目录，并保留完整文件夹，使 `SKILL.md` 能找到它引用的资料。若目标目录已存在，请在该目录中更新已有克隆，不要重复克隆到同一路径。

安装后，在支持 `$skill-name` 调用的 agent 中输入：

```text
用 $research-first 给这个项目加一个支持筛选、排序的数据表。
先理解实际使用场景，调查同类产品、可复用组件和官方资料，
实现前告诉我有哪些选择、推荐哪个，以及还需要自己写什么。
```

若你希望 agent 自主选型并继续执行，可以直接说明：

```text
用 $research-first 完成这个功能。你可以在现有技术栈内自主选型；
先简要展示比较与依据，然后继续实现和验证。
```

也可以只做调研：

```text
用 $research-first 调研这个功能的产品做法、开源方案和技术资料。
给出候选、取舍与推荐，这次不改代码。
```

支持自动技能匹配的环境也可根据请求选择这个 skill；显式调用便于明确要求使用它。核心技能是 Markdown 指令，没有运行时依赖；实际查阅网站、读取代码和运行验证，需要 agent 提供相应工具。可选的 Jev 适配单独安装，不影响普通使用。

## 你应该看到什么

```text
理解目的 → 查看现状 → 调查现成方案与资料 → 展示选择 → 实现 → 验证
```

在实质实现前，agent 应给出一份与任务分量相称的简短说明：

- **目的与约束**：解决谁的问题，项目已有些什么，哪些假设仍待确认。
- **证据与发现**：查阅了哪些产品、源码、文档或实验；哪些发现改变或支持了做法。
- **候选与取舍**：能复用什么，接入需要付出什么，哪些能力仍需自己实现。
- **推荐与验证**：为什么选择这个方案，如何确认它适合当前项目并覆盖关键失败情况。

例如，数据表选型可以这样组织。下表仅示意比较方向，实际候选必须有来源和核实结果：

| 路径 | 需要查清 | 应向用户解释 |
|---|---|---|
| 扩展项目现有组件 | 是否覆盖所需交互，缺口在哪里 | 哪些能力可直接沿用，哪些要补齐 |
| 接入专用表格库并沿用现有样式 | API、版本兼容、交互支持和许可证 | 能省下哪些实现工作，增加什么依赖与接入成本 |
| 自行实现 | 已调查的候选具体哪里不适合 | 自研的理由、参考依据及后续维护责任 |

推荐复用时，要说明仍需处理的业务逻辑和集成工作；推荐自研时，要说明为什么可信候选不适合。表格逻辑与动画是不同的选择，不应捆绑成「全套引库」或「全部手写」二选一。

实现完成后，报告实际交付内容、验证结果和仍未确认的事项。只有单个可逆功能在单次会话内完成、且无需深度（Deep）研究时，简短的「证据 → 决策 → 验证」记录才足够；实施前摘要可以记录证据与决策，再在完成说明中补上验证。多功能、跨会话或高风险任务使用[逐功能证据台账](references/feature-evidence-ledger.md)，防止一篇项目级调研被用来替所有子功能背书。

## 适用边界

- **实质功能需要调研。** 新功能、页面、交互、集成和重要方案选择都适用。仅改文案等不引入新行为的明确、低风险修改可以直接处理；代码改动虽小但引入新行为，仍属于实质功能。
- **证据强度匹配主张。** 重要主张优先用一手依据支持；高风险主张，或可能重大影响结果的证据争议，还要寻找独立佐证或用独立检查核实。
- **用户保留选择，也可以委托决策。** 尚未委托的重要产品、依赖、费用或视觉取舍需要用户选择；用户已选定或委托选型、且已授权执行时，说明依据后继续，不重复索要许可。
- **尊重约束，按任务分量研究。** 明确指定的技术和禁止新增依赖等要求应当遵守；无需为每次小改动做全行业调查，也不会为了前端任务硬加动画库。
- **复用已有证据，重新审视受影响的结论。** 有效调研不重复做；用户提出质疑时，寻找可能推翻当前方案的证据，而非只替已有实现辩护。
- **调查不到就说明缺口。** 无网络、资料不足或候选未验证时，明确区分事实、推断和假设；不能把搜索失败说成「没有现成方案」。

这是给 agent 的工作指导。是否执行到位，需要看它实际查阅的来源、展示的选项和交付证据；仓库中的示例也不替代当前项目的验证。

## 可选的 Jev 复核

可以让 Jev 在关键点多做一次范围明确的检查，而不是每一步都调用另一个模型：

| 时机 | 检查的问题 |
|---|---|
| 理解需求后 | 这段解释是否保留了用户明确提出的要求？ |
| 查阅资料后 | 这段实际读到的材料是否支持这一条结论？ |
| 展示选型前 | 摘要是否把已有的可行选项和重要代价告诉了用户？ |
| 验证完成后 | 这句完成声明是否与实际执行的检查一致？ |

2026-09-22 核实的稳定版为 `jev-1.13.0`，真实 API 探针也确认 `jev-latest` 返回该版本。适配复用官方 Python SDK，默认只预览请求；显式启用 `--live` 后才发送你提供的短证据卡。它不会自动收集项目或对话。

Jev 的输出仅是建议：不能证明来源真实、代替运行测试、决定用户偏好或批准实施。真实项目试验中出现过与预先记录的评估标签不一致的低置信度结果，因此没有设置自动放行阈值。

使用方法与适用边界见 [Jev 检查指南](references/jev-checkpoints.md)；真实项目试验、预先标注的案例及原始结果见 [验证记录](evals/README.md)。核心流程不依赖 Jev 可用。

## 文件导航

| 文件 | 用途 |
|---|---|
| [SKILL.md](SKILL.md) | 技能入口：意图理解、调研、选型、执行与验证 |
| [复用与备选方案](references/reuse-and-alternatives.md) | 调查现成方案、前端资源和实现前的用户选择 |
| [搜索质量](references/search-quality.md) · [调研深度](references/adapting-depth.md) | 选择证据、控制深度、判断何时停止搜索 |
| [问题扩展](references/problem-expansion.md) · [证据冲突](references/contradictions.md) | 补齐重要问题，处理资料之间的矛盾 |
| [逐功能证据台账](references/feature-evidence-ledger.md) | 跟踪每个功能的证据、决策和历史缺口 |
| [调研示例](references/research-examples.md) · [案例](references/case-studies.md) · [评估场景](references/intent-interpretation-evaluation.md) | 理解工作方式，检查常见判断偏差 |
| [调研报告模板](assets/research-report-template.md) · [项目背景卡](assets/project-identity-card.md) | 按需保存调研结论和长期项目背景 |
| [agents/openai.yaml](agents/openai.yaml) | 技能展示信息和默认调用提示 |
| [Jev 检查指南](references/jev-checkpoints.md) · [可选适配](scripts/jev_check.py) | 有界证据卡、官方 SDK 调用和结果解读 |
| [验证记录](evals/README.md) · [边界案例](evals/jev-cases.json) | 真实项目试验、可复现材料与局限 |

入口之外的资料按需读取；短任务无需产出全部模板。

## 许可

[MIT](LICENSE)

## 维护者校验

仓库维护者可用 Python 3.12 安装校验依赖、检查可分发包并运行离线测试：

```bash
python -m pip install -r scripts/requirements-dev.txt -r scripts/requirements-jev.txt
python scripts/validate_package.py
python -m unittest discover --start-directory tests --pattern "test_*.py" --verbose
```

这些依赖和命令只用于维护与校验，不是技能的运行依赖；日常使用只需 Markdown 指令。测试中的 Jev SDK 契约检查使用 mock，不发送真实 API 请求。
