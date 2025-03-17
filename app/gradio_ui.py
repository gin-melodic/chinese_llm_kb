import gradio as gr
from app.services.knowledge_base import KnowledgeBaseService

def create_gradio_interface():
    kb_service = KnowledgeBaseService()

    with gr.Blocks(title="Knowledge Base Management System") as interface:
        with gr.Tabs():
            # Knowledge base management page
            with gr.Tab("Document Management"):
                dir_input = gr.Textbox(label="Document Directory Path")
                ingest_btn = gr.Button("Import Documents")
                status_output = gr.Textbox(label="Operation Status", interactive=False)
                
                ingest_btn.click(
                    fn=kb_service.ingest_documents,
                    inputs=dir_input,
                    outputs=status_output
                )

            # Chat test page    
            with gr.Tab("Chat Test"):
                msg = gr.Textbox(label="Input Question")
                answer = gr.Textbox(label="Answer Content", lines=5)
                sources = gr.JSON(label="Source Documents")
                
                query_btn = gr.Button("Send Query")
                query_btn.click(
                    fn=kb_service.query_knowledge_base,
                    inputs=msg,
                    outputs=[answer, sources]
                )

        return interface
