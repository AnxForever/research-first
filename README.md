# research-first

**简体中文** · [English](README.en.md)

> 先理解用户真正想达成什么，再研究该怎么选。

一个面向 AI agent 的通用意图理解与调研方法论。它把**压缩的想法、症状、建议和质疑**转化为有证据支撑的决策——既不盲从用户的字面表述，也不自行扩大范围。

## 它做什么

这个 skill 引导 agent：

1. **还原意图** —— 把用户的话拆成目的、硬约束、候选手段、隐含假设和缺失维度。
2. **按比例扩展** —— 只补充有相关性、有证据、与任务分量相称的考量。
3. **高质量调研** —— 用本地证据、一手资料、既有方案、用户数据和安全的实验。
4. **评判所提手段** —— 采纳、改造、组合或否决，而不是把建议当成规格书。
5. **遇质疑时重估** —— 用户质疑时，去找**能推翻当前做法**的证据，而不是一味辩护或附和。
6. **行动并验证** —— 把发现转化为决策、实现约束、测试和完成证据。

当用户要求调研、要来源、要例子、要理解意图、要扩展想法，或者要求重新考虑已在推进的工作时，它会明确触发。

## 为什么需要它

用户说的话通常不是规格书。**「加个浏览器 skill」**可能是在说「agent 要能可靠地完成网页流程」；**「做得像 Vercel」**说的是克制、层次、密度这些**性质**，不是照抄布局；**「用 Redis」**可能表示需要共享状态、持久化或协调——先确认是哪个问题，再决定要不要引入 Redis。

这个 skill 让 agent 对这类输入保持**先调研、再决定**，而不是把用户随口提到的名词直接搬进方案。同时它有一个对称的约束：**不许借「理解意图」之名自行扩大范围**——每一条补充都必须通过相关性、证据、比例三重检验。

## 安装

```bash
npx skills add AnxForever/research-first
```

或手动：

```bash
git clone https://github.com/AnxForever/research-first.git ~/.agents/skills/research-first
```

## 结构

```
research-first/
├── SKILL.md                              # 核心工作流
├── agents/openai.yaml                    # Skill UI metadata
├── assets/                               # 可复用的调研模板
└── references/                           # 深入指南与回归案例
    ├── search-quality.md                 # 检索构造、质量信号、反模式
    ├── problem-expansion.md              # 10 维度框架与具体例子
    ├── feature-evidence-ledger.md        # 逐功能证据台账的结构与回填规则
    ├── adapting-depth.md                 # 时间压力、风险分级、失败模式
    ├── contradictions.md                 # 参考资料互相矛盾时怎么办
    └── intent-interpretation-evaluation.md # 评分标准与回归案例
```

核心文件保持精简，深入内容放在 `references/`——按需读取，而不是每次触发都全量加载。

## 适用环境

- 任何支持 Agent Skills 标准的 AI agent（Claude Code、Codex、Cursor 等）
- 无依赖、无需 API key、无需配置

## 许可

MIT —— 见 [LICENSE](LICENSE)
