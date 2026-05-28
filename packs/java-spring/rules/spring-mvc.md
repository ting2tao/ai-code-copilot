---
name: spring-mvc
description: 遵循 MVC 三层架构规范
globs: "*.java"
alwaysApply: true
---
## 基础环境
- 基于jdk1.8
- 集团脚手架
- maven3

## 分层结构规范

### 标准目录结构
src/main/java/com/gofo/
├── controller/ # 控制层（接收请求、参数校验）
├── service/ # 业务层
│ ├── impl/ # 业务实现类
├── dao/ # 数据访问层（或 mapper/repository）
├── entity/ # 实体类（对应数据库表）
├── dto/ # 数据传输对象（请求/响应）
├── vo/ # 视图对象（返回前端）
├── config/ # 配置类
├── common/ # 公共组件（常量、枚举、工具类）
└── exception/ # 自定义异常

### 依赖规则
- controller → service → dao → entity
- 禁止 controller 直接调用 dao
- 禁止 dao 层包含业务逻辑

### 命名规范
- Controller：实体名+Controller（如 UserController）
- Service 接口：实体名+Service（如 UserService）
- Service 实现：实体名+ServiceImpl（如 UserServiceImpl）
- DAO/Mapper：实体名+Mapper（如 UserMapper）
- DTO：用途+DTO（如 UserCreateDTO、UserQueryDTO）
- VO：用途+VO（如 UserDetailVO、UserListVO）


## Spring Boot 规范
- 配置优先使用 application.yml
- 使用 @ConfigurationProperties 绑定配置
- 异常统一使用 @ControllerAdvice 处理
- 日志使用 SLF4J + Logback

