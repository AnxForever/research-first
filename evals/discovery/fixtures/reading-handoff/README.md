# Reading Shelf fixture

这是一个仅依赖 Python 标准库的离线小工具。它从同目录的 `shelf.json` 读取资料，当前支持按原始顺序列出条目：

```powershell
python .\reading_shelf.py list
python .\reading_shelf.py list --format markdown
```

数据文件是 JSON 数组；数组顺序就是列表顺序。每条记录包含 `id`、`title`、`url`、`note` 和 `selected`。不要把本地数据上传或改写来生成交接内容。

`reading_shelf.py` 中的 `render_markdown_link(title, url)` 已用于 Markdown 列表，适合需要同样链接格式的功能复用。
