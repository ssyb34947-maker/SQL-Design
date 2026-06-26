# SQL Design

[![Agent: Skill](https://img.shields.io/badge/Agent-Skill-blue.svg)](https://github.com/claudeai/claude-agent/tree/main/skills/sql-design/README.md#agent-skill-usage)
[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)](https://www.python.org/downloads/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-12%2B-blue)](https://www.postgresql.org/)
[![MySQL](https://img.shields.io/badge/MySQL-8%2B-blue)](https://www.mysql.com/)

SQL Design 是一个面向 **企业级生产环境** 的 SQL 设计与优化 Skill，专为 Claude Code、Codex 等编码 Agent 打造。

> 让 AI 写的 SQL 不仅能跑通，更能**稳定上线**。

## 核心价值

| 维度 | Demo 级 SQL | 生产级 SQL（SQL Design 赋能） |
|------|------------|----------------------------|
| **性能** | 能查就行 | 索引优化、执行计划分析、查询改写 |
| **安全** | 无防护 | SQL 注入防护、租户隔离检查 |
| **稳定性** | 单机可用 | 事务、锁、死锁风险审查 |
| **可维护** | 无版本控制 | 迁移脚本、版本管理、回滚规划 |
| **可观测** | 无监控 | 执行计划归一化、性能基线 |

## 能力覆盖

### 数据库支持
- **PostgreSQL** - 优先支持，深度优化
- **MySQL** - 完整兼容指导
- **Oracle** - 企业级特性支持

### 核心功能
- ✅ **表结构设计** - 约束、范式、分区策略
- ✅ **索引优化** - B-Tree、GIN、GiST、覆盖索引
- ✅ **执行计划分析** - 全表扫描、排序、临时表识别
- ✅ **SQL 改写** - 子查询优化、JOIN 策略、分页优化
- ✅ **安全审计** - SQL 注入检测、动态 SQL 风险
- ✅ **ORM 指导** - Java/Python/Node.js/Go/.NET 技术栈
- ✅ **并发控制** - 事务隔离、锁竞争、死锁预防
- ✅ **迁移管理** - 版本控制、验证、回滚规划

## 项目结构

```text
sql-design/
├── SKILL.md                          # Skill 入口（纲要、触发、资源导航）
├── agents/
│   └── openai.yaml                   # OpenAI Agent 配置
├── references/                       # 详细知识库
│   ├── sop.md                        # 标准作业流程
│   ├── intake-checklist.md           # 需求采集清单
│   ├── database-selection.md         # 数据库选型指南
│   ├── postgresql.md / mysql.md / oracle.md  # 各数据库特性
│   ├── schema-design.md              # 表结构设计规范
│   ├── index-design.md               # 索引设计原则
│   ├── query-rewrite.md              # SQL 改写模式
│   ├── execution-plan.md             # 执行计划分析
│   ├── orm-and-application-stack.md  # ORM 技术栈
│   ├── sql-injection-security.md     # SQL 注入防护
│   ├── transaction-locking.md        # 事务与锁
│   ├── migration-version-control.md  # 迁移版本控制
│   ├── performance-testing.md        # 性能测试
│   ├── enterprise-report-template.md # 企业级报告模板
│   └── anti-patterns.md              # 反模式清单
└── scripts/                          # 辅助工具脚本
    ├── checklist_generator.py        # 任务清单生成器
    ├── normalize_explain.py          # 执行计划归一化
    └── sql_static_lint.py            # SQL 静态风险检查
```

## 快速开始

### 安装

将 Skill 复制到本地 skills 目录：

```bash
# Codex 风格
cp -R sql-design ~/.codex/skills/sql-design

# 其他 Agent 环境按各自机制引用
```

### 使用示例

```text
# 审查 SQL 查询
Use $sql-design to review this PostgreSQL query and suggest safe indexes, validation steps, and rollback.

# 设计新模块
Use $sql-design to design the schema, indexes, migration, and ORM access layer for this new order module.

# 安全审计
Use $sql-design to check whether this MyBatis dynamic SQL has SQL injection or tenant isolation risks.
```

## 辅助工具

### 1. 任务清单生成器

```bash
# 优化模式
scripts/checklist_generator.py --mode optimization --database postgres --orm MyBatis

# 设计模式（JSON 输出）
scripts/checklist_generator.py --mode design --database mysql --format json
```

### 2. SQL 静态风险检查

```bash
# 检查文件
scripts/sql_static_lint.py --dialect postgres path/to/query.sql

# 标准输入
printf "SELECT * FROM users ORDER BY ${sort};" | scripts/sql_static_lint.py --dialect postgres
```

**检测项**：`SELECT *`、无界查询、危险动态排序、字符串拼接 SQL、无 WHERE 更新/删除、函数包裹索引列、深分页、DDL 风险

### 3. 执行计划归一化

```bash
# 单文件处理
scripts/normalize_explain.py --database postgres path/to/explain.txt

# 自动检测数据库类型，JSON 输出
scripts/normalize_explain.py --database auto --format json path/to/plan.txt
```

**功能**：跨数据库（PostgreSQL/MySQL/Oracle）执行计划统一摘要，标记全表扫描、排序、临时空间、Nested Loop、估算偏差等信号

## 设计原则

SQL Design 引导 Agent 输出**可审计的工程结论**，包含：

1. **已确认事实** - 当前状态的客观描述
2. **假设与缺失证据** - 需要验证的前提条件
3. **根因分析** - 性能问题或安全风险的根本原因
4. **推荐方案** - 具体可执行的优化措施
5. **安全风险** - 潜在的安全隐患
6. **索引影响** - 新增/修改索引的代价与收益
7. **锁与迁移风险** - 生产变更的风险评估
8. **验证方案** - 上线前的验证步骤
9. **回滚方案** - 失败时的回滚策略

## 贡献

欢迎提交 Issue 和 Pull Request！

### 贡献指南

1. Fork 项目
2. 创建功能分支 (`git checkout -b feature/xxx`)
3. 提交更改 (`git commit -am 'Add xxx'`)
4. 推送到分支 (`git push origin feature/xxx`)
5. 创建 Pull Request