import gradio as gr

from app.vector_store import list_files, COLL_NAME


def build_admin():
    with gr.Blocks(analytics_enabled=False) as admin:
        gr.Checkboxgroup(list_files(COLL_NAME))
        gr.Button("Удалить")
    return admin
