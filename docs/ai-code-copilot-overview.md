# ai-code-copilot — 业务项目使用全景图

```mermaid
flowchart LR
    subgraph Init ["  初始化（首次）"]
        direction TB
        I1["自动检测技术栈<br/>Spring / Node / Go / Python"]
        I2["扫描项目结构<br/>识别模块与分层"]
        I3["创建配置目录<br/>ai_code_copilot/"]
        I1 --> I2 --> I3
    end

    subgraph Gears ["  核心齿轮"]
        direction TB
        Brain["/brainstorm<br/>设计探索"]
        Spec["/propose<br/>变更提案"]
        Code["/apply<br/>执行编码"]
        Check["/review<br/>双阶段审查"]
        Brain --> Spec --> Code --> Check
    end

    subgraph Side ["  辅助能力"]
        direction TB
        Fix["/fix<br/>增量修正"]
        Test["/test<br/>TDD 测试"]
        Debug["调试<br/>四阶段自动触发"]
    end

    subgraph Final ["  收尾"]
        direction TB
        Archive["/archive<br/>知识沉淀"]
        Knowledge["knowledge/"]
        Archives["changes/archives/"]
        Archive --> Knowledge
        Archive --> Archives
    end

    Init --> Gears
    Check -->|"FAIL"| Fix
    Fix --> Check
    Gears --> Side
    Gears --> Final

    classDef gear fill:#5BA55B,stroke:#3D8B3D,color:#fff,font-size:14px
    classDef side fill:#5DADE2,stroke:#2E86C1,color:#fff,font-size:14px
    classDef final fill:#9B59B6,stroke:#7D3C98,color:#fff,font-size:14px
    classDef init fill:#F5A623,stroke:#D4891A,color:#fff,font-size:14px

    class Brain,Spec,Code,Check gear
    class Fix,Test,Debug side
    class Archive,Knowledge,Archives final
    class I1,I2,I3 init
```

## 一分钟讲清楚

| 阶段 | 一句话 | 产出 |
| --- | --- | --- |
| **/init** | 自动识别你的项目，配置协作环境 | `ai_code_copilot/` 目录 |
| **/brainstorm** | 先聊清楚再动手，避免写错方向 | `design-brief.md` |
| **/propose** | 写规格说明书，明确改什么、怎么改 | `spec.md` + `tasks.md` |
| **/apply** | 按 spec 逐个 task 编码，每个都有证据验证 | 代码 + `log.md` |
| **/review** | 先查有没有按 spec 实现，再查代码质量 | 审查报告 |
| **/fix** | review 发现问题就修，修完再审 | 修复代码 |
| **/test** | Red/Green 循环，覆盖率 ≥ 80% | 测试用例 |
| **/archive** | 把踩过的坑沉淀成知识，下次自动加载 | `knowledge/` |
