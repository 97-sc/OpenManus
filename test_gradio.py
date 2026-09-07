import gradio as gr

print("[1] gradio imported", flush=True)

def respond(message, history):
    return f"Echo: {message}"

demo = gr.ChatInterface(
    fn=respond,
    title="Test"
)

print("[2] demo created", flush=True)

print("[3] about to launch", flush=True)
demo.launch(
    inbrowser=False,
    server_name="127.0.0.1",
    server_port=7860
)
print("[4] launched - should NOT print if server is blocking", flush=True)
