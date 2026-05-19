import gradio as gr
from src.core.pipeline import run_pipeline


def create_demo():
    """Create and return the Gradio UI demo."""
    with gr.Blocks(
        title="Multilingual Money Changer",
        theme=gr.themes.Default(),
        css="""
            .main-col { max-width: 720px; margin: 2rem auto; padding: 1.5rem; }
            #title { font-size: 2rem; font-weight: 700; margin-bottom: 0.4rem; }
            #subtitle { color: #444; font-size: 0.92rem; margin-bottom: 1.2rem; }
        """,
    ) as demo:
        with gr.Column(elem_classes="main-col"):
            gr.Markdown("# Multilingual Money Changer", elem_id="title")
            gr.Markdown(
                "Enter the amount and currency. Non-english languages supported. "
                "(e.g., '100 USD to EUR' or '100 US money to England money'):",
                elem_id="subtitle",
            )
            textbox = gr.Textbox(label="", placeholder="", lines=1, show_label=False)
            submit_btn = gr.Button("Submit")
            output = gr.Markdown()

        submit_btn.click(fn=run_pipeline, inputs=textbox, outputs=output)
        textbox.submit(fn=run_pipeline, inputs=textbox, outputs=output)

    return demo
