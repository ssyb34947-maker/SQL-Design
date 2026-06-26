# SQL Design

SQL Design 是一个 SQL 设计与优化 Skill，面向 Claude Code、Codex 等编码 Agent 使用。
目标是让 Agent 在写 SQL、审查 SQL、设计表结构、构建索引、处理 ORM、规避 SQL 注入和规划数据库变更时，更接近企业级后端工程师和数据库工程师的工作方式。

## 为什么需要它

编码 Agent 很容易写出本地 Demo 可用的 SQL：

- 表能建好。
- 数据能插入。
- 查询能返回正确结果。

但生产环境还需要更多东西：性能、安全、索引、事务、锁、版本控制、迁移、回滚、可观测性和高并发下的稳定性。

SQL Design 的作用是把这些生产级约束沉淀为一个可复用的开源 Skill，让开发者在 Claude Code、Codex 等工具里直接调用。

## 能力范围

- PostgreSQL 优先的 SQL 设计与优化。
- MySQL 和 Oracle 兼容指导。
- 已有 SQL、表结构、索引、执行计划的优化分析。
- 需求阶段的表结构、约束、索引、SQL、ORM 和迁移设计。
- 主流索引设计原则和生产上线风险。
- 执行计划分析。
- SQL 改写模式。
- SQL 注入防护和安全动态 SQL。
- Java、Python、Node.js、Go、.NET 常见 ORM 技术栈指导。
- 事务、锁、死锁和高并发风险审查。
- 数据库迁移版本控制、验证和回滚规划。

## 目录结构

```text
sql-design/
├── SKILL.md
├── agents/
│   └── openai.yaml
├── references/
│   ├── sop.md
│   ├── intake-checklist.md
│   ├── database-selection.md
│   ├── postgresql.md
│   ├── mysql.md
│   ├── oracle.md
│   ├── schema-design.md
│   ├── index-design.md
│   ├── query-rewrite.md
│   ├── execution-plan.md
│   ├── orm-and-application-stack.md
│   ├── sql-injection-security.md
│   ├── transaction-locking.md
│   ├── migration-version-control.md
│   ├── performance-testing.md
│   ├── enterprise-report-template.md
│   └── anti-patterns.md
└── scripts/
    ├── checklist_generator.py
    ├── normalize_explain.py
    └── sql_static_lint.py
```

`SKILL.md` 只做纲要、触发和资源导航。详细规则放在 `references/`，脚本放在 `scripts/`。

## 安装

Codex 风格的本地 Skill 可以放到本地 skills 目录，例如：

```bash
cp -R sql-design ~/.codex/skills/sql-design
```

Claude Code 或其他 Agent 环境可以按各自的 Skill、自定义指令或资源加载机制引用该目录。

## 使用示例

```text
Use $sql-design to review this PostgreSQL query and suggest safe indexes, validation steps, and rollback.
```

```text
Use $sql-design to design the schema, indexes, migration, and ORM access layer for this new order module.
```

```text
Use $sql-design to check whether this MyBatis dynamic SQL has SQL injection or tenant isolation risks.
```

## 辅助脚本

### 生成任务清单

```bash
scripts/checklist_generator.py --mode optimization --database postgres --orm MyBatis
```

```bash
scripts/checklist_generator.py --mode design --database mysql --format json
```

### 静态 SQL 风险检查

```bash
scripts/sql_static_lint.py --dialect postgres path/to/query.sql
```

也可以从标准输入读取：

```bash
printf "SELECT * FROM users ORDER BY ${sort};" | scripts/sql_static_lint.py --dialect postgres
```

该脚本会检查 `SELECT *`、无界查询、危险动态排序、字符串拼接 SQL、无 WHERE 的更新/删除、函数包裹索引列、深分页、DDL 风险等常见问题。

### 执行计划摘要归一化

```bash
scripts/normalize_explain.py --database postgres path/to/explain.txt
```

```bash
scripts/normalize_explain.py --database auto --format json path/to/plan.txt
```

该脚本不会替代 DBA 或 Agent 的判断，它只是把 PostgreSQL、MySQL、Oracle 或通用文本执行计划整理成便于审查的摘要，并标记顺序扫描、排序、临时空间、Nested Loop 和估算偏差等信号。

## 设计原则

这个 Skill 应引导 Agent 输出可审计的工程结论：

- 已确认事实。
- 假设和缺失证据。
- 根因分析。
- 推荐方案。
- 安全风险。
- 索引影响。
- 锁和迁移风险。
- 验证方案。
- 回滚方案。

