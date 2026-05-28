---
trigger: always_on
description: 遵循HTTP接口规范
globs: "*.java"
alwaysApply: true
---
## 接口响应报文规范

### 一、响应报文结构

#### 正常响应

> HTTP 状态码和响应报文 `code` 均为 200

```
{
  "params": null,
  "code": 200,
  "status": 1,
  "message": "成功",
  "data": null,
  "success": true
}
```

#### 异常响应

> 网络异常/系统异常/业务异常时，HTTP 状态码统一返回 200，响应报文 `code` 不为 200，具体值由业务场景决定

```
{
  "params": null,
  "code": 400,
  "status": 0,
  "message": "国内车牌号不可为空",
  "data": null,
  "success": false
}
```

### 二、请求方式规范

| 操作类型                   | HTTP 方法 |
| ---------------------------- | ----------- |
| 查询详情                   | GET       |
| 复杂查询、修改、新增、删除 | POST      |

