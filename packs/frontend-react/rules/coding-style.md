---
trigger: always_on
name: frontend-react-coding-style
description: React/前端编码规范
globs: "*.tsx,*.ts,*.jsx,*.js,*.css,*.scss"
---
# Frontend React 编码规范

## 组件设计

- 组件职责单一；展示组件、容器组件、业务逻辑 hooks 要有清晰边界。
- 复杂状态优先收敛到 feature 内部，不随意提升到全局状态。
- 表单、表格、弹窗、路由跳转等交互必须覆盖 loading、empty、error、success 状态。

## 类型与数据流

- TypeScript 项目中，API 响应、组件 props、表单数据必须有类型定义。
- 不在组件渲染中直接写复杂数据转换；提取为 selector、hook 或纯函数。
- API client 层统一处理 base URL、鉴权 header、错误转换。

## 可访问性与体验

- 可点击元素使用语义化按钮/链接，保证键盘可达。
- 表单控件要有 label、错误提示和禁用状态。
- 异步操作要避免重复提交，并提供用户可理解的反馈。

## 测试

- 关键用户流程优先用行为测试覆盖。
- 组件测试关注用户可见行为，不测试内部实现细节。
- 修改路由、权限、表单校验、数据缓存时必须补充回归验证。
