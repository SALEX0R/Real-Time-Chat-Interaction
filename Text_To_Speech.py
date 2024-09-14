import os
import torch
from TTS.api import TTS
import gradio as gr

device = "cuda" if torch.cuda.is_available() else "cpu"

def generate_audio(text="Well, it's Nice to meet you and i hope you are doing well."):
    tts = TTS(model_name='tts_models/en/ljspeech/fast_pitch').to(device)
    tts.tts_to_file(text=text, file_path="Output/audio.wav")
    return "Output/audio.wav"

# #design an interface

# demo = gr.Interface(
#     fn=generate_audio,
#     inputs=[gr.Text(label="Text"),],
#     outputs=[gr.Audio(label="Audio")],
# )

# demo.launch()

demo = gr.Interface(
    fn=generate_audio,
    inputs=[gr.Textbox(label="Text", placeholder="Enter your text here...")],
    outputs=[gr.Audio(label="Audio")],
    title="Text-to-Speech Demo",
    description="Enter your text, and I'll convert it to speech!"
)


demo.launch()