# 2026-10-07：更短的决策流程与独立成品验收

本轮重写了 skill 主流程，保留“调查现有解决方式，再作出选择”的目的，把选型责任、反例检查和实际交付接在一起。评测使用两组联系人导入对照和一组新题对照；功能结果与研究依据分别报告，不合成通用质量分数。本报告记录发布前冻结的候选与评测，运行过程未修改全局安装。

## 本轮改动

入口从上一轮候选的 1,828 个空白分词、237 行，缩到 1,224 个、150 行；已发布版为 1,920 个、243 行。这是文本长度，不能当作 token 消耗或质量提升。原先交叠的要求整理成四段：保留用户契约、解决关键选择、实施选择、用反例检查成品。

- 明确保留用户已经选定的技术、产物和方法；后续消息改变手段时，继续追踪原目标。新功能仍需适量调查，机械修改保持轻量。
- 单个可逆功能用“问题 → 实查证据 → 选择 → 关键检查”记录即可。多功能、跨会话、高风险工作才使用完整台账，常规实现不重复索要确认。
- 选择自研前，比较接手的完整契约和错误处理责任；不能只凭代码短或依赖少来排除可信方案。证据不足的候选保持条件式判断。
- 对外部输入和状态修改，先明确接纳或部分成功策略，再检查足以到达写入路径的近似有效反例；观察操作完成后的实际数据和反馈。没有在 skill 中写入本题的 CSV 测试答案。
- 条件参考文件继续覆盖来源访问失败、恢复、兼容和执行证据；可选 Jev 不变成运行依赖，也不能代替验收。

结构取舍参考了 [Agent Skills 编写指南](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices)的简洁与按需展开原则，以及[上下文工程说明](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)对有效上下文的讨论。这里是否有用，仍由下面的执行结果判断。

新增的 [trace_index.py](trace_index.py)只供维护者审计日志：按 ID 配对调用与返回，记录行号、哈希、缺失/重复/拒绝/错误，不复制原始提示、参数和结果正文。它不判定来源真假或任务通过。5 项专门测试覆盖乱序配对、结构异常、输出保护、内容省略及孤立 Unicode surrogate；后者曾导致指纹计算崩溃，现会记录畸形行并继续索引其他记录。日常使用 skill 无需运行此工具。

## 冻结方法与宿主

版本映射在运行前固定：`m1`、`m4` 和 `x1` 使用已发布的 `8a52431`；`m2`、`m3` 和 `x2` 使用本轮候选。联系人两组的版本启动顺序相反。先执行一次能力预检，再执行六次实现；每次上限 600 秒，并发两个，没有失败重抽。实现进程没有得到隐藏验收标准、旧答案或评审结论。

新题是离线 Python 阅读清单的 Markdown 交接导出。设计者没有读取候选 skill、旧答案或旧产物，但读过包含历史 CSV 失败的记忆摘要，因此不是完全未知历史背景。验收在实现前纠正了过度限定：不强制复用指定 helper，不强制 stdout，不指定命令拼写。复用既有 helper 属研究观察，与六条功能要求分开。

Windows 原生 Claude Code 2.1.281 上报模型为 `deepseek-v4-flash[1m]`；没有改模型或 provider，没有独立核实后端身份。这不是 Anthropic Claude 模型的效果证明。Node 24.14.0、Python 3.12.10、Playwright 1.57.0、Edge 154.0.4258.62。六试次工具库存和 skill 库存哈希分别一致。

本轮把 `/research-first` 放在位置提示开头，并要求成功 Read 项目入口。六份配对工具结果中的完整入口都与相应项目快照一致，运行后所有 skill 文件原始字节哈希未变。请求的工具集合包含 Skill，但实际工具池没有独立 Skill 工具；不把 Read 当作原生 Skill 调用成功，也不把显式调用结果当作自动触发证明。

每个进程关闭自动记忆，显式清空 MCP，使用相同的 Bash/PowerShell 命令规则，把 TEMP/TMP/TMPDIR 指向各自项目，并以文件工具 deny 规则限制用户目录。这些是本次启动参数，没有改全局配置，参见 [auto memory](https://code.claude.com/docs/en/memory#enable-or-disable-auto-memory)、[CLI settings](https://code.claude.com/docs/en/cli-reference)和[文件权限规则](https://code.claude.com/docs/en/permissions#read-and-edit)。原生 Windows 的 shell 没有操作系统级沙箱，命令许可不能约束任意程序的所有文件写入，见[沙箱边界](https://code.claude.com/docs/en/sandboxing)。没有使用会改变用户配置加载或认证方式的隔离参数。

上述宿主说明、记忆控制和明确读取入口的方式都与上一轮不同，因此只在本轮内比较，不能把跨轮差异单独归因于 skill。冻结提示、标准、原始字节哈希、完成状态、归档范围和重建结果见 [power protocol](2026-10-07-power-protocol.json)。

## 独立功能验收

六个 CLI 均正常结束，但功能判定来自独立执行。联系人通过 headless Edge 的真实页面按钮和文件选择器导入，每种场景使用全新上下文，阻断 HTTP(S)。阅读交接通过实际 CLI 导出文件，并核对原命令输出、文件内容和源 JSON 哈希。

| 任务与试次 | 已发布版 | 本轮候选 |
|---|---|---|
| 联系人，第 1 组 | `m1`：4/5；311.95 秒 | `m2`：5/5；145.66 秒 |
| 联系人，第 2 组 | `m4`：4/5；223.91 秒 | `m3`：5/5；199.34 秒 |
| 阅读交接，新题 | `x1`：6/6；162.58 秒 | `x2`：6/6；176.89 秒 |

时间是模型实现进程耗时，不包含独立验收，也不等于成本或稳定速度提升。五条联系人要求覆盖样例中的 Unicode 和引号逗号、原数据保留、重复导入、缺少必要表头后的拒绝与恢复、未闭合引号处理及无外部运行服务，其中原数据保留与真实样例归在同一条。阅读交接六条要求覆盖原命令、选择与顺序、Markdown 内容、指定 UTF-8 文件、空选择及离线运行/源数据保留。

两次已发布版的同一项失败都是：以下输入实际增加了第 4 位联系人，且显示成功，没有拒绝或明确跳过坏行。

```csv
姓名,邮箱,公司
星野,malformed@example.test,"unterminated, value
```

两次候选都拒绝了该输入并保留原三条记录，其余四条功能标准也通过。实现轨迹还显示候选自己执行了失败反例；独立验收再次从界面验证结果，没有修改失败产物。这是本轮最明确的改善信号，覆盖范围限于冻结场景。

阅读交接两边都检查并复用了既有 Markdown 链接 helper，六条功能要求均通过；两份实际交付的 Markdown 文件字节相同。候选还执行了两个本地 Markdown 解析器检查，以及非布尔选择值导致误导出、空备注等反例。它们属于额外观察，不提高冻结标准的分母，也不证明同事实际阅读器里的显示效果。

## 研究依据与范围不能随功能一起判满分

候选 `m2` 明确披露 PapaParse 页面未能读取、许可证和体积未核实，区分自制 GB18030 字节样例与真实 Excel 导出，也没有用自测数宣称跨浏览器通过。这比把搜索线索当作事实更准确。但原联系人代码和 README 并不自动构成“检查过可比产品的导入流程”；该项需要单独证据。

`m3` 的选型段使用约 20 KB 体积参与取舍，后文又说明没有独立测量；其“已确认中文 Excel 保存为 GBK”的表述也不能由一个合成字节样例建立。最终回答即使附上局限，前面的确定说法仍应收窄。不能因为五条功能检查通过，就认可所有兼容和选型陈述。

补充来源复核确认，npm 的 `dist.unpackedSize` 不能替代具体压缩文件的体积测量；已测引号、换行等 CSV 用例也不建立完整 RFC 4180 一致性。`m1`、`m4` 的 C4 记录为实际功能失败，没有据此推断它们曾承诺拒绝所有畸形 CSV。核对范围、未审项目和事件定位见[联系人来源审计](artifacts/2026-10-07-power-contacts-source-review.json)。

阅读交接两边对本地 helper 的检查和复用有配对工具结果支撑。`x1` 的 CommonMark 正文抓取被拒，后续通用搜索只提供线索；不能补称已读规范正文。`x2` 没有发起 WebFetch/WebSearch，使用本地实现与实际渲染输出解决这个离线小任务；合理复用不以网络搜索次数计分。详情见[交接来源与声明审计](artifacts/2026-10-07-power-handoff-source-review.json)。

本轮功能评审及后续来源复核只检查必要工具结果，在按调用参数分类后跳过 `.claude` 入口和参考正文，不知道版本映射。协调器按冻结标准复核初评，指出不能把本地代码检查直接计为外部流程调查；因此研究判断是经过协调器复核的定性判断，不是无干预的客观质量分数。

六试次显式 Write/Edit 调用没有项目外文件路径，所有运行副本保持冻结哈希。但这不是 shell 或文件系统完整审计，也不能把差异归功于 skill：本轮两条件都关闭了自动记忆并增加相同范围约束。`x1` 还有一处值得保留的边界问题：PowerShell 多路径 Remove-Item 被拒后，换用 Python 执行同一清理动作。替代调用成功不等于已获得授权，应与去掉无关复合命令后的合法重试分开看。

## 公开产物与复跑

| 原始夹具 | 已发布版产物与验收 | 候选产物与验收 |
|---|---|---|
| [联系人](fixtures/contacts/README.md)，第 1 组 | [m1 patch](artifacts/2026-10-07-power-contacts-m1.patch)、[验收](artifacts/2026-10-07-power-contacts-m1-acceptance.json) | [m2 patch](artifacts/2026-10-07-power-contacts-m2.patch)、[验收](artifacts/2026-10-07-power-contacts-m2-acceptance.json) |
| 联系人，第 2 组 | [m4 patch](artifacts/2026-10-07-power-contacts-m4.patch)、[验收](artifacts/2026-10-07-power-contacts-m4-acceptance.json) | [m3 patch](artifacts/2026-10-07-power-contacts-m3.patch)、[验收](artifacts/2026-10-07-power-contacts-m3-acceptance.json) |
| [阅读交接](fixtures/reading-handoff/README.md) | [x1 patch](artifacts/2026-10-07-power-handoff-x1.patch)、[验收](artifacts/2026-10-07-power-handoff-x1-acceptance.json) | [x2 patch](artifacts/2026-10-07-power-handoff-x2.patch)、[验收](artifacts/2026-10-07-power-handoff-x2-acceptance.json) |

先把相应原始夹具复制到仓库外的新目录，再应用其中一个 app patch。补丁保留失败，不是推荐的应用实现。六份 app patch 都经过 `git apply --check` 和实际应用，归档文件原始字节与对应试次一致。

公开候选 skill 可从 `8a52431` 的新副本应用 [Git 基础补丁](artifacts/2026-10-07-power-candidate-git.patch)重建；它以实际 Git blobs 为基础，将目标运行文件规范为 LF。独立新 clone 重建后的 19 个文件均与候选规范化哈希匹配。另保留[原始字节补丁](artifacts/2026-10-07-power-candidate.patch)，其基础是本次冻结的已发布版工作副本；它重建 19/19 原始字节哈希。该工作副本有 7 个文件与 Git blobs 仅换行不同，两套哈希和补丁用途不可混用。协议保存各自的验证边界。

已有的[导入反例检查](verify-contact-import.py)可复跑本轮关键失败；它只覆盖未闭合引号，不代替完整五条验收。新增[阅读交接检查](verify-reading-handoff.py)可复跑本轮两个归档产物，按实际帮助输出适配参数；其 Markdown 格式解析针对这两个产物，不是任意实现的通用判官。

```bash
python evals/discovery/verify-contact-import.py --app-dir ../contacts-app --output-dir ../contact-check --channel msedge
python evals/discovery/verify-reading-handoff.py --app-dir ../handoff-app --baseline evals/discovery/fixtures/reading-handoff/reading_shelf.py --output-dir ../handoff-check
```

交接检查仅需 Python 标准库，要求新的项目外输出目录，每个子进程设 15 秒上限。两份归档产物复跑返回 0；未实现 export 的原始夹具作为负对照返回 1。已有输出目录和项目内输出路径都被拒绝；额外 BOM/LF 诊断不计入冻结功能标准。受测子进程没有 OS 沙箱，只应对这些已知夹具使用。浏览器检查另需维护者安装 Playwright 和 Edge，这些都不是普通 skill 使用依赖。

公开 JSON 将机器路径替换为 `<round>`、`<repo>`、`<user-home>`，保留观测值；联系人研究审计与功能记录分开归档。自己复跑得到的 JSON 和终端输出仍包含本机路径及执行诊断，先保留在本地，分享前检查并替换私人路径。原始宿主日志、完整调用参数、截图和索引留在本机。trace index 在六份日志中配对了 266 次调用与返回，包含 18 条权限拒绝关联和 39 条工具错误，没有缺失、重复、孤立或畸形记录；这些统计只说明日志结构，不说明动作都成功或符合范围。

包结构和 skill 格式校验通过，维护测试共 37 项通过、无跳过；可选 SDK 的测试使用 mock，没有调用外部服务。静态检查、字节重建、CLI/浏览器功能验收和来源审计各自报告，不互相替代。

## 结论与下一道门槛

本轮最有力的结论是：较短的新入口在两次联系人试验中都生成了能挡住既有失败输入的实现，同时通过新题的六条功能要求。功能上的进步有可复核产物支持，研究依据与范围遵守仍不能统称全部通过。

只有两个任务、两组同题回归和一组新题，没有无 skill 条件，也没有第二种模型配置；它们不足以证明普遍稳定提升。自动触发描述未修改，本轮也未重测隐式触发。下一道门槛是用真实用户任务检验可比流程调查是否改变选择，以及切换到另一套实际模型配置后重复关键对照；继续保持成品、来源依据和成本分开报告。上一轮失败记录完整保留在[执行证据测试](2026-10-07-execution-evidence.md)，不被这次进步覆盖。
