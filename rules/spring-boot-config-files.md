---
trigger: always_on
name: spring-boot-config-files
description: Spring Boot 项目配置文件强制规范
---
### 📜 Spring Boot 项目配置文件强制规范

​**触发条件（Trigger）**​：
当检测到模块中存在带有 `@SpringBootApplication` 注解的 Java 类时，**必须**在该模块的 `src/main/resources/` 目录下包含以下两个配置文件：

---

#### ✅ 1. `bootstrap.properties`

* ​**路径**​：`src/main/resources/bootstrap.properties`
* ​**内容模板**​：
  
  
```properties
# 应用名称（请替换 ${project.name} 为实际项目名，或通过构建工具注入）
spring.application.name=${project.name}
server.port = ${project.port}
server.servlet.context-path = /${project.name}
spring.application.name = ${project.name}

app.id=${project.name}
apollo.bootstrap.enabled=true
apollo.cluster=default
apollo.bootstrap.namespaces=application,common,nacos
```


> 💡 说明：`bootstrap.properties` 用于 Spring Cloud 应用的早期配置加载（如配置中心、加密密钥等）。若项目未使用 Spring Cloud，可考虑使用 `application.properties` 替代，但本规范要求统一提供 `bootstrap.properties` 以保持一致性。

---

#### ✅ 2. `logback.xml`

* ​**路径**​：`src/main/resources/logback.xml`
* ${project.name} 为实际项目名
* ​**内容模板**​：

```xml
<?xml version="1.0" encoding="UTF-8"?>
<configuration scan="true" scanPeriod="60 seconds">
    
    <property name="LOG_HOME" value="logs/${project.name}"/>
    <property name="APP_NAME" value="${project.name}"/>
    
    <appender name="CONSOLE" class="ch.qos.logback.core.ConsoleAppender">
        <encoder>
            <pattern>%d{yyyy-MM-dd HH:mm:ss.SSS} [%thread] %-5level %logger{50} - %msg%n</pattern>
            <charset>UTF-8</charset>
        </encoder>
    </appender>
    
    <appender name="INFO_FILE" class="ch.qos.logback.core.rolling.RollingFileAppender">
        <file>${LOG_HOME}/${APP_NAME}-info.log</file>
        <filter class="ch.qos.logback.classic.filter.LevelFilter">
            <level>INFO</level>
            <onMatch>ACCEPT</onMatch>
            <onMismatch>DENY</onMismatch>
        </filter>
        <encoder>
            <pattern>%d{yyyy-MM-dd HH:mm:ss.SSS} [%thread] %-5level %logger{50} - %msg%n</pattern>
            <charset>UTF-8</charset>
        </encoder>
        <rollingPolicy class="ch.qos.logback.core.rolling.TimeBasedRollingPolicy">
            <fileNamePattern>${LOG_HOME}/${APP_NAME}-info-%d{yyyy-MM-dd}.%i.log</fileNamePattern>
            <timeBasedFileNamingAndTriggeringPolicy class="ch.qos.logback.core.rolling.SizeAndTimeBasedFNATP">
                <maxFileSize>100MB</maxFileSize>
            </timeBasedFileNamingAndTriggeringPolicy>
            <maxHistory>30</maxHistory>
        </rollingPolicy>
    </appender>
    
    <appender name="ERROR_FILE" class="ch.qos.logback.core.rolling.RollingFileAppender">
        <file>${LOG_HOME}/${APP_NAME}-error.log</file>
        <filter class="ch.qos.logback.classic.filter.LevelFilter">
            <level>ERROR</level>
            <onMatch>ACCEPT</onMatch>
            <onMismatch>DENY</onMismatch>
        </filter>
        <encoder>
            <pattern>%d{yyyy-MM-dd HH:mm:ss.SSS} [%thread] %-5level %logger{50} - %msg%n</pattern>
            <charset>UTF-8</charset>
        </encoder>
        <rollingPolicy class="ch.qos.logback.core.rolling.TimeBasedRollingPolicy">
            <fileNamePattern>${LOG_HOME}/${APP_NAME}-error-%d{yyyy-MM-dd}.%i.log</fileNamePattern>
            <timeBasedFileNamingAndTriggeringPolicy class="ch.qos.logback.core.rolling.SizeAndTimeBasedFNATP">
                <maxFileSize>100MB</maxFileSize>
            </timeBasedFileNamingAndTriggeringPolicy>
            <maxHistory>30</maxHistory>
        </rollingPolicy>
    </appender>
    
    <appender name="ASYNC_INFO" class="ch.qos.logback.classic.AsyncAppender">
        <discardingThreshold>0</discardingThreshold>
        <queueSize>512</queueSize>
        <appender-ref ref="INFO_FILE"/>
    </appender>
    
    <appender name="ASYNC_ERROR" class="ch.qos.logback.classic.AsyncAppender">
        <discardingThreshold>0</discardingThreshold>
        <queueSize>512</queueSize>
        <appender-ref ref="ERROR_FILE"/>
    </appender>
    
    <root level="INFO">
        <appender-ref ref="CONSOLE"/>
        <appender-ref ref="ASYNC_INFO"/>
        <appender-ref ref="ASYNC_ERROR"/>
    </root>
    
</configuration>
```


>  说明：`logback.xml` 是 Spring Boot 默认支持的日志配置文件，优先级高于 `application.properties` 中的日志设置。必须显式提供以确保日志行为可控。

---

### ⚙️ 执行要求

1. ​**自动创建**​：若上述任一文件缺失，应自动在 `@SpringBootApplication` 所在模块的 `src/main/resources/` 目录下创建对应文件，并填充模板内容。
2. ​**变量替换**​：` $ {project.name}` 应由构建工具（如 Maven/Gradle）或 IDE 插件自动替换为实际项目 artifact ID 或自定义名称。
3. ​**位置约束**​：配置文件必须与 `@SpringBootApplication` 类处于**同一 Maven/Gradle 模块**下，不可跨模块引用。

---

### 🚫 例外情况（可选豁免）

* 若项目明确声明​**不使用 Spring Cloud**​，可将 `bootstrap.properties` 替换为 `application.properties`，但需在项目 README 中说明。
* 若使用 Log4j2 等其他日志框架，需提供对应配置文件（如 `log4j2.xml`），并移除 `logback.xml`，但需显式排除 Logback 依赖。
