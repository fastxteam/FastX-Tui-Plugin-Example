# 示例插件手册

## 概述

示例插件演示了如何使用FastX-Tui插件接口，包括：
- 实现插件手册
- 定义配置模式
- 在业务逻辑中使用配置
- 分离入口文件和业务逻辑

## 功能

### Hello World

显示问候信息，演示基本命令执行。

### 配置演示

演示如何在插件中使用配置参数。

## 配置

### greeting_message

- 类型: 字符串
- 默认值: "Hello from Example Plugin!"
- 说明: 用于Hello World命令的问候信息

### show_timestamp

- 类型: 布尔值
- 默认值: True
- 说明: 是否在输出中显示时间戳

### log_level

- 类型: 字符串
- 默认值: "INFO"
- 说明: 插件的日志级别
- 可选值: "DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"

## 使用示例

1. 选择"示例插件"菜单
2. 选择"Hello World"命令查看问候信息
3. 选择"配置演示"命令查看配置使用
4. 在配置管理中修改插件配置

## 开发说明

该插件演示了FastX-Tui插件的最佳实践：
- 分离入口文件和业务逻辑
- 使用配置管理系统
- 实现插件手册
- 遵循插件接口规范
- 使用日志系统

## 插件结构

```
FastX-Tui-Plugin-Example/
├── fastx_tui_plugin.py      # 插件入口文件
├── example_business.py      # 业务逻辑文件
├── manual.md                # 插件手册
├── config_schema.json       # 配置模式
└── README.md                # 插件说明文档
```

## 版本历史

### v1.0.0
- 初始版本
- 实现基本命令执行
- 实现配置演示
- 添加帮助文档
- 分离入口文件和业务逻辑