# FastX-Tui 插件配置接入指南

本文档详细说明FastX-Tui示例插件的配置是如何接入FastX-Tui系统的，包括配置定义、配置使用、配置管理和配置界面。

## 1. 配置定义

### 1.1 配置定义方式

示例插件通过`get_config_schema()`方法定义配置项，该方法返回一个字典，包含插件的所有配置项及其约束。

### 1.2 配置项结构

每个配置项包含以下字段：

| 字段名 | 类型 | 说明 |
|-------|------|------|
| type | str | 配置项类型，支持：string, boolean, integer, number |
| default | Any | 配置项默认值 |
| description | str | 配置项描述 |
| required | bool | 是否必填 |
| choices | List[Any] | 可选值列表（仅适用于枚举类型） |
| min | int | 最小值（仅适用于数值类型） |
| max | int | 最大值（仅适用于数值类型） |

### 1.3 示例插件配置定义

示例插件在`fastx_tui_plugin.py`中定义了以下配置项：

```python
def get_config_schema(self) -> Dict[str, Any]:
    """获取插件配置模式"""
    return {
        "enabled": {
            "type": "boolean",
            "default": True,
            "description": "是否启用该插件",
            "required": True
        },
        "greeting_message": {
            "type": "string",
            "default": "Hello from Example Plugin!",
            "description": "用于Hello World命令的问候信息",
            "required": False
        },
        "show_timestamp": {
            "type": "boolean",
            "default": True,
            "description": "是否在输出中显示时间戳",
            "required": False
        },
        "log_level": {
            "type": "string",
            "default": "INFO",
            "description": "插件的日志级别",
            "choices": ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
            "required": False
        }
    }
```

## 2. 配置使用

### 2.1 获取配置值

插件通过`get_config()`方法获取配置值，该方法由Plugin基类提供，实际实现由PluginManager动态替换，使用配置管理器获取配置。

### 2.2 使用示例

#### 2.2.1 在初始化中使用配置

示例插件在`example_business.py`的`initialize()`方法中获取配置：

```python
def initialize(self):
    """初始化业务逻辑"""
    # 从配置中获取初始化参数
    self.greeting_message = self.plugin.get_config("greeting_message", "Hello from Example Plugin!")
    self.show_timestamp = self.plugin.get_config("show_timestamp", True)
    self.log_level = self.plugin.get_config("log_level", "INFO")
    
    self.plugin.log_info(f"示例插件初始化完成，问候语: {self.greeting_message}")
    self.plugin.log_info(f"显示时间戳: {self.show_timestamp}")
    self.plugin.log_info(f"日志级别: {self.log_level}")
```

#### 2.2.2 在业务方法中使用配置

示例插件在`hello_world()`方法中获取配置：

```python
def hello_world(self) -> str:
    """演示基本命令执行"""
    # 获取配置
    greeting = self.plugin.get_config("greeting_message", "Hello World!")
    show_timestamp = self.plugin.get_config("show_timestamp", True)
    
    # 构建响应
    result = f"{greeting}\n"
    if show_timestamp:
        result += f"当前时间: {time.strftime('%Y-%m-%d %H:%M:%S')}\n"
    result += f"插件版本: {self.plugin.get_info().version}\n"
    result += "命令执行成功!"
    
    return result
```

## 3. 配置管理

### 3.1 配置存储

插件配置存储在FastX-Tui的主配置文件中，使用`plugin_{plugin_name}`作为键，存储插件的所有配置项。

### 3.2 配置访问

#### 3.2.1 插件内部访问

插件通过`get_config()`和`set_config()`方法访问和修改配置，这些方法由PluginManager动态替换，使用配置管理器获取和设置配置：

```python
def plugin_get_config(config_name, default=None):
    plugin_config = self.plugin_configs.get(plugin_name, {})
    return plugin_config.get(config_name, default)
def plugin_set_config(config_name, value):
    if plugin_name not in self.plugin_configs:
        self.plugin_configs[plugin_name] = {}
    self.plugin_configs[plugin_name][config_name] = value
    self._save_plugin_configs()
```

#### 3.2.2 系统访问

系统通过`config_manager.get_config(f"plugin_{plugin_name}", {})`访问插件配置。

### 3.3 配置持久化

插件配置在修改后自动持久化到配置文件中，由ConfigManager负责管理。

## 4. 配置界面

### 4.1 配置界面入口

用户可以通过以下路径访问插件配置：

1. 主菜单 -> 配置管理
2. 选择 "4. 插件配置管理"

### 4.2 配置界面流程

1. **插件列表**：显示所有已加载的插件
2. **选择插件**：用户选择要配置的插件
3. **插件配置**：显示选定插件的所有配置项
4. **修改配置**：用户可以修改配置项的值
5. **保存配置**：修改后的值自动保存到配置文件

### 4.3 配置界面实现

配置界面由`ConfigInterface`类实现，主要方法包括：

1. `_show_plugin_config()`：显示插件配置主界面
2. `_show_single_plugin_config()`：显示单个插件的配置
3. `_modify_plugin_config()`：修改插件配置

#### 4.3.1 显示插件配置主界面

```python
def _show_plugin_config(self):
    """显示插件配置界面"""
    if not self.plugin_manager:
        self._show_message("插件管理器未初始化", "red")
        return
    
    plugins = self.plugin_manager.list_plugins()
    plugin_list = [plugin for plugin in plugins if plugin["loaded"]]
    
    # 显示插件列表，供用户选择
    # ...
```

#### 4.3.2 显示单个插件配置

```python
def _show_single_plugin_config(self, plugin, plugin_info):
    """显示单个插件的配置"""
    # 获取插件配置模式
    config_schema = plugin.get_config_schema()
    
    # 获取插件配置
    plugin_config = self.config_manager.get_config(f"plugin_{plugin_info['name']}", {})
    
    # 显示配置项，供用户修改
    # ...
```

## 5. 配置验证

插件配置在修改时会进行验证，确保符合配置模式中定义的约束：

- 类型验证：确保值的类型符合配置项定义
- 可选值验证：确保值在可选值列表中（如果定义了choices）
- 范围验证：确保值在指定范围内（如果定义了min/max）

## 6. 最佳实践

1. **合理定义配置项**：只定义必要的配置项，避免过多配置项增加用户负担
2. **提供默认值**：为所有配置项提供合理的默认值
3. **详细描述**：为每个配置项提供清晰的描述，说明其用途和影响
4. **使用合适的类型**：根据配置项的实际用途选择合适的类型
5. **添加约束**：为配置项添加适当的约束，如可选值、范围等
6. **在初始化时获取配置**：在`initialize()`方法中获取配置，避免在业务方法中频繁获取
7. **使用日志记录配置**：在初始化时记录配置值，便于调试和问题排查

## 7. 示例插件配置接入总结

| 配置项 | 类型 | 默认值 | 说明 |
|-------|------|--------|------|
| enabled | boolean | True | 是否启用该插件 |
| greeting_message | string | "Hello from Example Plugin!" | 用于Hello World命令的问候信息 |
| show_timestamp | boolean | True | 是否在输出中显示时间戳 |
| log_level | string | "INFO" | 插件的日志级别，可选值：DEBUG, INFO, WARNING, ERROR, CRITICAL |

### 7.1 配置使用流程

1. 插件通过`get_config_schema()`定义配置项
2. 插件在初始化和业务方法中通过`get_config()`获取配置值
3. 用户通过配置界面修改配置
4. 配置修改后自动保存到配置文件
5. 插件重启后加载新的配置值

### 7.2 配置管理流程

1. ConfigManager负责配置的存储和管理
2. PluginManager负责插件配置的访问和修改
3. ConfigInterface提供配置界面，供用户操作

## 8. 扩展阅读

- [FastX-Tui 插件开发指南](PLUGIN_DEVELOPMENT_GUIDE.md)
- [FastX-Tui 插件系统蓝图](PLUGIN_SYSTEM_BLUEPRINT.md)
- [FastX-Tui 配置管理](features/config/README.md)

## 9. 常见问题

### 9.1 配置不生效

**问题**：修改插件配置后，插件行为没有变化

**解决方法**：
1. 确保插件已重新加载（修改配置后自动重载）
2. 检查配置项名称是否正确
3. 检查配置值是否符合约束
4. 查看日志文件，确认是否有配置加载错误

### 9.2 配置丢失

**问题**：重启应用后，插件配置丢失

**解决方法**：
1. 确保配置文件有写入权限
2. 检查配置文件路径是否正确
3. 查看日志文件，确认是否有配置保存错误

### 9.3 配置项不显示

**问题**：插件配置界面中没有显示某个配置项

**解决方法**：
1. 确保配置项在`get_config_schema()`中正确定义
2. 检查配置项是否被标记为`required: True`
3. 确保插件已正确加载

## 10. 示例插件配置接入示意图

```
┌─────────────────────────────────────────────────────────┐
│                     配置管理中心                         │
└─────────────────────────────────────────────────────────┘
                                 │
                                 ▼
┌─────────────────────────────────────────────────────────┐
│                  插件配置管理                            │
└─────────────────────────────────────────────────────────┘
                                 │
                                 ▼
┌─────────────────────────────────────────────────────────┐
│                 选择插件                                 │
└─────────────────────────────────────────────────────────┘
                                 │
                                 ▼
┌─────────────────────────────────────────────────────────┐
│                  插件配置界面                            │
└─────────────────────────────────────────────────────────┘
                                 │
                                 ▼
┌─────────────────────────────────────────────────────────┐
│                  修改配置值                              │
└─────────────────────────────────────────────────────────┘
                                 │
                                 ▼
┌─────────────────────────────────────────────────────────┐
│                  保存配置到文件                          │
└─────────────────────────────────────────────────────────┘
                                 │
                                 ▼
┌─────────────────────────────────────────────────────────┐
│                  插件加载配置                            │
└─────────────────────────────────────────────────────────┘
                                 │
                                 ▼
┌─────────────────────────────────────────────────────────┐
│                  插件使用配置                            │
└─────────────────────────────────────────────────────────┘
```

通过以上流程，示例插件的配置成功接入FastX-Tui系统，用户可以通过配置界面方便地管理插件配置。