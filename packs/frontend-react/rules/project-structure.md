---
trigger: always_on
name: frontend-react-project-structure
description: React/前端项目结构与边界
globs: "*.tsx,*.ts,*.jsx,*.js,package.json"
---
# Frontend React 项目结构

- 优先遵循项目现有框架：Next.js、Vite、CRA、Remix 或自定义构建。
- 路由层只做页面组装和数据入口，不堆积复杂业务逻辑。
- `features/<feature>/` 可包含组件、hooks、api、types、tests，避免跨 feature 直接访问内部文件。
- 共享组件放 `components/` 或项目既有设计系统目录，不能混入业务副作用。
- 样式方案跟随项目既有选择：CSS Modules、Tailwind、styled-components、vanilla-extract 等，不混用新体系。
