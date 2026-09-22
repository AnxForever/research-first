# 验证记录

2026-09-22：在真实开源项目上完成一次调研与实现试验，并用 Jev 检查几类短证据卡。这里记录实际结果、可复现材料和局限，不把少量案例当成通用效果保证。

## 真实项目试验

项目：[satnaing/shadcn-admin](https://github.com/satnaing/shadcn-admin)，MIT，固定基线 [`e16c87f`](https://github.com/satnaing/shadcn-admin/tree/e16c87f213a5ba5e45964e9b67c792105ec74d26)。试验使用隔离克隆，没有向该项目上游提交修改。环境为 Windows、Node 24.14.0、pnpm 10.28.0、React 19、TanStack Table 8.21.3。

试验请求由本次评估编写，并非上游用户提交的 issue：

> 让 Tasks 页的批量 CSV 导出真正可用，导出的文件要能用于后续整理任务。

原 handler 只有 `sleep(2000)`、toast 和清空选择，没有 CSV 编码或下载调用。这个结论来自完整源码检查；早期浏览器工具超时不算“不下载”的有效测试证据。

一个独立 agent 根据原始请求和 skill 先调研，再在展示选项后实施。查看了 Linear 的导出流程、MUI/MRT 表格导出、TanStack v8 行模型、CSV/BOM/下载 API 文档，以及两个候选库的固定版本源码。完整证据和实施前的逐功能台账见 [调研记录](shadcn-admin-research.md)。

| 路径 | 查到的适配点 | 需要承担的代价 | 最终处理 |
|---|---|---|---|
| Papa Parse 5.7.0 | 显式字段、引号/换行、可自定义公式转义规则 | 新增运行依赖和类型声明，项目仍负责范围和下载 | 采用，固定版本 |
| export-to-csv 1.5.0 | 类型化 ESM、CSV/BOM、下载 helper | 仍需补资源回收和适合当前输入的文本保护 | 向用户展示，未采用 |
| 手写编码 | 五个字符串字段可以自行编码 | 节省依赖，但需维护 CSV 和公式边界 | 向用户展示，未采用 |
| 更换整套表格/UI | 可获得其他导出能力 | 现有 TanStack/shadcn 已满足交互，迁移成本无对应收益 | 保留现有组件 |

调查结果落实到了实现：

- 从已筛选、排序的全量行模型取选中项，覆盖跨页选择；不直接复制第三方示例的行选择器。
- 固定 `id,title,status,label,priority` 五列，保留完整原文，排除未进入 Task 契约的 mock 元数据。
- 复用 Papa 编码，输出 UTF-8 BOM 和 CRLF；检查固定版本实现后扩展公式前缀规则，覆盖测试中的前导换行、空白及全角符号。增加的单引号是数据变化，项目说明中已写明。
- 成功和失败都保留选择，失败可以重试；仅提示“已发起下载”，不声称能确认用户已保存。

### 已执行检查

| 检查 | 结果与范围 |
|---|---|
| 原始项目构建 | 实施前 `pnpm build` 通过 |
| 修改后 Tasks 测试 | 5 文件 / 39 项通过：19 项编码与下载生命周期、4 项真实 TanStack 集成、16 项原有表单测试 |
| 修改后构建与 lint | `pnpm build`、`pnpm lint` 通过 |
| 改动文件格式与补丁 | Prettier、`git diff --check` 通过；补丁在干净基线工作树上 `git apply --check` 通过 |
| 独立真实下载 | Edge 153.0.4234.48：3 份实际文件下载成功，Python 标准库解析并比较五列值、记录顺序、CRLF、BOM；空选择及选择保留检查通过 |

39 项自动化测试中的下载点击使用 spy；这些测试本身不证明文件已经落盘。独立浏览器检查使用真实 `download` 事件和 `saveAs`，没有 mock Blob/anchor，记录及制品如下：

| 实际文件 | 解析结果 | 大小 |
|---|---|---|
| [cross-page.csv](shadcn-admin-browser/cross-page.csv) | 第 1 页 TASK-9366、第 2 页 TASK-9874，共 2 条 | 228 bytes |
| [filtered.csv](shadcn-admin-browser/filtered.csv) | 筛选 TASK-9366 后只有这一条 | 153 bytes |
| [sorted-descending.csv](shadcn-admin-browser/sorted-descending.csv) | 标题降序，TASK-9874 排在 TASK-9366 前 | 228 bytes |

三次 `download.failure()` 均为 `null`，BOM 为 `efbbbf`。清除筛选恢复两页原有选择；清空选择后没有导出按钮或额外下载事件。见 [原始浏览器结果](shadcn-admin-browser/result.json) 和 [可复跑脚本](verify-shadcn-export.mjs)。

先前 agent-browser 0.37.1 / Chrome 153.0.8010.47 的下载路径多次返回 `Download was canceled`，显式指定下载目录也未解决。其根因尚未确定；随后使用项目已有 Playwright 和本机 Edge 下载成功，应用代码没有为此改变。因此只能报告 Edge 路径通过，不能声称已修好该 CLI 或完成跨浏览器验证。

### 复现实现

[实现补丁](shadcn-admin-export.patch) 包含源码、依赖锁定、项目说明和新增测试；原项目版权声明见 [LICENSE.shadcn-admin](LICENSE.shadcn-admin)。下面假设两个仓库位于同一父目录：

```bash
git clone https://github.com/satnaing/shadcn-admin.git
cd shadcn-admin
git checkout e16c87f213a5ba5e45964e9b67c792105ec74d26
git apply --check ../research-first/evals/shadcn-admin-export.patch
git apply ../research-first/evals/shadcn-admin-export.patch
pnpm install --frozen-lockfile
pnpm exec playwright install chromium
pnpm test src/features/tasks
pnpm build
pnpm lint
```

本机测试起初因默认 `::1:63315` 端口不可用及 Playwright Chromium 未安装而未能启动，没有计作通过。最终使用仓库外临时 `.mts` 配置，继承项目 `vite.config`，只将 browser API 改为 `127.0.0.1:4184`、Playwright channel 改为已安装的 `msedge`。未更改上游正式测试配置。其他环境通常可直接使用上面的 Chromium 命令。

真实下载脚本需要 Node、Python、目标项目已安装的 Playwright，以及运行中的应用。在目标项目启动 `pnpm dev --host 127.0.0.1 --port 4173` 后，从 research-first 根目录另开终端运行：

```bash
node evals/verify-shadcn-export.mjs ../shadcn-admin ../new-export-artifacts
```

默认使用已安装的 Playwright Chromium。需要复现本次 Edge 环境时，将环境变量 `CSV_BROWSER_CHANNEL` 设为 `msedge`。输出目录必须是新目录；可选的第三个参数用于指定其他 Tasks 页面 URL。

## Jev 的插入与观测

官方 [模型列表](https://docs.typesafe.ai/models)、[API](https://docs.typesafe.ai/api) 和 [1.13 局限说明](https://docs.typesafe.ai/model-jaggedness/jev-1.13) 于 2026-09-22 核实。使用 `typesafe-sdk==0.7.1`；评估固定 `jev-1.13.0`，单独的真实 `jev-latest` 探针也返回该版本。

每张卡只问一个范围明确的问题，标签和解释不发送给模型。所有预期标签由本次任务的 agent 在查看该轮响应前记录，**没有独立真人标注**。原始概率、模型版本、错误和分歧保留，不用本地规则覆盖模型回答，不调参重跑以美化结果。

| 数据组 | 性质 | 成功调用 | 与预标注一致 | 平均客户端耗时 |
|---|---|---|---|---|
| [12 张边界卡](jev-cases.json) · [原始响应](jev-boundary-results.json) | agent 构造的合成场景，含中文约束、引用内指令、隐藏备选方案、未执行测试 | 12/12 | 12/12 | 1037.2 ms |
| [4 张项目卡](shadcn-admin-before.json) · [原始响应](shadcn-admin-before-results.json) | 从实施前的真实调研派生，含刻意错误的诊断声明 | 4/4 | 3/4 | 1246.8 ms |
| [2 张完成卡](shadcn-admin-after.json) · [原始响应](shadcn-admin-after-results.json) | 真实文件验收后的补充诊断，不属于独立留出集 | 2/2 | 2/2 | 1166.8 ms |

各组结果应分别阅读，不能混成“整体准确率”。项目卡不是四个实际缺陷，也不是四个独立项目。

一次明确分歧出现在选型摘要：摘要提到了手写方案，却没说明其维护成本。预标注为 `contradicted`，Jev 返回 `supported`；原始 confidence 为 `0.47`，概率为 supported `0.64` / contradicted `0.35` / insufficient `0.01`。agent 仍补充了手写方案的依赖收益与维护代价。不能据此说 Jev 发现并修复了这个遗漏，也不能拿这个样本设自动放行阈值。

其余项目卡分别比较了请求解释、旧 handler 的实现声明、以及把计划测试当成已验证结果的声明。Jev 只接收短证据，不会读取源码、查询来源或运行测试；CSV 边界发现来自实际调研。

最后两张卡使用已执行的浏览器结果：Jev 支持了“Edge 实际保存了跨页选中的两条任务”这一有界声明，并把“已验证 Excel 和 LibreOffice 打开文件”的刻意过度声明判为 `insufficient`。后者从未成为实际交付承诺。这演示了完成节点的用法，未产生新的实现修改。

边界卡共 6072 输入 tokens，实施前项目卡 2393，完成卡 1373；按当日文档的每百万输入 tokens $0.042 估算，分别为 $0.000255024、$0.000100506 和 $0.000057666，均不含别名探针。这是计算值，不是供应商账单。耗时包含客户端开销，不等于模型服务端推理耗时。

### 复现 Jev 检查

在 research-first 根目录执行。默认预览不联网，不需要 SDK 或密钥：

```bash
python -m unittest discover -s tests -v
python evals/run_jev_cases.py evals/jev-cases.json preview-results.json
```

本轮在已安装固定版本 SDK 的虚拟环境中运行，适配器与 runner 的 **19 项离线测试通过**，覆盖显式联网、输出校验、错误/超时、模型版本、报告预留及探针失败统计等行为。未安装可选 SDK 时，其中 2 项 SDK 契约测试会跳过。不会把这些本地测试算成模型能力测试。

已启用 TypeSafe 调用、通过运行环境安全提供 `TYPESAFE_API_KEY` 时：

```bash
python -m pip install -r scripts/requirements-jev.txt
python evals/run_jev_cases.py evals/jev-cases.json new-boundary-results.json --live --probe-latest
python evals/run_jev_cases.py evals/shadcn-admin-before.json new-project-results.json --live
python evals/run_jev_cases.py evals/shadcn-admin-after.json new-completion-results.json --live
```

每张卡发送一次，无自动重试；输出路径必须是新文件，既有报告不会被覆盖。首轮边界报告由等价的一次性 runner 产生，早于仓库 runner，故缺少后增的 `mode` 等报告字段；其中 `source: jev`、实际模型和 usage 均来自真实响应。重新运行可能得到不同结果，不要替换历史报告。

## 结论的范围

这次运行表明，skill 可以引导 agent 完成产品/源码/资料调查，给出可复用选择，并把发现落实到功能和验收。只有一个选定项目、一次实现过程，没有“不使用 skill”的对照组，因此不能证明整体成功率提升，也不能证明 Jev 改善了最终实现。

当前建议是在需求理解、证据关联、选项披露、完成声明四个节点按需使用 Jev。模型输出仅供复核，不代替用户选择、证据核验和执行结果。普通 skill 流程无需 Jev、SDK 或 API key。

项目仍使用演示数据；Import、CRUD、后端持久化不在本次任务范围。未验证真实 Excel/LibreOffice、非 Chromium 浏览器、所有地区分隔符、极大数据量或完整无障碍使用。文本前缀保护覆盖已测输入，不承诺任意电子表格软件反复另存后仍保持相同保护。
