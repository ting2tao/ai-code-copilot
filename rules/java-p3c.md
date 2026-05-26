---
trigger: always_on
name: java-p3c
description: 遵循阿里巴巴 P3C Java 编码规范
globs: "*.java"
---

## 命名规范
- 类名使用 UpperCamelCase（如 UserService）
- 方法名、变量名使用 lowerCamelCase（如 getUserById）
- 常量使用 UPPER_SNAKE_CASE（如 MAX_RETRY_COUNT）
- 抽象类以 Abstract 或 Base 开头
- 异常类以 Exception 结尾
- 测试类以 Test 结尾

## 代码风格
- 禁止使用魔法值，必须定义常量
- 方法参数不超过 5 个
- 单行代码不超过 120 字符
- 使用 4 空格缩进，禁止 Tab

## OOP 规范
- 避免通过对象引用访问静态变量
- 所有覆写方法必须加 @Override
- 禁止使用过时的类或方法

## 异常处理
- 不要捕获 Exception，应捕获具体异常
- 禁止在 finally 块中使用 return
- 异常信息必须包含上下文

## 代码质量
- 方法不超过 100 行
- 类不超过 1000 行
- 遵循阿里巴巴 Java 开发规范