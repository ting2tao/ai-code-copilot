---
trigger: always_on
name: frontend-react-verification
description: React/前端变更验证要求
globs: "*.tsx,*.ts,*.jsx,*.js,package.json,playwright.config.*,vite.config.*,next.config.*"
---
# Frontend React 变更验证

## 验证原则

- 优先使用项目已有 `package.json` scripts；不要为了验证临时引入新的测试框架或构建工具。
- UI 可见变化必须验证真实渲染结果；本地应用可启动时，优先用浏览器访问或截图确认。
- 异步流程必须覆盖 loading、error、empty、success 中受本次改动影响的状态。
- 权限、鉴权、删除、提交、发布等敏感交互必须同时验证允许路径和拒绝路径。

## 场景矩阵

| 改动场景 | 最低验证 |
|----------|----------|
| 类型、schema、共享 contract | 类型检查；构建 |
| 组件渲染或交互 | 行为测试；必要时截图 |
| 路由、layout、server/client component 边界 | 构建；访问受影响路由 |
| API client、缓存、请求状态 | 单测或集成验证；错误态和成功态 |
| 样式体系或设计系统组件 | 受影响页面截图；移动端和桌面至少各一个视口 |
