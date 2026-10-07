# Windows Claude Code：调研价值与成品验收

本轮确认 research-first 在本机 Windows Claude Code 上能触发，并能带来有用的调研与实现细节；同时发现成品边界错误、过宽保证和缺乏依据的选型理由。不能把这些结果概括成“所有任务通过”或“质量已稳定提升”。这是诊断性评测，不是通用质量认证。

## 环境和比较边界

- Windows 原生 Claude Code **2.1.281**，保留现有配置。CLI 上报模型 `deepseek-v4-flash[1m]`，部分事件为 `deepseek-v4-flash`；这个标识不独立证明后端实际模型，也不代表测试过 Anthropic Claude 模型。
- 基线为 `c94db861ede29f3d718ea6be1dc1b0f1875cb88a`。候选仅在 `SKILL.md` Step 9 增加一段：检查成品与最终答复中的承诺，限定输入、环境与失败阶段，以反例检查重要概括，并走完新手所用平台的后续步骤。其 SHA256 见 [manifest](artifact-manifest.json)。
- 每项任务使用新进程、独立 git 项目和 `.claude/skills/research-first` 副本，显式 `/research-first` 调用；worker 只看到原始提示与 fixture，不看到验收标准或上一次输出。自动触发另见 [五项宿主测试](2026-10-02-windows-host.md)。
- 任务上限各 600 秒，均正常完成。使用 `acceptEdits` 与单次调用的工具 allowlist；没有切换 provider、修改全局 skill 安装、推送或发布。
- 实现 worker 的浏览器工具被拒，所称 25/25、23/23 或 61/61 不是独立浏览器验收。维护者另外用真实 Edge 和新复制的 Python fixture 检查成品。
- 本轮没有同条件无 skill 对照，也没有足够重复次数。回归是同题重跑，只有阅读列表是新的 forward case；不能把一次差异全部归因于新增指令。

## 基线产物

### 联系人 CSV 导入

运行 134.56 秒；保存了 [原始 fixture](fixtures/contacts/index.html) 与 [实现补丁](artifacts/contacts-baseline.patch)。

独立 Edge 验收中，示例通过可见界面导入，保留 3 条原记录，新增 2 条、跳过 1 条重复；中文、引号包围的逗号字段均保留。重复导入不会继续新增；缺少姓名表头时给出错误，之后可重新选择有效文件。22 个检查通过。

**另有 2 个检查失败：**引号未闭合的 CSV 被当作有效记录追加，整个剩余内容进入姓名，邮箱和公司为空，界面却报告成功。解析器在文件结束时没有拒绝未结束的引号字段。因此这一产物的核心错误处理没有完整通过，不能以其自报的 Node 25/25 代替验收。

来源检查显示，worker 实际查阅 RFC 4180 和 PapaParse 资料；引号内换行和双引号转义进入了实现。邮箱去重来自任务与本地示例推断，没有证据证明它来自对某个联系人产品流程的调研。PapaParse 的体积等成本论据也缺乏充分的一手材料支撑。这里有实现契约调研价值，但尚未证明用户期望的产品流程发现能力。

### 新同事上手说明

运行 172.45 秒；保存了 [原始工具](fixtures/onboarding/receipt_summary.py) 与 [生成的说明](artifacts/onboarding-baseline.md)。代码与示例数据哈希未改变。

新复制的原始工具在 Windows Python 3.12.10 下，首次运行、查看实际 JSON、重复运行报错和 `--overwrite` 恢复均通过。独立的 15 个运行检查还确认 UTF-8 BOM/CRLF、编码拒绝和金额格式等事实；这个数量表示运行事实核对成功，不表示文档所有主张正确。

文档有四处需要修正：

1. “Excel 导出的 CSV 可以直接用”过宽：本工具支持 UTF-8（可带 BOM），同样中文数据的 GBK 文件实际报错。
2. “合计为 0 就输出 `"0"`”不成立：输入 `0.00` 实际输出 `"0.00"`。
3. “报错不会留下半成品文件”超出证据：已验证的是数据校验失败先于写入；代码直接写最终文件，没有验证所有写入故障。其他 I/O 失败的风险来自代码路径推断，不是已复现的运行失败。
4. macOS 只在版本检查处提示换成 `python3`，后续操作仍写 `python`；macOS 没有实测。

worker 在撰写前实际查阅了 Diátaxis tutorial 指导，成品将首次获得结果、错误恢复和参考信息组织成新手可用的路径。这是有价值的文档设计调研；但好的结构没有消除事实误差。

## 候选修正与复验

候选新增的验证段落没有列入 CSV、GBK、零金额等答案，也没有改变 description 或要求更多来源、更多功能。目的是检验“承诺与证据范围一致”这一通用原则。

### 原题回归：上手说明

运行 104.05 秒；[候选说明](artifacts/onboarding-candidate.md)保留原代码与示例，改为直接扩写 README。明确要求 UTF-8 并提供编码错误恢复，删除了关于零金额和所有错误都不留半文件的两句错误概括。Windows/macOS 的首次运行分别列出命令。

不过，候选仍把错误中的 `Row N` 称为文件行号，而 CSV 空行会影响这一对应关系；覆盖恢复段又只列 `python`。最终答复声称“每一条断言都用真实执行验过”，同时承认 PowerShell/macOS 未实测。这说明问题得到部分改善，但这段新增指令没有使证据约束变得可靠。

同组 15 个独立运行检查再次通过，新增的空行行号检查失败：物理第 4 行的错误实际报告为 `Row 3`。候选关于“中文 Windows Excel 默认 GBK”的说法也未被本地编码探针证明；该探针只证明工具不能读取这份 GBK 文件，不能证明所有 Excel 版本的默认导出设置。

### 新题：阅读列表备份与恢复

运行 192.00 秒；提示、哈希与预先冻结的标准见 [forward case](forward-case.json)，产物见 [实现补丁](artifacts/reading-list-candidate.patch)。要求仅为跨电脑备份、误操作恢复，以及覆盖当前列表前可确认；未指定库、格式或界面。

独立 Edge 154.0.4258.48 验收有 18 项通过、1 项失败，另有 2 项仅记录观察。通过项包含本地页面加载、备份下载、中文/引号/换行/状态往返保留、覆盖前显示影响与确认、取消和 Esc 保留当前数据、无效 JSON 拒绝以及选择文件恢复。`file://` 下的下载与恢复也在这台机器上实际运行；没有测试第二台实体电脑、Chrome 或 Firefox。

失败的是未知版本输入：将生成的封装 `version` 改为 `999` 后，程序仍进入确认并恢复，报告成功。实现输出 `app/version` 元数据，导入时却没有检查它们。因此备份主路径有效，但预先冻结的“不支持的备份格式不得直接应用”标准没有通过。

选型说明还有两个已独立核查的问题：`confirm()` 支持传入消息字符串，因此“无法显示数量”不是成立的排除理由。[MDN confirm](https://developer.mozilla.org/en-US/docs/Web/API/Window/confirm)

对“Chrome 所有 `file://` 页面共享存储”的概括也没有足够证据。当前平台文档将 `file:` 的 localStorage 行为列为未定义、可能因浏览器而异，不能保证一个统一规则。[MDN localStorage](https://developer.mozilla.org/en-US/docs/Web/API/Window/localStorage)

文本备份备用通道具有潜在使用价值，但当前 trace 不足以证明其下载失败前提适用于目标环境；本次 Edge 的 `file://` 下载实际成功。独立评审在四个维度分别给出相关性 2、增量价值 1、调研贡献 1、选择校准 1（每项 0–2，不相加）。这轮更明显的问题是用不充分的理由排除替代方案，而不是缺少搜索次数。

## 这轮改变了什么

1. 修正中英文 README 的 Claude Code 安装路径与 `/research-first` 调用方式，补 Windows PowerShell 示例和同名副本优先级说明。
2. 在技能的验证阶段补充一段通用的成品承诺检查；回归结果支持保留该方向，但不支持宣称它已经解决模型过度概括的问题。
3. 建立可继续复跑的触发、发现价值与成品验收用例，保留失败输出；不会把“CLI success”“有引用”“测试很多”直接计为质量通过。

下一步优先验证两个能力：以实际产品流程寻找更好的使用方式，以及对关键选型理由/失败恢复做独立复核。当前证据不足以支持“可不经验收放心交付成品”的宣传；也不足以据此否定它作为调研工作指导的用途。

## 复现与证据

使用 [cases.json](cases.json) 的原始提示，仅复制选定 fixture 与冻结 skill 到独立目录。基线取 `c94db86`；候选需同时核对 [manifest](artifact-manifest.json) 中的 skill SHA256；若 checkout 转换了换行，另有 LF 归一化哈希用于比较正文，实际运行字节哈希仍保留。原始失败产物保存在 `artifacts/`，请不要原地修补后再把它标为原始输出。

实际 full trial 参数为 `-p --output-format stream-json --verbose --no-session-persistence --permission-prompts none --permission-mode acceptEdits`，另外提供以下 `--allowedTools`：

```text
Skill Read Write Edit Glob Grep WebSearch WebFetch
Bash(python *) Bash(python3 *) Bash(node *) Bash(npm *) Bash(npx *) Bash(pnpm *)
Bash(git status*) Bash(git diff*) Bash(git ls-files*) Bash(rg *)
```

通过 Python subprocess 参数列表启动 Windows 原生 `claude.exe`，提示以 UTF-8 stdin 输入；不要直接拼接包含 `$research-first` 的多层 shell 字符串。每条原始结果记录退出码、超时状态、CLI/model 标识、耗时与工具事件。宿主级 MCP 和插件会影响工具可用性，allowlist 不是全局隔离沙箱。

本机原始日志、冻结设计、浏览器截图、独立验收脚本与详细结果位于 `D:\research-first-review\2026-10-02\next-stage-eval\`，其中 `discovery/acceptance` 为基线与上手说明复验，`candidate/acceptance-forward` 为阅读列表验收。原始 host 初始化信息未复制到公共仓库。CLI 返回的费用字段 `costBasis=unknown`，不作为真实账单。

维护校验通过：包结构及 Markdown 本地链接、4 个 JSON 文件、9 个原始 fixture 文件哈希、4 个产物哈希、候选 SKILL 哈希，以及两份补丁在对应原始 fixture 上的 `git apply --check`。宿主触发副本的 12 文件还分别核对运行字节与 c94 Git blob；其中 6 个存在换行差异，全部 LF 归一化后内容一致。此类维护校验不替代上面的失败项。验收服务 4421、4422 均已关闭。
