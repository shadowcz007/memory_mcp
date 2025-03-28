from mcp import ClientSession, StdioServerParameters, types
from mcp.client.stdio import stdio_client
from mcp.shared.context import RequestContext
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
    context: RequestContext,  # 添加context参数
    message: types.CreateMessageRequestParams,
) -> types.CreateMessageResult:
    # 这里可以根据message参数进行自定义处理
    # 客户端需要调用LLM处理
    print(f"收到消息创建请求：{json.dumps(message.model_dump(), indent=2, ensure_ascii=False)}")
    
    # 返回正确的CreateMessageResult类型
    return types.CreateMessageResult(
        role="assistant",
        content=types.TextContent(
            type="text", text="LLM处理结果:::假装LLM已经对messages进行了处理并返回"
        ),
        model="test-model",
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
                    # 列出资源
                    resources = await session.list_resource_templates()
                    # 使用 exclude_none=True 来排除空值，使用 by_alias=True 来使用字段别名
                    print(f"资源: {json.dumps(resources.model_dump(exclude_none=True, by_alias=True), indent=2, ensure_ascii=False)}")

                    print("--------------------------------")
                    # 请求资源
                    result = await session.read_resource("memory://short-story/all")
                    # 格式化输出资源内容
                    if result.contents:
                        for content in result.contents:
                            print(f"资源URI: {content.uri}")
                            print(f"MIME类型: {content.mimeType}")
                            print(f"内容: {content.text}")
                    else:
                        print("未找到资源内容")
                    print("--------------------------------")
                    # 请求资源
                    result = await session.read_resource("memory://short-story/草图")
                    # 格式化输出资源内容
                    if result.contents:
                        for content in result.contents:
                            print(f"资源URI: {content.uri}")
                            print(f"MIME类型: {content.mimeType}")
                            print(f"内容: {content.text}")
                    else:
                        print("未找到资源内容")
                    print("--------------------------------")

                    # 列出可用工具
                    tools = await session.list_tools()
                    # 修改工具序列化方式
                    tools_dict = {"tools": [tool.model_dump(exclude_none=True, by_alias=True) for tool in tools.tools]}
                    print(f"可用工具: {json.dumps(tools_dict, indent=2, ensure_ascii=False)}")
                    print("--------------------------------")
                    # 调用工具
                    result = await session.call_tool("read_graph", {})
                    # 修改结果序列化方式
                    result_dict = result.model_dump(exclude_none=True, by_alias=True) if hasattr(result, "model_dump") else result
                    print("调用工具read_graph:", json.dumps(result_dict, indent=2, ensure_ascii=False))
                    print("--------------------------------")
                    
                except Exception as e:
                    print(f"会话操作错误: {e}")
    except Exception as e:
        print(f"连接错误: {e}")


if __name__ == "__main__":
    asyncio.run(run())