import gradio as gr
from app.agent.manus import Manus

print("[1] gradio and Manus imported", flush=True)

async def chat(message, history):
    agent = await Manus.create()
    result = await agent.run(message)
    return result

demo = gr.ChatInterface(
    fn=chat,
    title="OpenManus Web UI",
    description="基于本地 Qwen 的 AI 智能体网页聊天界面",
    examples=["用 Python 写一个 hello world 函数并保存到 hello.py"],
)

print("[2] demo created", flush=True)
print("[3] about to launch", flush=True)
demo.launch(
    inbrowser=False,
    server_name="127.0.0.1",
    server_port=7860,
    prevent_thread_lock=False,
)
print("[4] launched - should NOT print if server is blocking", flush=True)
