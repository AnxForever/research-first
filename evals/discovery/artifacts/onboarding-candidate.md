# 收据汇总

这是团队每周在本机使用的小工具。它读取收据 CSV，生成按类别汇总的 JSON。
目前只有维护者熟悉操作；新同事有 Windows 和 macOS 用户，都已安装 Python。
仓库中的姓名、金额和项目均为演示数据。本工具不会连接财务系统。

---

## 给新同事：五分钟上手

### 1. 准备工作

不需要 `pip install` 任何东西——这个工具只用 Python 标准库。

在终端里确认 Python 可用：

| 系统 | 命令 |
|---|---|
| Windows（PowerShell） | `python --version` |
| macOS（终端） | `python3 --version` |

能打印出版本号即可。若 Windows 上 `python` 无反应，改试 `py --version`。

### 2. 跑一次

先 `cd` 到本仓库目录，然后：

```powershell
# Windows PowerShell
python receipt_summary.py example.csv --output summary.json
```

```bash
# macOS
python3 receipt_summary.py example.csv --output summary.json
```

**这条命令没有任何输出——这是正常的，代表成功了。** 打开 `summary.json` 看结果。

### 3. 结果长什么样

```json
{
  "rows": 3,
  "totals": {
    "交通": "20.50",
    "办公": "39.90"
  }
}
```

- `rows`：成功处理的收据行数。
- `totals`：每个分类的金额合计，按分类名的 Unicode 顺序排列（不是拼音顺序）。

## 每周重复运行：记得加 `--overwrite`

这是最容易卡住的地方。工具**默认不覆盖已有文件**，所以第二周用同样的输出名再跑一次会直接报错：

```
FileExistsError: [Errno 17] File exists: '...\summary.json'
```

解决办法是加 `--overwrite`：

```powershell
python receipt_summary.py example.csv --output summary.json --overwrite
```

（或者换个 `--output` 文件名。）

## CSV 要满足什么格式

```csv
date,category,amount
2026-09-28,交通,12.50
2026-09-29,办公,39.90
```

- 表头必须**同时**有 `date`、`category`、`amount` 三列，顺序不限，多余的列会被忽略。
- `date` 必须存在，但**不参与计算**——工具不按日期分组，也不校验日期格式。
- `category` 不能为空；首尾空格会被自动去掉，所以 `交通` 和 ` 交通 ` 会合并成同一类。
- `amount` 必须是数字且 ≥ 0，不要写成 `12.5元`，也不要用千分位逗号。
- 文件必须是 **UTF-8** 编码（带不带 BOM 都行）。

> **从 Excel 导出时注意**：中文 Windows 上 Excel 的「CSV（逗号分隔）」默认存成 GBK，本工具读不了，会报
> `UnicodeDecodeError: 'utf-8' codec can't decode byte ...`。
> 请改选「**CSV UTF-8（逗号分隔）**」另存一次，同一份内容就能正常处理。

## 出错了怎么查

| 屏幕最后一行 | 原因 | 怎么办 |
|---|---|---|
| `FileExistsError: ... File exists` | 输出文件已存在 | 加 `--overwrite` |
| `UnicodeDecodeError: 'utf-8' codec can't decode byte ...` | CSV 不是 UTF-8（多半是 Excel 存成了 GBK） | 另存为「CSV UTF-8（逗号分隔）」 |
| `ValueError: CSV requires date, category, amount columns` | 表头缺列 | 补齐这三列表头 |
| `ValueError: Row N: category is empty` | 第 N 行分类为空 | 填上分类；N 是文件行号，表头算第 1 行 |
| `ValueError: Row N: amount is not a number` | 第 N 行金额为空或不是数字 | 改成纯数字 |
| `ValueError: Row N: amount must be finite and non-negative` | 金额是负数或 NaN | 金额须 ≥ 0；退款等负数目前不支持 |
| `FileNotFoundError: ... .json` | `--output` 指定的文件夹不存在 | 先建好目录，或输出到当前目录 |
| `error: the following arguments are required: --output` | 忘了 `--output` | 补上 `--output summary.json` |

退出码：`0` 成功、`1` 数据或文件出错、`2` 命令行参数写错。

## 其他细节

- **金额是精确十进制相加**（`12.50 + 8.00 = 20.50`），不会有浮点误差；但 JSON 里的金额是**字符串**，程序化读取时需要自己转成数字。
- 只有表头、没有数据行时，结果是 `{"rows": 0, "totals": {}}`，不算错误。
- Windows 上输出的换行是 CRLF，macOS 上是 LF。如果跨系统比对文件内容，注意这个差异。
- 工具运行期间不联网，也不连接财务系统。
- `python receipt_summary.py --help` 可以看参数列表，但参数说明很简略，细节以上面这份文档为准。
