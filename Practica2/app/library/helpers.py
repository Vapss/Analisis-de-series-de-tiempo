import os.path
import uuid
from pathlib import Path
from PIL import Image
import markdown
import functools


def openfile(filename):
    filepath = os.path.join("Practica2/app/pages/", filename)
    with open(filepath, "r", encoding="utf-8") as input_file:
        text = input_file.read()

    html = markdown.markdown(text)
    data = {
        "text": html
    }
    return data