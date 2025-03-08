import gradio as gr
from whois import whois_info

demo = gr.Interface(
    fn=whois_info,
    inputs=gr.Textbox(label="Enter URL", placeholder="https://example.com"),
    outputs=gr.Textbox(label="Output")
)