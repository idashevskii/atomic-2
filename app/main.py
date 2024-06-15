import logging
import gradio as gr

from llm_stub import infer

def respond(message, chat_history):
    response = infer("Answer briefly in Russian language", message)
    judge = infer("Is it a clear question which can be answered in the single word?. Answer YES or NO.", message)
    logging.info("%s => [%s] %s ", message, judge, response)
    l_judge = judge.lower()
    if cant_give_a:=("нет" in l_judge or "no" in l_judge):
        gr.Info("Переформулируйте вопрос")

    summon = len(chat_history)>0
    chat_history.append((message, response if not cant_give_a else "Вопрос не ясен. Переформулируйте пожалуйста\n<details><summary>возможный ответ</summary>%s</details>"%response))

    return "", chat_history, gr.Button(visible=False)

def call_func():
    gr.Info("Звоню...")

def vote(data: gr.LikeData, chat):
    logging.info("%s %s", data, chat)
    return gr.Button(visible=not data.liked)

def build_gradio():
    # Function to handle the user's message and generate a response
    with gr.Blocks(analytics_enabled=False, css=".built-with{display:none!important}") as demo:
        with gr.Row():
            chatbot = gr.Chatbot(scale=5)
            callop=gr.Button("Позвать оператора", visible=False, scale=1)#, link="help.greenatom.com")

        msg = gr.Textbox(label="Message")
        clear = gr.Button("Clear")

        msg.submit(respond, [msg, chatbot], [msg, chatbot, callop])
        clear.click(lambda: [[], gr.Button(visible=False)], None, [chatbot,callop], queue=False)
        callop.click(call_func,queue=True)
        chatbot.like(vote, [chatbot],[callop])
    return demo

demo = build_gradio()

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')

# Launch the interface
demo.launch(server_name='0.0.0.0', ssl_verify=False)
