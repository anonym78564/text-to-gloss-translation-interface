import time
import gradio as gr
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

tokenizer_hf = AutoTokenizer.from_pretrained("")
model_hf = AutoModelForSeq2SeqLM.from_pretrained("")

def translate_texts_for_gradio(text: str):
    inputs = tokenizer_hf(text, return_tensors="pt")

    outputs = model_hf.generate(
        **inputs,
        max_new_tokens=60,
        num_beams=4,
        early_stopping=True,
        repetition_penalty=1.1,
    )
    gloss_sentence = tokenizer_hf.decode(outputs[0], skip_special_tokens=True).strip()
    return gloss_sentence

def respond(message, history):

    response = translate_texts_for_gradio(message)

    history = history + [(message, "")]
    partial = ""

    for char in response:
        partial += char
        history[-1] = (message, partial)
        time.sleep(0.01)
        yield "", history


with gr.Blocks(
    theme=gr.themes.Monochrome()
) as demo:

    gr.Markdown(
        """
        # 🤖 Text-to-Gloss Translation
        """
    )

    chatbot = gr.Chatbot(
        elem_id="chatbot",
        bubble_full_width=False
    )

    with gr.Row():

        msg = gr.Textbox(
            placeholder="Write down text here...",
            show_label=False,
            scale=9
        )

        send = gr.Button("Send ", scale=1)

    clear = gr.Button("🗑 Delete chat")

    send.click(respond, [msg, chatbot], [msg, chatbot])
    msg.submit(respond, [msg, chatbot], [msg, chatbot])

    clear.click(lambda: None, None, chatbot, queue=False)


demo.launch()
demo = gr.Interface(fn=translate_texts_for_gradio, inputs="text", outputs="text")
demo.launch()