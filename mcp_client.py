from mcp import ClientSession, StdioServerParameters, types
from mcp.client.stdio import stdio_client
import asyncio
import platform
import json  # 添加 json 模块导入

# Create server parameters for stdio connection
server_params = StdioServerParameters(
    command="dist/mcp_server_memory" if platform.system() != "Windows" else "dist/mcp_server_memory.exe",  # 根据系统选择可执行文件
    args=["--transport", "stdio"],  # 确保使用 stdio 传输模式
    env=None,  # 可选环境变量
)


# Optional: create a sampling callback
async def handle_sampling_message(
    message: types.CreateMessageRequestParams,
) -> types.CreateMessageResult:
    return types.CreateMessageResult(
        role="assistant",
        content=types.TextContent(
            type="text",
            text="Hello, world! from model",
        ),
        model="gpt-3.5-turbo",
        stopReason="endTurn",
    )


async def run():
    try:
        print("正在启动 stdio 客户端...")
        async with stdio_client(server_params) as (read, write):
            print("stdio 客户端已启动，正在创建会话...")
            async with ClientSession(
                read, write, sampling_callback=handle_sampling_message
            ) as session:
                try:
                    # 初始化连接
                    print("正在初始化会话...")
                    await session.initialize()
                    print("会话初始化成功")
                    print("--------------------------------")
                    # 列出可用工具
                    tools = await session.list_tools()
                    # 将 ListToolsResult 对象转换为可序列化的字典
                    tools_dict = {"tools": [tool.model_dump() for tool in tools.tools]}
                    print(f"可用工具: {json.dumps(tools_dict, indent=2, ensure_ascii=False)}")
                    print("--------------------------------")
                    # 这里可以添加调用工具的代码
                    result = await session.call_tool("read_graph", {})
                    # 同样需要确保 result 是可序列化的
                    result_dict = result.model_dump() if hasattr(result, "model_dump") else result
                    print("调用工具read_graph:", json.dumps(result_dict, indent=2, ensure_ascii=False))
                    print("--------------------------------")
                    
                except Exception as e:
                    print(f"会话操作错误: {e}")
    except Exception as e:
        print(f"连接错误: {e}")


if __name__ == "__main__":
    asyncio.run(run())