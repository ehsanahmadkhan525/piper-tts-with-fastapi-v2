import io
import os
import wave
from typing import Any, Dict

import librosa
import pyrubberband
import soundfile as sf
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response
from pydantic import BaseModel

from . import PiperVoice
from .download import ensure_voice_exists, find_voice, get_voices

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

MODEL_PATH = os.getenv("MODEL_PATH", "src/python_run/no_NO-talesyntese-medium.onnx")
CONFIG_PATH = None
USE_CUDA = False


model_path = MODEL_PATH
config_path = CONFIG_PATH
voice = PiperVoice.load(model_path, config_path=config_path, use_cuda=USE_CUDA)


app = FastAPI()


class SynthesisRequest(BaseModel):
    text: str
    file_name: str


@app.post("/tts/", response_class=Response)
async def tts(request: SynthesisRequest):
    """
    Text-to-Speech (TTS) endpoint.

    Args:
        Give the text that will be converted to TTS and the file name.

    Returns:
        Response: The HTTP response object with the synthesized audio file saved as "Analysed_{file_name}.wav".
    """
    text = request.text.strip()

    synthesize_args = {
        "speaker_id": 0,
        "length_scale": None,
        "noise_scale": None,
        "noise_w": None,
        "sentence_silence": 0.0,
    }

    if not text:
        raise ValueError("No text provided")

    file_name = request.file_name
    with wave.open(f"{file_name}.wav", "wb") as wav_file:
        voice.synthesize(text, wav_file, **synthesize_args)

    filepath = f"{file_name}.wav"
    analyzed_filepath = f"analyzed{file_name}.wav"

    y, sr = librosa.load(filepath, sr=None)
    y_stretched = pyrubberband.time_stretch(y, sr, 0.9)
    sf.write(analyzed_filepath, y_stretched, sr, format="wav")
    return Response(f'Audio saved as "Analysed_{file_name}.wav"')
