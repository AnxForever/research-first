# 收据汇总工具 · 上手说明

写给第一次接触这个工具的新同事。照着[第一部分](#第一部分先跑通一次)敲一遍，你就能独立用它汇总自己的收据数据。

- 工具：仓库根目录的 `receipt_summary.py`
- 依赖：**没有**。只用 Python 标准库，不需要 `pip install` 任何东西
- 平台：Windows 和 macOS 都能用
- 数据：仓库里的姓名、金额、项目都是演示数据，本工具**不连接**任何财务系统

---

## 第一部分：先跑通一次

这一部分请照着敲，先不要改任何东西。做完你手上会有一份真实的汇总结果。

### 1. 打开终端，进入仓库目录

Windows（PowerShell）：

```powershell
cd 你的仓库路径
```

macOS：

```bash
cd 你的仓库路径
```

判断有没有进对：执行 `ls`（Windows 上 `dir`），应该能看到 `receipt_summary.py` 和 `example.csv`。

### 2. 确认 Python 可用

```bash
python --version
```

macOS 上如果提示 `command not found`，换成 `python3 --version`。只要能看到版本号就可以（本文档在 Python 3.12.10 上验证过）。

### 3. 用示例文件跑一次

```bash
python receipt_summary.py example.csv --output summary.json
```

**这一步没有任何输出，是正常的。** 这个工具成功时不打印任何东西，它把结果写进文件。判断成功的标准是：命令没报错，并且当前目录下出现了 `summary.json`。

### 4. 看结果

打开 `summary.json`，内容应该是这样：

```json
{
  "rows": 3,
  "totals": {
    "交通": "20.50",
    "办公": "39.90"
  }
}
```

对照着看：

- `rows` 是读到的**数据行数**，不含表头。示例文件有 3 行数据，所以是 3。
- `totals` 是每个类别的金额合计，按类别名排序。
- 金额是**字符串**（`"20.50"`，不是 `20.50`）。工具内部用十进制累加来避免浮点误差，所以故意不转成数字类型。用的时候按字符串原样读即可。

### 5. 再跑一次（会失败，这是正常的）

把第 3 步的命令原样再执行一次。屏幕上会打出一整段报错，最后一行是：

```
FileExistsError: [Errno 17] File exists: 'summary.json'
```

**这不是你操作错了。** 工具默认不覆盖已经存在的文件，避免手滑把上一次的结果冲掉。想重新生成，就加 `--overwrite`：

```bash
python receipt_summary.py example.csv --output summary.json --overwrite
```

> **记住这一条**：同一个输出文件跑第二次，必须加 `--overwrite`。这是新同事最常撞的一次墙。

到这里你已经跑通了。下面是把示例换成你自己数据的部分。

---

## 第二部分：换成你自己的数据

### CSV 需要什么格式

必需三列：`date`、`category`、`amount`。表头名字要**完全一致**，列的先后顺序随意。

| 列 | 参与计算 | 说明 |
| --- | --- | --- |
| `date` | 否 | 目前只是占位，但**必须存在**，缺了会报错 |
| `category` | 是 | 类别名，不能为空 |
| `amount` | 是 | 金额，非负数字 |

其他多余的列可以存在，会被忽略，不会报错。

示例（就是仓库里的 `example.csv`）：

```csv
date,category,amount
2026-09-28,交通,12.50
2026-09-29,办公,39.90
2026-09-30,交通,8.00
```

### 几个容易踩的点

- **金额不要写千分位逗号。** 这条最危险，因为**它不报错**：`1,200.00` 会被 CSV 按逗号拆成两列，工具只读到 `1`，结果静默算错成 1 块钱。去掉逗号写 `1200.00`。（写成 `"1,200.00"` 加上引号则会直接报 `amount is not a number`，同样是错的。）
- **类别名前后的空格会被自动去掉**，所以 ` 交通 ` 和 `交通` 会合并成同一类，不会分成两类。
- **空行会被跳过**，不报错。
- **负数不支持**：退款、冲销这类负数金额会被拒绝。
- **Excel 导出的 CSV 可以直接用**：带 BOM 和 Windows 换行都能正确读取。
- **小数位不会补齐**：合计为 0 就输出 `"0"`，不是 `"0.00"`。

### 运行

```bash
python receipt_summary.py 你的文件.csv --output 结果.json --overwrite
```

- `--output` 是**必填**的，工具不会把结果打印到屏幕上。
- 路径相对于你**当前所在的目录**。不确定的话，先用绝对路径。
- 输出所在的目录必须**已经存在**，工具不会自动建目录。

---

## 第三部分：报错了怎么办

工具出错时会打印一整段 Python 堆栈，看起来很吓人，但**你只需要看最后一行**。对照下表：

| 最后一行长这样 | 什么意思 | 怎么办 |
| --- | --- | --- |
| `FileExistsError: [Errno 17] File exists: ...` | 输出文件已经存在 | 加 `--overwrite`，或换个输出文件名 |
| `FileNotFoundError: ...` 指向你的 CSV | 找不到输入文件 | 检查路径和当前目录，注意扩展名 |
| `FileNotFoundError: ...` 指向输出路径 | 输出目录不存在 | 先手动建目录，或输出到已有目录 |
| `ValueError: CSV requires date, category, amount columns` | 表头缺列、名字写错，或不是逗号分隔 | 核对表头这三个名字 |
| `ValueError: Row N: category is empty` | 第 N 行类别为空 | 补上类别 |
| `ValueError: Row N: amount is not a number` | 第 N 行金额不是数字 | 常见原因：千分位逗号、货币符号、空单元格 |
| `ValueError: Row N: amount must be finite and non-negative` | 金额是负数，或是 NaN / Infinity | 去掉该行，或改成正确金额 |
| `PermissionError: [Errno 13] ...` | `--output` 指向了一个目录 | 改成文件名 |
| `error: the following arguments are required: ...` | 参数没写全 | 用 `python receipt_summary.py --help` 看用法 |

关于 `Row N`：N 按**数据行**计数，第一条数据行是 2（表头算第 1 行）。文件里如果有空行，N 会比实际行号小，所以别只盯着数字，按类别或金额的内容去找那一行。

两个让人安心的性质：

- **报错时不会留下半成品文件。** 工具会先把整个 CSV 校验完，再去写输出文件。所以看到 `ValueError` 时，你原有的输出文件没有被改动。
- **退出码**：`0` 成功，`1` 是上面这些数据/文件错误，`2` 是参数写错。写脚本时可以用它判断成败。

---

## 第四部分：参考

### 命令行参数

`python receipt_summary.py --help` 的真实输出（工具的说明文字是英文的）：

```
usage: receipt_summary.py [-h] --output OUTPUT [--overwrite] source

Summarize synthetic receipt rows by category using the Python standard
library.

positional arguments:
  source

options:
  -h, --help       show this help message and exit
  --output OUTPUT
  --overwrite
```

上面没写清楚的地方，这里补上：

| 参数 | 必填 | 说明 |
| --- | --- | --- |
| `source` | 是 | 输入 CSV 的路径 |
| `--output OUTPUT` | 是 | 输出 JSON 的路径。**没有默认值**，不写会直接报参数错误 |
| `--overwrite` | 否 | 默认不加；输出文件已存在时会报错，加上才允许覆盖 |
| `-h`, `--help` | 否 | 显示帮助 |

### 输出格式

```json
{
  "rows": 3,
  "totals": {
    "交通": "20.50",
    "办公": "39.90"
  }
}
```

- 文件为 UTF-8 编码（不带 BOM），两空格缩进，末尾有换行符。
- `totals` 的键按类别名排序，同样的输入每次输出完全一致，方便做 diff。
- 金额一律是字符串，且**不会统一补齐到两位**：单个值原样保留输入的小数位（`7` 就是 `"7"`），合计取参与相加的数字里最多的小数位（`12.50 + 8.5` 得 `"21.00"`）。所以别假设拿到的一定是 `x.xx` 格式，展示前自己格式化。
- 换行符跟随系统：Windows 上生成的是 CRLF，macOS 上是 LF。所以**不要把输出 JSON 提交进仓库**——两个平台各跑一次就会产生整文件的 diff。

### 目前不支持的事

- 负数金额（退款、冲销）
- 千分位逗号等带格式的数字
- 总计、按日期筛选、按月份拆分 —— 现在只有按类别的合计
- 读取 Excel 原文件（`.xlsx`）—— 需要先另存为 CSV
- 任何联网或对接财务系统的操作

---

## 第五部分：想改代码的话

给需要维护它的同事：

- 全文件只有一个 `summarize()` 负责读取和计算，`main()` 负责命令行和写文件。要加新功能，基本都改 `summarize()`。
- 金额用 `Decimal` 而不是 `float`，是为了避免浮点误差；输出转成字符串也是这个原因。改动时请保持这一点。
- 代码只用标准库，唯一的版本相关语法是 f-string（Python 3.6+），没有别的门槛；但本次只在 Python 3.12.10 上实测过，更老的版本没有验证。
- 改完至少回归一遍：示例文件能跑出上面那份结果，且重复运行会要求 `--overwrite`。
