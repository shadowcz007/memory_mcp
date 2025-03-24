# Memory MCP 服务器

> 基于 [MCP Servers - memory](https://github.com/modelcontextprotocol/servers/tree/main/src/memory) 改造的知识图谱管理服务器

## 功能特点
- 支持多种启动方式：交互式、命令行、JSON配置
- 完整的知识图谱管理功能
- 自动数据持久化
- 灵活的配置选项

## 快速开始

### 启动方式

1. **交互式启动**
直接运行程序（双击），按提示输入配置：

- 程序会提示输入端口号（默认8080）
- 程序会提示输入内存文件路径（默认为程序所在目录的memory.json）

### 2. 命令行传参

启动服务
```bash
mcp_server_memory.exe --port 8080 --memory-path ./memory.json
```

### 3. JSON配置启动
通过管道传入JSON配置：

```bash
echo '{"jsonrpc": "2.0","method": "start","id": 2,"params":{"port": 8080, "memory_path": "./memory.json"}}' | ./mcp_server_memory.exe
```

获取帮助信息
```bash
echo '{"jsonrpc": "2.0","method": "help","id": 1}' | mcp_server_memory.exe
```

## 客户端接入

[mcp_client.py](mcp_client.py) 是客户端接入示例，使用 [mcp](https://github.com/modelcontextprotocol/mcp) 库实现。

## 配置项

| 参数 | 说明 | 默认值 |
|------|------|--------|
| port | 服务器监听端口 | 8080 |
| memory_path | 数据存储文件路径 | ./memory.json |

## API 接口

### 实体操作
- `create_entities`: 创建实体
- `delete_entities`: 删除实体
- `search_nodes`: 搜索节点
- `open_nodes`: 打开指定节点

### 关系操作
- `create_relations`: 创建关系
- `delete_relations`: 删除关系

### 观察操作
- `add_observations`: 添加观察
- `delete_observations`: 删除观察

### 图谱操作
- `read_graph`: 读取完整图谱

## 数据持久化
- 数据以JSON行格式存储
- 自动保存最新配置到 `config.json`
- 支持相对/绝对路径
- 自动创建不存在的目录

## 注意事项
- Windows系统推荐使用 `\` 或 `\\` 作为路径分隔符
- 确保程序对存储路径有读写权限
- 首次运行自动创建存储文件

## 相关链接
- [GitHub 仓库](https://github.com/shadowcz007/memory_mcp)
- [使用教程](https://mp.weixin.qq.com/s/kiDlpgWqmo0eDYNd7Extmg)

---

<div align="center">
<p style="color: #2ecc71">Starting MCP Memory Server</p>
<p>by Mixlab</p>
</div>