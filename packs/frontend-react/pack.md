# 规则包：frontend-react

## 检测规则

以下任一组合命中本包：
- `package.json` 存在，且依赖包含 `react` / `next` / `vite` / `@remix-run`
- `src/App.tsx`、`src/App.jsx`、`app/`、`pages/` 任一存在

命中后继续识别细分信号：
- 框架：Next.js / Vite / Remix
- 类型系统：TypeScript
- 测试：Vitest / Playwright
- 样式：Tailwind CSS
- 数据与状态：TanStack Query / Redux / Zustand / Jotai / Recoil

## 项目扫描命令

```bash
find . \( -name "*.tsx" -o -name "*.ts" -o -name "*.jsx" -o -name "*.js" \) -not -path "./node_modules/*" -not -path "./.git/*" | head -120
```

## 规则文件

`/init` 命中本包时，复制以下规则到项目级 `.ai_code_copilot/rules/`：

- `packs/frontend-react/rules/coding-style.md`
- `packs/frontend-react/rules/project-structure.md`
- `packs/frontend-react/rules/verification.md`

## 常见架构

```
src/
  app/ or pages/      ← 路由
  components/         ← 可复用组件
  features/           ← 业务功能模块
  hooks/              ← React hooks
  services/ or api/   ← API client
  styles/             ← 样式
```

## 构建与测试命令

| 操作 | 命令 |
|------|------|
| 依赖安装 | `npm install` / `pnpm install` / `yarn install` |
| 类型检查 | `npm run typecheck` 或 `tsc --noEmit` |
| 跑全量测试 | `npm test` |
| 跑单文件测试 | `npm test -- <file>` |
| 构建 | `npm run build` |
| Lint | `npm run lint` |

> `/init` 应优先读取 package.json scripts，使用项目已有命令。

## 变更验证矩阵

| 改动场景 | 建议验证 |
|----------|----------|
| TypeScript 类型或共享契约 | `npm run typecheck` + `npm run build` |
| UI 组件行为 | 组件/feature 行为测试；视觉变化需浏览器截图验证 |
| 路由、layout、框架数据加载 | `npm run build` + 路由访问或 Playwright smoke test |
| API client、缓存、异步状态 | API/feature 测试 + loading/error/empty/success 状态验证 |
| 权限、鉴权、破坏性操作 | 正反权限用例 + 敏感流程人工审查 |

## 依赖读取命令

```bash
cat package.json
```
