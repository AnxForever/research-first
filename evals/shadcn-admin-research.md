# Tasks 批量 CSV 导出：实施前调研

调研日期：2026-09-22。调研者：独立执行调研的 agent。本文保留实施前状态；最终结果见 [验证记录](README.md)。目标仓库：`shadcn-admin`。本阶段只调研；未实现导出、未安装依赖、未执行项目测试或构建。根 agent 提供了正在运行的开发服务器，本调研仅在独立浏览器 session `rf-export-research` 中读取页面并改变临时行选择。根 agent 的其他调查结论和实验输出未读取。

## 1. 原始请求与理解

**唯一模拟产品请求：**“让 Tasks 页的批量 CSV 导出真正可用，导出的文件要能用于后续整理任务。”

- **目的：**用户选中一批任务后，得到能在电子表格中识别、筛选、排序和继续整理的真实文件；应保留任务身份、完整标题及分类，而非只有成功通知。
- **明确约束：**Tasks 页、批量、CSV 是指定交付物；仅在隔离仓库内实施，不推送上游，不改其他项目。本阶段停在调研，后续由根 agent 下发实施阶段，不要求用户重复许可。常规方案与依赖选择已获授权。
- **候选手段：**现有导出按钮可复用；CSV 序列化库、原生浏览器下载或完整表格导出组件是待比较手段，用户没有指定库或新架构。
- **假设：**“后续整理”优先包含 Excel/LibreOffice 等电子表格及常规 CSV 工具；没有证据要求指定第三方导入格式、服务器报表、云端上传、定时导出或 XLSX。
- **遗漏但必要的维度：**导出哪批行、排序/筛选/分页的关系、列与字段完整性、特殊字符/中文、公式注入、空选择、失败重试、浏览器下载状态与资源回收。
- **理解信心：**目的高；主要消费软件与是否需要所有 mock 元数据为中。采用明确且可逆的五字段 CSV 契约，不假装已确认 Excel 所有地区设置或完整数据迁移需求。
- **调研深度：**Standard。数据输出功能包含多个独立失败点，但当前仅 100 行客户端演示数据，没有必要引入后台任务、流式导出或新的权限系统。

## 2. 已知现场与可定位证据

仓库基线 `e16c87f213a5ba5e45964e9b67c792105ec74d26`，项目 2.2.1。`git log -5 --oneline` 为依赖升级/格式调整；没有把历史提交当成导出行为的证据。首次 `git status --short` 为空；后续出现 `src/routeTree.gen.ts` 修改，根 agent 告知是其安装/构建产生的行尾变化。本 agent 未写目标仓库文件。

以下 L 证据均为**实际读取的本地源代码**，路径相对上述目标仓库，行号对应该基线。

| ID | 位置与短原文/直接观察 | 能证明什么 |
| --- | --- | --- |
| L1 | `src/features/tasks/components/data-table-bulk-actions.tsx:59`：`toast.promise(sleep(2000), ...)`；:64、:69：`table.resetRowSelection()` | “导出”只等待并提示，整个 handler 无 CSV/Blob/下载调用；且立即清空选择。不是已经部分可用的下载实现。 |
| L2 | 同文件 :31 与 `src/components/data-table/bulk-actions.tsx:35`：`table.getFilteredSelectedRowModel().rows`；共享组件 `if (selectedCount === 0) return null` | 导出入口与计数基于筛选后已选行；空选择不出现工具栏。 |
| L3 | `src/features/tasks/components/tasks-columns.tsx:17`：`table.toggleAllPageRowsSelected(!!value)`；`tasks-table.tsx` 配置 core、filtered、pagination、sorted 模型，无 `manualPagination` | 页头全选只选本页；完整数据保留在客户端；不能误用当前页模型导出全部已选任务。 |
| L4 | `src/features/tasks/data/schema.ts:5`：`id, title, status, label, priority` 五个 `z.string()`；`tasks-mutate-drawer.tsx` 的 formSchema 也是 title/status/label/priority | 目前正式 Task 类型及编辑界面只承诺五个字段。 |
| L5 | `src/features/tasks/components/tasks-columns.tsx`：标题 cell 同时显示 label Badge 与 `className='truncate font-medium'` 的 title；status/priority 从映射查显示名 | 不能抓取表格渲染文字来编码 CSV；label 必须独立一列，标题应取完整原始字符串。 |
| L6 | `src/features/tasks/data/tasks.ts:6`：`Array.from({ length: 100 })`；:23–27 包含 createdAt/updatedAt/assignee/description/dueDate；`index.tsx` 把 tasks 直接传 TasksTable | 100 行 mock 对象确实带额外元数据，但未进入 Task 契约。此差异是已检视的边界，不能说仓库里根本没有这些字段。 |
| L7 | `tasks-import-dialog.tsx:53` 的 onSubmit 仅 `showSubmittedData(fileDetails, ...)`；导入测试 :52 标题为 “calls showSubmittedData and closes…”；批量 status/priority handler 同样 sleep/toast | 当前 Import、状态/优先级修改仍是演示功能；不能许诺 CSV 能通过当前 Import 真正回导或导出已保存的修改。它们属于范围外历史缺口。 |
| L8 | `package.json` / `pnpm-lock.yaml:4824`：React 19.2.5、TanStack Table 8.21.3、TypeScript ~6.0.3、Sonner 2.0.7、Radix/本地 Shadcn、tw-animate-css 1.4.0；未列 CSV 库。`vite.config.ts:24`：Vitest browser enabled / Playwright / Chromium | 复用现有表格、按钮、提示与测试框架；新 CSV 库是新增依赖。README 明示部分 Shadcn 组件针对 RTL 有定制。 |

**B1 独立浏览器观察（agent-browser 0.37.1）：**打开 `http://127.0.0.1:4173/tasks`，初始页显示 10 行，页码到 10；无选中时没有 Export tasks。勾选 TASK-9366 后出现工具栏，文本为 `1 task selected`，包含 Export tasks。翻到第 2 页后计数仍为 `1 task selected`。第 2 页快照保存于 `本地调研快照目录（未随仓库分发）\local-page2-selection-snapshot.txt`。未点击导出/未捕获下载，故“当前不生成文件”结论来自 L1 的完整控制流，不冒充下载测试结果。

## 3. 外部证据：实际检视而非候选名称罗列

所有网页于 2026-09-22 读取。文档网页未声明版本的，以下明确以访问日标记；可版本化的核心代码已固定 tag/commit，并保存文本副本在 `本地调研快照目录（未随仓库分发）`。`agent-browser read URL` 部分站点超时，随后用同一独立 session `open URL` + `get text body` 成功检视正文/原始代码。

| ID | 来源、版本、短原文/实际观察 | 改变或支持的决定 |
| --- | --- | --- |
| E1 | [Linear 官方 Exporting Data](https://linear.app/docs/exporting-data)，访问日版本：“Export data … to build custom reports, keep records”；issue-view CSV 的字段列举含 `ID … Title, Description, Status … Priority … Assignee, Labels …` | CSV 是可继续整理的任务数据制品；保留任务 ID 与独立分类有产品先例。Linear 的全部字段不能机械复制到本地五字段契约。其管理员/导出上限属该产品，不能推导本项目也需要权限/配额。 |
| E2 | [MUI 官方 Data Grid export](https://mui.com/x/react-data-grid/export/)，访问日版本：“exports the selected rows if there are any”；`fields` 令列“exactly those … in the same order”；提供 filtered/sorted/page selectors；“By default, the formulas in the cells are escaped.” | 显式列顺序、选中行导出、排序/分页分离、公式保护是成熟组件的真实选择。它的默认“无选择则导出全部”不适合本地仅批量入口，应适配而非照抄。 |
| E3 | [Material React Table V3 CSV 示例](https://www.material-react-table.com/docs/examples/export-csv)，实际读正文及 TS 示例：“does not have a data exporting feature built in”；使用 `mkConfig, generateCsv, download`；:47–50 `rows.map(row => row.original)`；:83 “including from the next page … respects filtering and sorting” | 可以把现有 TanStack 行模型接到独立 CSV 库，无需换表格。示例的 `getSelectedRowModel()` 不尊重本地过滤计数，不能直接复制。 |
| E4 | [TanStack v8 row-selection guide](https://tanstack.com/table/v8/docs/guide/row-selection)：“getFilteredSelectedRowModel() … after filtering”，“getGroupedSelectedRowModel() … after grouping and sorting”；[v8.21.3 RowSelection.ts](https://github.com/TanStack/table/blob/v8.21.3/packages/table-core/src/features/RowSelection.ts#L346)，实际源代码 :346–363 分别依赖 `getFilteredRowModel()` 与 `getSortedRowModel()` | 筛选后的选择本身不保证排序；推荐从已过滤且排序的全量行模型筛选 getIsSelected，覆盖全部页。必须使用 v8 资料。 |
| E5 | [Papa Parse 文档](https://www.papaparse.com/docs#json-to-csv)，Papa Parse 5：“object explicitly defining fields and data”；`newline` 默认 CRLF；`escapeFormulae` 接受 boolean 或 regexp。实际 [5.7.0 源码](https://github.com/mholt/PapaParse/blob/5.7.0/papaparse.js#L365) :365–400 的 safe() 会双写内部引号、必要时包引号；:294–297 允许自定义 regexp。 | 有明确字段、稳定编码、可定制公式保护，适合复用。不能仅设置默认配置就宣称安全。 |
| E6 | [Papa Parse 5.7.0 上游测试](https://github.com/mholt/PapaParse/blob/5.7.0/tests/test-cases.js#L1859) 实际查看 “Data with newlines”、quote 测试，:2110 “Escape formulae”、:2140 “Escape formulae with tab and carriage-return”。[npm 5.7.0 元数据](https://registry.npmjs.org/papaparse/5.7.0)：MIT，gitHead `555c1c1b6175e7a043adf8694983776a1e6fdeeb`，main `papaparse.js`、browser `papaparse.min.js`，未声明 runtime dependencies/types | 检视了行为核心和测试，不只 README。需要 TypeScript 声明包或经检查的类型方案；库有解析等本次不用的能力，bundle 实际增量尚未测量。测试只是阅读，未运行。 |
| E7 | [export-to-csv 1.5.0 npm 元数据](https://registry.npmjs.org/export-to-csv/1.5.0)：MIT、ESM、自带 `./output/index.d.ts`，无声明 runtime dependencies；gitHead `68a4082fa8b849d8e929820f9824cecafabf2115`。实际读该 commit 的 [config.ts](https://github.com/alexcaza/export-to-csv/blob/68a4082fa8b849d8e929820f9824cecafabf2115/lib/config.ts)：`useBom: true, escapeFormulas: false`；[helpers.ts](https://github.com/alexcaza/export-to-csv/blob/68a4082fa8b849d8e929820f9824cecafabf2115/lib/helpers.ts#L124) 的 `/^[=+\-@\t\r]/`，:152–172 处理引号/换行。 | 是真实可用的较专注替代品，而且当前 1.5.0 已有公式转义，不能引用旧认知说它完全没有。默认未启用，覆盖仍有边界。 |
| E8 | export-to-csv 同 commit [generator.ts](https://github.com/alexcaza/export-to-csv/blob/68a4082fa8b849d8e929820f9824cecafabf2115/lib/generator.ts)：download 创建 Blob URL、append/click/remove anchor，整个函数未调用 revokeObjectURL；generateCsv 的 `useKeysAsHeaders` 分支读取 `Object.keys(data[0])` | 即使用其下载 helper，也要考虑空数组与资源回收；库不会替我们确定领域列。不能宣称安装后所有生命周期问题自动解决。 |
| E9 | [RFC 4180 §2](https://www.rfc-editor.org/rfc/rfc4180#section-2)，2005，Informational 而非互联网标准：“Fields containing line breaks … double quotes, and commas should be enclosed in double-quotes”；内部引号以另一个双引号转义；记录用 CRLF。 | 逗号拼接不足以交付有效 CSV；明确列数、引号、换行与 `text/csv;charset=utf-8`。不把 RFC 称作严格覆盖 Unicode 的全球唯一规范。 |
| E10 | [Microsoft：Opening CSV UTF-8 files correctly in Excel](https://support.microsoft.com/en-us/office/opening-csv-utf-8-files-correctly-in-excel-8a935af5-3416-4edd-ba7e-3dfd2bc4a032)，访问日版本：“open a CSV file encoded with UTF-8 normally if it was saved with BOM” | 默认 UTF-8 BOM，降低中文双击打开乱码的机会；这不能证明所有 Excel 地区设置的分隔符识别。MUI E2 也公开提供 utf8WithBom 选项。 |
| E11 | [OWASP CSV Injection](https://owasp.org/www-community/attacks/CSV_Injection)，访问日版本：公式起始 `= + - @`、Tab/CR/LF 与全角变体；“There is no universal CSV sanitization strategy … all downstream consumers”；警示 Excel 保存重开可能去掉转义。其 Excel-resistant 段建议危险公式前缀 Tab，并明确 Tab 成为原数据的一部分。 | CSV 引号转义与公式注入是两件事。应有显式输出文本策略，不能声称“任意表格软件、反复另存均安全”或同时保证所有值字节完全原样。 |
| E12 | [MDN download](https://developer.mozilla.org/en-US/docs/Web/API/HTMLAnchorElement/download)，页标日期 2024-07-26：“cannot be used to determine whether the download will occur”；[MDN revokeObjectURL](https://developer.mozilla.org/en-US/docs/Web/API/URL/revokeObjectURL_static)，页标日期 2026-02-09：“Call this method when you've finished using an object URL” | UI 只能如实报告已生成/已发起下载，不能确认用户已保存；需要失败反馈及 object URL 回收。 |

**Context7 使用与版本冲突：**已调用 resolve-library-id 查 TanStack Table、Papa Parse；前者返回 `/tanstack/table` 与 `/websites/tanstack_table_v8`。query_docs 的前者实际返回 main 分支新的 static-function API/v9 perf 笔记，后者仅泛化 table 首页，均不能作为项目 v8.21.3 的精确行为证据。Papa Parse resolve 未命中，返回无关 Parse 项目。故改查 E4/E5 的官方 v8 文档与固定 tag 源码，未将 Context7 搜索结果冒充版本匹配的证据。

**未形成证据的访问：**Airtable 试探路径 404；一条 export-to-csv 非官方猜测域名 DNS 失败，立即改用 npm 元数据里的真实 GitHub 仓库。未从这些失败推断不存在产品/库。BrowserOS neo 不在本会话可调用工具中，按阶段要求使用已读取工作流的 agent-browser。

## 4. 候选选择及代价（独立选择不捆绑）

| 方案 | 已验证能复用的部分 | 剩余本地责任、代价 | 判断 |
| --- | --- | --- | --- |
| **Papa Parse 5.7.0 + 现有 UI + 原生下载** | 明确 fields/data、可靠 CSV quoting、CRLF、自定义 escapeFormulae regexp；检视源码与上游边界测试（E5/E6） | 新运行依赖及 TS 声明；含本次不需的 parser；需自行定义字段、行范围、文件名、Blob/BOM、反馈/清理。真实 bundle 增量待 build | **推荐 Combine**。序列化和公式策略扩展能力更重要；不重写引号转义算法。 |
| export-to-csv 1.5.0 + 现有 UI | ESM、自带类型、BOM、列名映射、generateCsv/download，已有同类 TanStack 集成示例（E3/E7） | 要显式打开 escapeFormulas；LF/全角等策略仍需预处理；自带 download 未回收 URL（E8）。包解压大小较小不等于生产 bundle 差值 | **可行备选**，若优先更专注 API/内建类型可选；无需换任何 UI。 |
| RFC 4180 小型手写 encoder + 原生下载 | 无新增 runtime 包，可限定五字符串字段（L4/E9） | 自己维护特殊字符、空值、公式策略及回归覆盖；省掉包但没有消除问题复杂度 | **可行但不推荐 Build**，当前没有禁依赖约束，现成库已覆盖主要编码责任。 |
| MUI Data Grid 的完整导出组件 / MRT 整表替换 | MUI 实际提供导出状态/字段/格式选项；MRT 示例证明独立库整合可行（E2/E3） | 迁移现有 TanStack/Shadcn/URL 状态和 RTL 定制，增加 UI 系统；MRT 本身也不内置导出 | **Learn-from，不安装**。仅实现一个现有操作无需表格迁移。 |

**组件/动效：**复用当前 Button、Tooltip、已有 bulk toolbar 的键盘行为、aria-label、aria-live 和 Sonner。实际 L2/L8 显示工具栏已经有 CSS transition/hover 动效；本需求没有新增空间转换或等待流程，调查 E2/E3 后没有理由引入 Motion 或另一套菜单。无需新增组件库/动画库；不复制其 UI。共享工具栏的 hover 动效与 reduced-motion 完整审核不在本次导出范围，不能因沿用而宣称已验证所有可访问性。

## 5. 推荐行为与证据到实现的约束

1. **选取范围：**仅导出“当前筛选范围内已选行”，跨全部客户端页；遵循当前排序。工具栏计数应等于 CSV 数据行数（L2/L3、B1、E2/E4）。建议从 `table.getSortedRowModel().rows.filter(row => row.getIsSelected())` 获取，不按任务显示 ID 去重、不用当前页 `getRowModel()`。本地无分组；以后新增 server pagination/grouping 时此决定应重审。
2. **输出契约：**固定列 `id,title,status,label,priority`，下游不受 View 隐藏列影响；label 独立、完整标题；保留 raw 分类值，例如 `in progress`，便于稳定分组/后续程序处理，而不是从显示 Badge 反取（L4/L5、E1/E2/E5）。表头使用稳定字段名而不是本地化 label；这是可逆设计选择，不是用户已经指定的格式。
3. **额外 mock 字段的取舍：**不 `Object.keys(row.original)` 自动导出；已看见 assignee/description/dates，但它们没有 Task 类型/编辑契约（L4/L6）。本次默认五字段，不替用户臆造“完整迁移备份”。如果后续明确需要负责人/到期日等，应先把字段纳入正式 schema、日期格式及验收，再扩展固定列。该取舍可在评审中改变，不被隐藏为事实。
4. **编码：**UTF-8 + BOM、逗号、CRLF、有表头、显式列序、标准双引号转义，读取 raw 字符串，不 trim、不 truncate（E5/E9/E10）。可固定全部字段加引号简化输出检查，但不能把加引号当成公式保护。
5. **公式文本策略：**推荐利用 Papa 自定义 `escapeFormulae` regexp，对 ASCII/全角公式起始字符、Tab/CR/LF 及前导空白后的危险起始进行识别，用其已有前置单引号保护并 quote（E5/E6/E11）。**不能仅用 `escapeFormulae:true`：**5.7.0 源码 :297 默认为 `/^[=+\-@\t\r].*$/`，未列 LF/全角，`.*$` 对内含换行字符串有静态可见的匹配边界；本阶段未执行复现，实施时必须测试 `=1\n+2`。危险字段输出会新增前缀，需在说明中讲清楚；普通字段保持原值。若交付标准变成“Excel 编辑后反复 CSV 另存也保留防护”，应改为 E11 的 Tab 策略并做真实 Excel 验证，不能把当前较通用策略伪称覆盖该场景。
6. **下载与命名：**同步处理当前小数据量，直接发起本地 Blob 下载；文件名如 `tasks-YYYY-MM-DD-HHmmss.csv`（无 Windows 不合法冒号）。移除假两秒等待；同一点击使用同一批任务快照。成功提示写 “CSV download started for N tasks.” 而非“已保存到磁盘”（L1/L6、E12）。
7. **生命周期：**空选择防守返回、不生成空文件；生成/创建 URL/触发异常显示可重试错误；成功与失败均保留选择供继续整理/再次下载（不改变任务数据的设计判断，L1/B1/E12）；删除临时 anchor，恰当延迟回收 URL，异常也清理。具体回收时机需真实下载验收，MDN 没有承诺某一 timeout 在所有浏览器都正确。
8. **范围限制：**不加后台、数据库、CSV Import、完整任务 CRUD、XLSX、下载历史、导出权限/配额。任务数据已在客户端（L6），本地生成不需外传。对现有 import/status/priority 假行为仅记录缺口（L7），不扩大本次实现。

## 6. 功能证据账本（实施前）

所有记录 parent=`TASK-CSV`，优先级均为本次必需。Delivery 与 coverage 分开：代码仍未实施，不能因调研充分标 operational。

| ID / 用户结果与生命周期 | 当前 Delivery | 当前证据覆盖 / 历史缺口 | 决定与接受证据 / 下一步 |
| --- | --- | --- | --- |
| CSV-SCOPE / 导出与已选任务数、过滤、排序、跨页一致 | 现有选择 enabled；导出 planned | partial；inherited-unassessed：原 stub 没有范围证据记录；本次 L2/L3/B1/E2/E4 回填，仍待集成验证 | 用已过滤排序的全页已选行；验收 2 页选择、改变筛选、排序、清空筛选后选择恢复、0 行。 |
| CSV-DATA / 后续可区分、分组、排序任务 | planned | partial；inherited-unassessed：五字段与 raw 元数据差异此前未评估；L4–L6/E1/E2 回填 | 固定五列/原始完整值/独立 label；验收隐藏列不丢字段、额外属性不泄出、英文状态值稳定。 |
| CSV-ENCODING / 正常打开中文、符号及多行字段 | planned | partial；原 stub 无实现；E5/E6/E9/E10 有设计支持 | 解析回读与字节 BOM/CRLF 检查，特殊字符 fixture；真正 Excel 尚未验证。 |
| CSV-TEXT / 公式样式标题按文本输出 | planned | partial；原 stub 未评估；E5–E7/E11 回填但 spreadsheet 再保存边界仍明确未验证 | 显式防护 regex 与测试；有前缀的数据差异说明；不宣称所有应用普遍安全。 |
| CSV-DOWNLOAD / 真文件、可重试、无假完成、资源释放 | planned | partial；inherited-unassessed：原先成功 toast 与 reset 不表示下载；L1/E8/E12 回填 | Blob/anchor/异常/cleanup 测试 + 真实浏览器文件检查；保留选择。 |
| CSV-UX / 可发现、键盘可用、状态真实 | 现有 toolbar enabled；导出行为 planned | partial；继承的 keyboard/aria 仅源码检视，不能当已做完整 A11y 测试 | 复用 L2/L8 与现有标签；实际键盘触发、无行隐藏、错误反馈及无假延迟。 |

历史保留：2026-09-22 建账时均为 `inherited-unassessed` 或尚无实现；本次补充设计依据是 backfill event，但整项仍 partial，因为新行为/文件未验收且外部应用边界未核实。不得把这份报告当作“导出已实现”的证据。

## 7. 发给用户的实施前中文摘要（已准备，供根 agent 发出）

> 现在的导出按钮只有成功提示，没有文件。我会让它导出当前筛选范围内已选的任务，覆盖跨页选择并按当前排序排列；文件固定包含任务 ID、完整标题、状态、标签、优先级，便于后续分组整理，中文和标题中的逗号、引号、换行也能保留。
>
> 我比较了 [Papa Parse](https://www.papaparse.com/docs#json-to-csv)、[export-to-csv](https://github.com/alexcaza/export-to-csv) 和手写编码。建议复用 Papa Parse：它的字段控制和字符转义有现成实现与测试，代价是新增一个 CSV 依赖及类型声明；export-to-csv 自带类型、也可用，但仍要补下载清理和文本保护。按钮和表格继续使用项目现有组件。
>
> 下载会使用 UTF-8 编码，并保护公式样式文本；成功或失败都保留选择，方便继续操作。现有 Import 只是演示，这次不把回导或任务保存算作已支持功能。接下来按这个方案实现并检查实际下载文件。

这一摘要是待发的具体建议，不声称用户已看到/批准新方案；阶段指令已授权常规选型，不新增许可门槛。源码 mock 额外元数据取舍与公式再保存边界保留在本报告，实施验收必须据实披露。

## 8. 下一阶段实施切片与验收（均未执行）

1. 固定 CSV 列和 task-specific 序列化 helper；选择依赖/类型版本并记录 lockfile。将生成字符串与下载副作用分开，以便检查真实字段内容和失败行为；不是先造通用报表框架。
2. 把现有 handler 接到真实下载，移除其 sleep/reset；类型对齐 `Table<Task>` 或等价明确契约，避免未验证泛型强转扩散。按 E12 清理和如实提示。
3. **内容验收：**一条/多条任务；五列恰好匹配；标签独立；包含 `中文😀`、逗号、双引号、CR/LF、前后空格、空字符串；普通值回读保持原样；BOM 字节 `EF BB BF`；行记录 CRLF；多行字段不误增数据行。
4. **公式验收：**`=1+1`、`+...`、`-...`、`@...`、Tab/CR/LF、前导空白、全角变体、`=1\n+2`；字节级确认保护而不是仅使用同一个 serializer 断言“成功”。普通包含中间 `=` 的标题不应被无故修改。记录有前缀时的预期数据变化。源库测试只作设计依据，不能替代项目验收。
5. **表格交互验收：**第一页选一行、第二页再选一行只导出这两行；排序后顺序匹配；筛选隐藏一条后仅导出工具栏所显示的选中数；清除筛选后未销毁原选择；View 隐藏 priority 仍输出契约列；无选择无下载；不修改任何任务内容。
6. **真实制品验收：**用独立 agent-browser session 下载至本次临时目录；检查生成文件名、CSV 内容、行数、字节 BOM，重新用独立 CSV 解析器读入；不把 toast 或 mock anchor.click 当成已下载证据。异常路径确认错误提示、选择保留、anchor/URL 释放；正常释放后已下载文件完整。
7. **项目检查：**按现有 Vitest browser/Chromium 框架做导出范围/内容/失败测试，运行相关测试和 build、lint/格式检查。前序根 agent 的原始项目 build 不是本改动通过的证据。

**剩余未验证：**没有实现代码/输出文件；未执行库或项目测试；尚未安装/验证 Papa TS 声明与生产 bundle 增量；未真实 Excel、LibreOffice、Safari/Firefox 打开文件；分隔符地区设置、Excel 编辑后重存的公式保护无运行证据；大于本地 100 行的数据量/后台分页未测试；用户未明确要求 mock 的五个额外字段，本方案暂不导出。没有把这些项隐藏成已覆盖。

**准备度判断：**本阶段可进入受测实施：目的、范围、主方案与可行备选、重要失败条件已有具体来源和验收计划；没有尚缺授权的用户决策。外部应用兼容性必须保持有界描述。下一阶段由根 agent 下发，不在本报告阶段自行安装或改代码。
