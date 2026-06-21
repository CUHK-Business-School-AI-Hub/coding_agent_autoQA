<!-- sync-version: 2026-06-21 -->
# Coding Agent AutoQA

[English](README.md) | [简体中文](README_CN.md) | [繁體中文（香港）](README_HK.md)

<!-- sync-key: promise -->
AutoQA 是一个面向 coding agent 软件开发的证据驱动 QA skill，尤其适合没有技术背景的产品负责人。它与 [coding_agent_constitution](https://github.com/CUHK-Business-School-AI-Hub/coding_agent_constitution) 配合使用：constitution 把产品意图、架构和合同沉淀成长期文档；AutoQA 再把这些文档转成测试、可执行业务流程、新鲜证据和便于人类执行的发布检查清单。

AutoQA 不替代测试框架、代码审查者或人的判断。它要防止 coding agent 把默认 QA harness、一个 happy-path 测试或漂亮的覆盖率数字当成充分证明。

<!-- sync-key: mindset -->
## QA Mindset

核心功能开发可以探索多种合理实现；QA 的自由度更低，因为它的职责是挑战实现，而不是欣赏实现。

工具可以变化，但以下证明责任不能变化：

- 从业务行为和合同出发，而不是从 agent 恰好写出的代码出发。
- 声称模块已覆盖前，先列出所有公开入口和出口。
- 在适用时测试拒绝、边界、状态、权限和依赖失败。
- 证明关键测试确实能发现一个被故意改错的实现。
- 运行每一条已命名的业务流变体，并保留新鲜的命令证据。
- 由人判断视觉质量、易用性、信息清晰度和完整真实旅程。
- 安全、隐私、数据损失、核心流程或重大业务结果错误必须立即停止。

QA 不是悲观，而是用纪律把“agent 看起来很自信”替换为“这是证据、这是缺口、这是需要人作出的决定”。

| 不可妥协 | 可以根据项目调整 |
| --- | --- |
| 需求到测试可追踪 | pytest、Vitest、JUnit 或其他框架 |
| 入口出口及业务边界覆盖 | 测试文件的组织和命名 |
| 新鲜的可执行证据 | 命令如何组合 |
| 人负责视觉和易用性判断 | 浏览器、设备及清单格式 |
| 发布时没有未解决的 P0/P1 | P2/P3 如何排期 |

<!-- sync-key: partnership -->
## 如何与 Constitution 配合

```text
产品想法
   |
   v
constitution-skill
   SPEC -> 用户目标、业务流程、验收标准
   ARCH -> 模块及职责边界
   CONTRACTS -> 输入、输出、错误、schema、事件
   RULES -> 仓库专属安全和测试规则
   TASKS -> 小而明确的实现任务
   |
   v
autoqa-skill
   QA plan -> 必须证明什么、为什么
   file gates -> 每个源文件修改后的快速反馈
   module cases -> 面向业务的黑盒边界测试
   integration flows -> 用脚本跑完整旅程
   human E2E -> 视觉、易用性及发布判断
   |
   v
有证据支持的发布决定
```

没有 constitution 文档时 AutoQA 仍能工作，但必须把推断出的需求标成假设。两者结合更强，因为 QA agent 可以根据长期产品事实独立设计测试，而不是从实现代码倒推原本意图。

<!-- sync-key: gates -->
## 为什么需要这些“门”

门是停止条件，不是仪式。每一道门都在仍然容易定位和修复的时候拦截一类不同的错误。

### 门 0：QA 规划

实现前，agent 先映射需求、风险、模块、入口、出口、业务流变体、环境、命令和人工检查。这样测试不会被已经存在的实现带偏。

### 门 1：文件冒烟

每修改一个可执行源文件，agent 立即执行最窄的语法、类型、导入、编译、启动或业务冒烟检查。被动 schema 或类型文件由验证器或消费者覆盖，不强行制造无意义测试。

原因：一个刚写坏的文件比五个后续文件都依赖它之后更容易诊断。

### 门 2：模块黑盒

把每个架构模块当作黑盒，覆盖所有公开入口和出口，以及适用的正常、拒绝、边界、状态、权限、依赖、幂等、并发和恢复行为。

原因：一次请求能穿到一次响应，只能证明连接存在，不能证明业务正确。

### 门 3：功能集成

通过 HTTP、CLI、事件、文件、任务或其他脚本接口，执行每一条已命名的正常、替代和失败旅程。内部组件尽量保持真实；外部系统只在有文档的合同边界替换。

原因：每个模块单独正确，连接起来仍可能错误。

### 门 4：人工 E2E

Agent 准备普通语言清单和测试环境；人按真实旅程操作并判断布局、文案、反馈、键盘/触摸、响应式、信息清晰度和整体是否合理。

原因：agent 可以读取像素和 DOM 状态，但不能替目标用户作出视觉和体验批准。

### 发布门

只有自动化证据仍然新鲜、人工检查已经完成、且没有未解决的 P0/P1 时，AutoQA 才接受“可以发布”的声明。P2/P3 会继续作为剩余风险展示。

<!-- sync-key: quick-start -->
## 非技术负责人的快速开始

### 1. 安装或暴露 skill

把 `autoqa-skill/` 放入 coding harness 支持的 skill 目录，或直接把该文件夹路径交给 agent。常用安装方法如下：

```bash
# Codex 个人 skill
mkdir -p ~/.codex/skills
cp -R autoqa-skill ~/.codex/skills/autoqa-skill

# Cursor 项目级 skill
mkdir -p .cursor/skills
cp -R autoqa-skill .cursor/skills/autoqa-skill

# Claude Code 项目级 skill
mkdir -p .claude/skills
cp -R autoqa-skill .claude/skills/autoqa-skill
```

安装后重启或打开新的 agent session。如果 harness 没有发现 skill，请以它的当前文档为准，因为安装惯例可能演进。

### 2. 同时使用 constitution 和 AutoQA

可以这样开始：

```text
使用 constitution-skill 定义这个产品，并把下一个功能拆成一个有边界的任务。
然后在实现前使用 autoqa-skill 建立 QA 计划；编码过程中执行文件门和模块门；
功能完成后准备人工 E2E 清单。所有需要我决定的事情请用非技术语言解释。
```

### 3. 主动索取真正的证据

常用提示包括：

```text
告诉我还有哪些业务需求没有对应测试。
```

```text
把这个模块当成黑盒审计。列出每个入口、出口、适用边界，以及证明它的测试。
```

```text
运行 AutoQA 自动化门，告诉我什么通过、什么失败、还有什么没有测试。
```

```text
用简体中文准备人工 E2E 指南。如果我发现 P0 或 P1，请立即让我停止。
```

### 4. 完成人应该做的部分

打开 `docs/QA/HUMAN-E2E.md`，逐项操作。你不需要检查代码或日志。记录实际发生的事情，附上要求的证据；失败时把检查 ID 交回 agent。

遇到陌生词，可以按需阅读 [QA 菜鸟百科](autoqa-skill/references/rookie-qa-pedia_CN.md)。

<!-- sync-key: artifacts -->
## AutoQA 会向项目添加什么

| 文件 | 读者 | 用途 |
| --- | --- | --- |
| `docs/QA/QA-PLAN.md` | 人和 agent | 范围、风险、来源、环境和退出条件 |
| `docs/QA/QA-MATRIX.md` | 人和 reviewer | 从需求到测试和证据的可读映射 |
| `docs/QA/qa-manifest.json` | Agent 和验证器 | 可机械检查的边界、用例、业务流、命令、人工检查和缺陷 |
| `docs/QA/HUMAN-E2E.md` | 非技术人士 | 编号后的视觉和易用性清单 |
| `.autoqa/evidence/latest.json` | 本地验证器 | 新鲜命令结果及命令指纹，通常不提交 |

确定性检查命令：

```bash
python3 autoqa-skill/scripts/check_qa.py --root /path/to/project --phase plan
python3 autoqa-skill/scripts/check_qa.py --root /path/to/project --phase automated --run
python3 autoqa-skill/scripts/check_qa.py --root /path/to/project --phase release
```

命令执行器使用参数数组，不使用隐藏逻辑的 shell 字符串。命令发生变化或证据超过时间限制后，原证据自动失效。

<!-- sync-key: defects -->
## QA 失败时怎么办

| 等级 | 常见例子 | 下一步 |
| --- | --- | --- |
| P0 | 数据损失、隐私/安全泄露、不受控的不可逆行为 | 立即停止；不要在该环境继续 |
| P1 | 应用无法启动、核心旅程受阻、重大结果错误、严重无障碍障碍 | 停止受影响测试；修复并重测后再继续 |
| P2 | 非核心行为错误或容易误解，但存在安全替代方案 | 保存证据；继续相互独立的安全检查；之后集中提交 |
| P3 | 视觉、文案、间距或低影响细节问题 | 记录并完成清单 |

等级取决于影响，不取决于修复看起来是否容易。阻断问题修复后，agent 必须说明要重跑哪些自动化测试、重做哪些已经通过的人工检查。

<!-- sync-key: best-practices -->
## 不断演进的最佳实践

AutoQA 初始版本故意保留一个空的最佳实践 registry。规划测试前，agent 先检查 registry；没有当前适用的实践包时，再查询最新官方文档、标准和第一手资料，而不是只依赖记忆。

新实践包依次经历 `Candidate`、`Active` 和 `Superseded`。每个包记录范围、不适用情况、来源、复核日期、验证案例和限制。尚未证实的想法放在 `TODO_BEST_PRACTICE_EVOLUTION.md`，不能被偷偷当成行业事实。

<!-- sync-key: languages -->
## 语言

`SKILL.md`、脚本、schema 字段、ID 和 agent 技术参考以英文为规范源。README、QA 菜鸟百科和人工 E2E 模板同时维护英文、简体中文和香港繁体中文。`check_translations.py` 检查这些关键文档的版本和章节是否同步。

<!-- sync-key: influences -->
## 参考项目与许可证

AutoQA 的“先证据后声明”、red-green 测试和反 mock 偷懒机制受到 MIT 项目 [obra/superpowers](https://github.com/obra/superpowers) 启发；更广泛的测试词汇也参考了 MIT 项目 [wshobson/agents](https://github.com/wshobson/agents) 和 [addyosmani/web-quality-skills](https://github.com/addyosmani/web-quality-skills)。

本仓库采用 [MIT License](LICENSE)。
