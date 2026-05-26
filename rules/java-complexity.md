---
trigger: always_on
name: java-complexity
description: 控制代码圈复杂度，提升可维护性
globs: "*.java"
---

## 圈复杂度规范

### 方法复杂度限制
- 单个方法圈复杂度不超过 10
- 超过 10 时必须拆分为多个小方法
- 复杂度超过 15 的方法禁止提交

### 降低复杂度的方法
- 使用卫语句（Guard Clause）提前返回
- 用多态替代复杂的 if-else/switch
- 提取私有方法封装条件逻辑
- 使用 Optional 替代 null 检查
- 用 Stream API 替代复杂循环

### 示例重构
```java
// 避免：复杂度高
if (a) {
    if (b) {
        if (c) { ... }
    }
}

// 推荐：卫语句
if (!a) return;
if (!b) return;
if (!c) return;
// 核心逻辑
```*