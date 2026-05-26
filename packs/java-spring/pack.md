# 规则包：java-spring

## 检测规则

以下任一文件存在则命中本包：
- `pom.xml`
- `build.gradle`
- `build.gradle.kts`

## 项目扫描命令

```bash
find src/main/java -name "*.java" -type f | head -100
```

## 分层架构

```
Controller (web/ 或 controller/)   ← 入口层，参数校验 + 协议转换
    ↓
Service (service/)                  ← 业务编排，事务边界
    ↓
Manager (manager/)                  ← 领域能力，单一职责，可复用
    ↓
DAO (dao/ 或 mapper/)               ← 纯数据访问
```

## 构建与测试命令

| 操作 | 命令（Maven） | 命令（Gradle） |
|------|-------------|--------------|
| 编译检查 | `mvn compile -q` | `./gradlew compileJava` |
| 跑全量测试 | `mvn test` | `./gradlew test` |
| 跑单模块 | `mvn test -pl <module>` | `./gradlew :<module>:test` |

> `/init` 检测到本包时，优先用 Maven；若无 pom.xml 只有 build.gradle 则用 Gradle。
> 填充 project-context.md 时记录实际使用的命令。

## 依赖读取命令

```bash
# Maven
cat pom.xml | grep -E "<artifactId>|<version>" | head -40

# Gradle
cat build.gradle | grep -E "implementation|testImplementation" | head -40
```
