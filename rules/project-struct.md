---
name: 集团脚手架
description: 新增项目或使用中间件时，必须优先选用【公司自定义组件&脚手架】，禁止直接引入外部开源组件
alwaysApply: true
---

## 分布式微服务项目（Spring Cloud）父pom.xml

```xml
<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 
         http://maven.apache.org/xsd/maven-4.0.0.xsd">
    <modelVersion>4.0.0</modelVersion>

    <!-- 微服务父依赖 -->
    <parent>
        <groupId>com.zt</groupId>
        <artifactId>zt-digital-springcloud-parent</artifactId>
        <version>1.5.7.RELEASE</version>
        <relativePath/>
    </parent>

    <groupId>com.zt</groupId>
    <artifactId>your-project-parent</artifactId>
    <version>1.0.0-RELEASE </version>
    <packaging>pom</packaging>
    <description>您的项目描述</description>

   

    <modules>
        <module>your-service-api</module>
        <module>your-service-biz</module>
        <module>your-service-impl</module>
        <module>your-gateway</module>
    </modules>

    <properties>
        <java.version>1.8</java.version>
        <project.build.sourceEncoding>UTF-8</project.build.sourceEncoding>
        <project.reporting.outputEncoding>UTF-8</project.reporting.outputEncoding>
        <maven.compiler.source>1.8</maven.compiler.source>
        <maven.compiler.target>1.8</maven.compiler.target>
    </properties>

    <dependencyManagement>
        <dependencies>
            <!-- 统一启动类 -->
            <dependency>
                <groupId>com.zt</groupId>
                <artifactId>zt-digital-common-boot-starter</artifactId>
                <version>1.5.7.RELEASE</version>
            </dependency>
            
            <!-- API基础组件 -->
            <dependency>
                <groupId>com.zt</groupId>
                <artifactId>zt-digital-common-api-base</artifactId>
                <version>1.5.7.RELEASE</version>
            </dependency>
            
            <!-- 常用组件依赖管理（根据需要添加） -->
            <dependency>
                <groupId>com.zt</groupId>
                <artifactId>zt-digital-common-log-starter</artifactId>
                <version>1.5.7.RELEASE</version>
            </dependency>
            <dependency>
                <groupId>com.zt</groupId>
                <artifactId>zt-digital-common-config-starter</artifactId>
                <version>1.5.7.RELEASE</version>
            </dependency>
            <dependency>
                <groupId>com.zt</groupId>
                <artifactId>zt-digital-common-register-start</artifactId>
                <version>1.5.7.RELEASE</version>
            </dependency>
            <!-- 其他组件... -->
        </dependencies>
    </dependencyManagement>
</project>
```

## 单体应用项目父pom.xml



```xml
<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 
         http://maven.apache.org/xsd/maven-4.0.0.xsd">
    <modelVersion>4.0.0</modelVersion>

    <!-- 顶级父依赖 -->
    <parent>
        <groupId>com.zt</groupId>
        <artifactId>zt-digital-dependencies</artifactId>
        <version>1.5.7.RELEASE</version>
    </parent>

    <groupId>com.zt</groupId>
    <artifactId>your-single-app</artifactId>
    <version>1.0.0-SNAPSHOT</version>
    <packaging>jar</packaging>
    <description>您的单体应用描述</description>

    <!-- 单体应用父依赖 -->
    <parent>
        <groupId>com.zt</groupId>
        <artifactId>zt-digital-springboot-parent</artifactId>
        <version>1.5.7.RELEASE</version>
        <relativePath/>
    </parent>

    <dependencies>
        <!-- 统一启动类（必须） -->
        <dependency>
            <groupId>com.zt</groupId>
            <artifactId>zt-digital-common-boot-starter</artifactId>
        </dependency>
        
        <!-- API基础组件（必须） -->
        <dependency>
            <groupId>com.zt</groupId>
            <artifactId>zt-digital-common-api-base</artifactId>
        </dependency>
        
        <!-- 日志组件（推荐） -->
        <dependency>
            <groupId>com.zt</groupId>
            <artifactId>zt-digital-common-log-starter</artifactId>
        </dependency>
        
        <!-- 工具类（推荐） -->
        <dependency>
            <groupId>com.zt</groupId>
            <artifactId>zt-digital-common-util</artifactId>
            <version>1.5.7.RELEASE</version>
        </dependency>
        
        <!-- 根据项目需求添加其他组件 -->
        <dependency>
            <groupId>com.zt</groupId>
            <artifactId>zt-digital-mybatis-starter</artifactId>
            <version>1.5.7.RELEASE</version>
        </dependency>
        
        <dependency>
            <groupId>com.zt</groupId>
            <artifactId>zt-digital-common-cache-starter</artifactId>
            <version>1.5.7.RELEASE</version>
        </dependency>
        
        <!-- Swagger API文档（开发环境） -->
        <dependency>
            <groupId>com.zt</groupId>
            <artifactId>zt-digital-common-swagger-starter</artifactId>
            <version>1.5.7.RELEASE</version>
            <scope>provided</scope>
        </dependency>
    </dependencies>
</project>
```

## 微服务模块示例（service模块）



```xml
<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 
         http://maven.apache.org/xsd/maven-4.0.0.xsd">
    <modelVersion>4.0.0</modelVersion>
    
    <parent>
        <groupId>com.zt</groupId>
        <artifactId>your-project-parent</artifactId>
        <version>1.0.0-SNAPSHOT</version>
    </parent>
    
    <artifactId>your-service-biz</artifactId>
    
    <dependencies>
        <!-- 核心启动类 -->
        <dependency>
            <groupId>com.zt</groupId>
            <artifactId>zt-digital-common-boot-starter</artifactId>
        </dependency>
        
        <!-- API基础 -->
        <dependency>
            <groupId>com.zt</groupId>
            <artifactId>zt-digital-common-api-base</artifactId>
        </dependency>
        
        <!-- 微服务核心三件套 -->
        <dependency>
            <groupId>com.zt</groupId>
            <artifactId>zt-digital-common-log-starter</artifactId>
        </dependency>
        <dependency>
            <groupId>com.zt</groupId>
            <artifactId>zt-digital-common-config-starter</artifactId>
        </dependency>
        <dependency>
            <groupId>com.zt</groupId>
            <artifactId>zt-digital-common-register-start</artifactId>
        </dependency>
        
        <!-- 熔断限流 -->
        <dependency>
            <groupId>com.zt</groupId>
            <artifactId>zt-digital-common-fuse-starter</artifactId>
            <version>1.5.7.RELEASE</version>
        </dependency>
        
        <!-- 数据库 -->
        <dependency>
            <groupId>com.zt</groupId>
            <artifactId>zt-digital-common-mybatis-starter</artifactId>
            <version>1.5.7.RELEASE</version>
        </dependency>
        
        <!-- 监控 -->
        <dependency>
            <groupId>com.zt</groupId>
            <artifactId>zt-digital-common-micrometer-starter</artifactId>
            <version>1.5.7.RELEASE</version>
        </dependency>
    </dependencies>
</project>
```

## 项目创建规则清单

### 必须遵循的规则：

1. ​**版本统一**​：所有组件必须使用 `1.5.7.RELEASE` 版本
2. ​**父依赖选择**​：
   * 微服务项目 → `zt-digital-springcloud-parent`
   * 单体应用 → `zt-digital-springboot-parent`
3. ​**核心依赖**​（必须包含）：
   * `zt-digital-common-boot-starter`
   * `zt-digital-common-api-base`

### 推荐配置：

1. ​**所有项目都应包含**​：
   * `zt-digital-common-log-starter`
   * `zt-digital-common-util`
2. ​**微服务项目加配**​：
   * `zt-digital-common-config-starter`
   * `zt-digital-common-register-start`
   * `zt-digital-common-fuse-starter`
3. ​**Web项目加配**​：
   * `zt-digital-common-swagger-starter`（开发环境）
   * `zt-digital-common-security-starter`（需要安全认证）
