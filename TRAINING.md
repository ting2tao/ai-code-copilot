# ai-code-copilot 使用培训

> **核心理念：Context First, Code Follows.**
> AI 让代码更容易生成，真正稀缺的是准确理解需求、约束和验证标准的共享上下文。
> ai-code-copilot 的所有设计，都是为了让 AI 在正确的上下文里做正确的事。

---

## 一、它是什么

ai-code-copilot 是一个部署在 `~/.claude/ai_code_copilot/` 的全局 Claude Code 配置，通过 skill 机制自动加载。你在任何后端项目里跟 Claude 说「帮我实现一个功能」，它就激活了。支持 Java/Spring Boot、Python、Go 等技术栈，/init 会自动检测项目类型并加载对应规则包。

**它不是代码生成器。** 它是一个遵循研发纪律的 AI 搭档：
- 写代码前先搞清楚要做什么（Spec 驱动）
- 复杂需求先头脑风暴再动笔（设计探索）
- 完成后必须展示命令输出，不接受口头声明（Evidence Before Claims）
- 踩过的坑记下来（知识飞轮）

---

## 二、触发方式

直接用中文跟 Claude 说话即可，不需要记命令。

| 你想做的 | 怎么说 |
|---------|--------|
| 先讨论方案再动手 | 「先讨论一下这个需求」「帮我分析一下方案」「brainstorm」 |
| 做一个新需求 | 「帮我实现用户注册功能」「我要加个订单查询接口」 |
| 修一个 Bug | 「这里报空指针了」「xxx 功能不工作了」 |
| Review 代码 | 「帮我看一下这次的改动」「review 一下 add-coupon」 |
| 写单元测试 | 「帮我补一下 OrderService 的单测」「写测试」 |
| 归档沉淀知识 | 「归档 add-coupon 这个变更」 |
| 初始化项目 | 「初始化项目」（第一次使用时运行） |

也可以直接说出流程名称：「init」「brainstorm」「propose」「apply」「fix」「review」「test」「archive」

---

## 三、渐进式复杂度

每次接到任务，AI 会**先判断档位告诉你**，你可以接受或覆盖：

```
你：帮我实现优惠券发放功能

AI：我判断这是 Standard 档（预计涉及 coupon service + 发放记录表 + 对外接口，
    改动 5-8 个文件，需要 2-3 天）。
    建议先走 /brainstorm 梳理设计，再进入 /propose。
    先问你几个问题...
```

| 档位 | 标准 | 流程 | 文档 |
|------|------|------|------|
| **Quick** | ≤1天，<5文件，不跨模块 | 说明范围 → 确认 → 执行 | 只有 log |
| **Standard** | 1-5天，或你要求 | /brainstorm（建议）→ /propose → /apply → /review | design-brief + spec + tasks + log |
| **Complex** | >5天，或跨 3+ 模块 | /brainstorm（必须）→ 拆子项目 → 每个走 Standard | 每个子项目各自文档 |

**Quick 档的代价：** 没有 spec，所以 /review 阶段无法做 Spec 合规检查，只能做代码质量检查。AI 会提前告知你这个限制。

**建议：** 新需求默认走 Standard，别为了省事走 Quick，事后 review 不了，踩了坑也不好溯源。

---

## 四、Standard 档完整流程

### 第零步：/brainstorm — 设计探索（苏格拉底式对话）

Standard 档建议先做，Complex 档**必须**先做。目的是在写 spec 之前对齐方向，避免方向跑偏了再推倒重来。

AI 走五个步骤，**每次只问一个问题，不连发多问**：

**Step 1：理解意图**
```
AI：发券功能的触发时机是什么？
    A. 用户主动领取（推荐，符合现有业务模式）
    B. 系统自动发放（需要定时任务）
    C. 订单完成后触发
```

**Step 2：探索现状（代码有出处）**
```
AI：相关现状：
- CouponService.java:L34 — 现有优惠券查询逻辑
- coupon_info 表 — 字段：coupon_id / type / amount / expire_time
- 暂无发放记录表，需要新建
```

**Step 3：提出 2-3 个方案 + 推荐**

```
AI：方案对比：
    方案 A（推荐）：直接写 coupon_issue_log 表，uid+coupon_id 唯一索引防重
    方案 B：Redis SET 防重，异步落库 — 性能好但增加复杂度，YAGNI
    推荐 A，理由：当前 QPS 不高，简单可靠优先
```

**Step 4：逐段确认**（每段等你确认才继续）

**Step 5：生成 design-brief.md**

```
.ai_code_copilot/changes/add-coupon/
└── design-brief.md   ← 记录需求理解、方案选择、风险识别
```

完成后提示：`设计简报已生成。确认后可执行 /propose add-coupon 进入方案细化。`

---

### 第一步：/propose — 把需求变成 Spec

如果已有 design-brief，AI 直接加载作为输入，跳过重复的方案探索，只补充技术细节。

AI 会做三件事后才生成文档：

**1. Research（代码出处）**
```
AI：我找到以下相关代码：
- OrderController.java:L45 — 现有下单接口
- OrderService.java:L89 — 订单创建核心逻辑
- order_info 表 — 现有字段 ...
风险点：修改支付状态有并发风险
```

**2. 逐一提问（一次一个问题）**
```
AI：支付成功回调后，是直接发货还是等人工确认？
    A. 自动发货（推荐，符合现有链路）
    B. 人工确认后发货
    C. 其他
```

**3. 分三段展示草稿，你逐段确认**
```
AI：【段1】代码现状 + 功能点 — 是否正确？
（你确认）
AI：【段2】变更范围 + 风险 — 是否有遗漏？
（你确认）
AI：【段3】技术决策 + 待澄清 — 还有什么问题？
```

**HARD-GATE：** 待澄清全部解决、你显式回复「确认」后，才能进入编码。

生成的文件在 `.ai_code_copilot/changes/<变更名>/`：
```
add-coupon/
├── design-brief.md  ← /brainstorm 产出（若已执行）
├── spec.md          ← 需求合同，不得在编码阶段擅自改动
├── tasks.md         ← 执行计划，每个 task 精确到文件和函数
└── log.md           ← 决策记录，供 /archive 时沉淀
```

---

### 第二步：/apply — 执行编码

```
你：apply add-coupon
```

**开发标准流：** 严禁无票开发。每个代码变更必须关联 Issue，spec/quick-card 里要记录 Issue ID 或 URL；推荐一个 Issue 对应一个开发分支，分支名使用 `<type>/<description>-<IssueID>`，例如 `feature/login-123`、`fix/header-456`。可以使用云端 Copilot 或本地 AI 助手，但必须遵守 Issue、验证、提交与 PR 门禁。

AI 逐 task 执行，每完成一个 task，必须展示**可验证证据**：

```
AI：T1 完成：CouponService.issueCoupon() 方法已实现

    验证（使用 project-context.md 中记录的编译命令）：
    $ mvn compile -pl coupon-service -q
    BUILD SUCCESS

    已 commit：feat(coupon): 新增 issueCoupon 核心逻辑

    继续 T2？
```

**log.md 实时写入规则：**
- 关键决策 / 方向调整 / Reverse Sync 事件 → 写入 `## 过程记录`
- 踩坑 / 隐含规则 / 新发现 → 写入 `## 知识发现`

**所有 task 完成后，自动回填 `## 变更信息`：** 完成时间、涉及文件数、commit 列表。

**完成声明铁律（Evidence Before Claims）：** 每个 task 完成后，以及 /fix 完成后，AI 必须先展示实际命令输出，才能说"完成了"。你不会看到"应该好了"这类无证据声明。

**零偏差原则：** spec 是合同，AI 是打印机。遇到逻辑冲突必须停下来：

```
AI：⚠️ 发现问题：spec §3.2 要求发放记录写 coupon_issue_log 表，
    但该表字段与当前 DO 不匹配。
    
    请确认：是修改 spec 还是修改表结构？
    确认前我不会继续编码。
```

---

### 第三步：/review — 两阶段审查

```
你：review add-coupon
```

**前置检查：** AI 先读取 tasks.md/log.md 中记录的 /apply commit hash。没有则停止，提示先补录提交记录或执行 `/apply`——没有代码证据就没有可审查的对象。

**PR 要求：** 提交 PR 时必须用 `Closes #ID` 关联对应 Issue，并确保 CodeQL 静态审查与 CI 编译自动化审查被触发。

**阶段一：Spec Compliance**（独立 Sub-Agent）

隔离运行，不知道你刚才改了什么，只会亲自读代码验证：
```
Spec Compliance 审查报告 — add-coupon

- ✅ F1 优惠券发放：已实现，见 CouponService.java:L42
- ✅ F2 发放记录写入：已实现，见 CouponIssueLogMapper.java:L23
- ❌ F3 发放上限校验：未实现（spec §3.3 要求每人限领一张，代码中未找到校验逻辑）

结论：❌ 不合规，需修复 F3
```

Spec 合规通过后，才进入——

**阶段二：Code Quality**（另一个独立 Sub-Agent）

```
Code Quality 审查报告 — add-coupon

Critical（阻塞）：
- ❌ CouponService.java:L89：并发场景下发放上限校验有 race condition，
  未加分布式锁

Important（应修复）：
- ⚠️ CouponMapper.java:L34：魔法值 "1" 未定义为常量

结论：❌ FAIL（有 Critical 问题）
```

**两阶段完成后，无论 PASS/FAIL，AI 自动将结论写入 log.md `## /review 结论`。**

FAIL → 回到 `/fix`，修完重新 `/review`，直到双阶段 PASS。

> 如果你接受某个 Important 问题不改，说「这个问题我们接受」，AI 会记到 log.md `## 遗留问题` 并注明原因，不阻塞流程。但 Critical 不能跳过。

---

### 第四步：/archive — 归档 + 知识沉淀

```
你：archive add-coupon
```

AI 逐条问你要不要把发现沉淀到 knowledge/：

```
AI：发现以下值得沉淀的内容：

    1. 优惠券发放场景需要分布式锁（RedisLockHelper，TTL=30s）
       → 沉淀到 knowledge/distributed-lock.md？(y/n)

    2. coupon_issue_log 表设计：uid + coupon_id 联合唯一索引
       → 沉淀到 knowledge/coupon-design.md？(y/n)
```

沉淀后，这些知识会成为下次 /propose 的上下文——AI 看到「发券」两个字就会自动加载相关知识，不会再踩同样的坑。

---

## 五、调试流程

遇到报错不需要任何命令，直接说就行：

```
你：本地测试环境跑 OrderServiceTest 报 NullPointerException

AI：好的，我进入调试模式。先看完整日志...
```

AI 走四阶段，**禁止未确认根因前改代码**：

| 阶段 | 做什么 |
|------|--------|
| Phase 1 根因调查 | 完整读日志 + 复现步骤 + 查近期 git 变更 |
| Phase 2 模式分析 | 找能跑通的类似代码，逐项对比差异 |
| Phase 3 假设验证 | 写下具体假设，最小变更验证 |
| Phase 4 实施修复 | 先写复现测试（Red）→ 修复（Green） |

**连续三次未修复则停止，与你讨论架构问题。** 不会无限次乱试。

---

## 六、项目初始化（第一次用）

在任何新项目里，先说「初始化项目」：

```
你：初始化项目

AI：检测到 pom.xml，识别为 java-spring 项目，加载规则包...
    已识别：
    - 技术栈：Spring Boot 2.7 + MyBatis + Redis
    - 分层：Controller → Service → Manager → DAO
    - 关键模块：order / coupon / user / payment
    - 构建命令：mvn compile -q / mvn test（已写入 project-context.md）
    
    已创建 .ai_code_copilot/ 目录，建议提交到 git：
    git add .ai_code_copilot/ && git commit -m "chore: 初始化 ai-code-copilot"
```

> 非 Java 项目（如 Python、Go）也适用：AI 根据 `requirements.txt` / `go.mod` 等文件判断技术栈，询问确认后填入对应的构建和测试命令。

生成的目录：
```
<project>/.ai_code_copilot/
├── rules/
│   ├── project-context.md   ← AI 自动填充的工程上下文
│   ├── coding-style.md      ← 可覆盖全局规范
│   └── domain-rules.md      ← 项目业务约束（你来填）
├── knowledge/
│   └── index.md             ← 知识索引（/archive 自动维护）
└── changes/
    └── （变更目录，每次 /propose 后自动创建）
```

**domain-rules.md 建议填写的内容：**
- 订单状态流转规则
- 金额处理约定（用 BigDecimal，禁用 double）
- 特定业务的禁止操作
- 团队约定的架构决策

这些规则会在每次会话启动时自动加载，AI 不会再做违反它们的事。

---

## 七、安全规则自动注入（Hooks 机制）

安装完成后，每次打开 Claude Code 会话，框架会通过 **SessionStart Hook** 自动向 Claude 注入安全规则：

```
[会话启动时，Claude 自动收到]
- Standard/Complex 档：/propose 未确认前，禁止任何编码动作
- Quick 档：必须先说明变更范围，确认后才执行
- 涉及资金/状态流转/权限变更：必须高亮提醒，等待人工确认
- 禁止硬编码密钥、AK/SK、数据库密码
- 禁止日志中打印手机号、身份证、银行卡等敏感信息
```

**你不需要做任何操作。** install.sh 在安装时已自动将 hook 写入 `~/.claude/settings.json`。

这意味着：即使你没有手动触发 ai-code-copilot skill，安全红线依然在每次会话中生效。

---

## 八、安装 & 更新

```bash
# 安装（一次性）
curl -fsSL https://raw.githubusercontent.com/ting2tao/ai-code-copilot/main/install.sh | bash
# 或本地安装
cd ~/.claude/ai_code_copilot && bash install.sh

# 更新（拉取最新版本）
cd ~/.claude/ai_code_copilot && bash install.sh
# symlink 指向源文件，pull 后自动生效
```

安装脚本会自动完成三件事：
1. clone / 更新框架到 `~/.claude/ai_code_copilot/`
2. 创建 skill symlink（让 Claude Code 识别 skill）
3. 注册 SessionStart Hook 到 `~/.claude/settings.json`（安全规则自动注入）

---

## 九、常见问题

**Q：Quick 档和 Standard 档怎么选？**

> 简单原则：改动涉及任何业务逻辑（不是纯配置或修字段），就走 Standard。
> Quick 省的时间，往往在 debug 时加倍还回来。

**Q：/brainstorm 和 /propose 有什么区别？**

> /brainstorm 解决"方向对不对"，/propose 解决"具体怎么做"。brainstorm 是苏格拉底式讨论，产出一份设计简报；propose 读取简报后补充技术细节，产出可执行的 spec + tasks。没有 brainstorm 也可以直接 propose，但复杂需求容易在 apply 中途发现方向跑偏。

**Q：AI 给出的档位判断不对怎么办？**

> 直接说「改成 Standard 档」或「这个其实很简单，走 Quick」，AI 会遵从你的判断。

**Q：/review 太严了，有些 Important 问题我觉得可以不改？**

> 和 AI 说「这个 Important 问题我们接受，记到 log 里」，AI 会记录你的决策，不会阻塞流程。但 Critical 问题不能跳过。

**Q：中途需求变了，spec 要改怎么办？**

> 直接说「需求变了，xxx 改成 xxx」，AI 会先改 spec，再评估对 tasks 的影响，然后告诉你接下来怎么做。

**Q：AI 在 /apply 过程中停下来了说"Reverse Sync"是什么意思？**

> 说明 AI 发现实际情况和 spec 描述不一致，需要你先确认 spec 的正确版本，再继续写代码。这是保护你的机制——先对齐再动手，比动完手再发现方向错了代价小得多。

**Q：knowledge/ 里的内容什么时候会自动加载？**

> 每次 /propose 的 Research 阶段，AI 会读 knowledge/index.md，匹配当前需求的关键词，自动加载命中的知识文档。例如你在做一个「扣库存」的需求，index.md 里有「库存扣减」的条目，AI 就会自动读取对应文档，知道你们用什么方式做扣减、有什么坑。

**Q：项目不是 Java，可以用吗？**

> 可以。/init 会根据项目文件（go.mod / requirements.txt / package.json 等）自动检测技术栈，加载对应规则包，并将实际的构建和测试命令写入 project-context.md。后续所有命令都读这份配置，不会硬写 `mvn`。

**Q：log.md 需要自己维护吗？**

> 不需要。全程自动维护：/apply 按章节分类写过程记录和知识发现，所有 task 完成后回填变更信息，/review 写审查结论，接受某 Important 问题时写遗留问题。你只需要在 /archive 时确认哪些条目要沉淀到 knowledge/。

---

## 十、一句话总结

**它最大的价值不是写代码快，而是让 AI 在正确的方向上工作，不用你反复纠正。**

核心流程记住一条线就够了：

```
说需求 → brainstorm（对齐方向）→ propose（写死 spec）→ apply（逐task执行+证据）→ review（双阶段验收）→ archive（沉淀知识）
```

Quick 档可以跳过 brainstorm 和 propose，直接说需求确认后执行，但没有 spec 保护。
