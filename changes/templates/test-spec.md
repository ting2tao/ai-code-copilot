# 测试 Spec：{变更名}

> **关联 Spec**：`spec.md`
> **Red/Green 铁律**：每个测试必须先验证 RED（测试确实失败），再实施代码使其 GREEN。跳过 RED 的测试视为无效。
> **覆盖率门禁**：statement ≥ 80%，branch ≥ 70%

---

## P0 核心逻辑测试（必测）

> 覆盖主流程 + 关键边界。单元测试，Mockito mock 外部依赖。

### TC-P0-01：{测试场景名}

**测试类**：`{XxxServiceTest.java}`
**测试方法**：`test_{场景描述}()`
**前置条件**：{数据准备、mock 设置}
**操作**：{调用什么方法，传什么参数}
**预期结果**：{断言什么}

```java
@Test
void test_{场景描述}() {
    // given
    {mock 设置}
    
    // when
    {调用}
    
    // then
    {断言}
}
```

### TC-P0-02：{异常场景}

**测试类**：`{XxxServiceTest.java}`
**前置条件**：{触发异常的条件}
**预期结果**：抛出 `{XxxException}`，message 包含 `{关键字}`

---

## P1 数据层测试（应测）

> Mapper/Repository 层，使用 H2 或 @MybatisTest。

### TC-P1-01：{数据操作场景}

**测试类**：`{XxxMapperTest.java}`
**操作**：{insert/select/update/delete}
**预期结果**：{数据变更验证}

---

## P2 入口层测试（选测）

> Controller 层，MockMvc，验证 HTTP 状态码 + 响应结构。

### TC-P2-01：{接口场景}

**测试类**：`{XxxControllerTest.java}`
**请求**：`{METHOD} {/path}` Body: `{json}`
**预期**：HTTP `{status}`，响应包含 `{字段=值}`

---

## 覆盖率目标

| 类 | Statement | Branch | 备注 |
|----|-----------|--------|------|
| `{XxxServiceImpl}` | ≥ 80% | ≥ 70% | |
| `{XxxMapper}` | ≥ 80% | - | |

---

## 实际测试结果

> /test 完成后填写，必须粘贴 `mvn test` 实际输出

```
{mvn test 实际输出}
```

覆盖率报告：`target/site/jacoco/index.html`
