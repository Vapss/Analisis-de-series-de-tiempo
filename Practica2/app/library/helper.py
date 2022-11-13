import os.path
import markdown


def openfile(filename):
    filepath = os.path.join("/Users/vaps/Documents/GitHub/Analisis-de-series-de-tiempo/Practica 2/pages", filename)
    with open(filepath, "r", encoding="utf-8") as input_file:
        text = input_file.read()

    html = markdown.markdown(text)
    data = {
        "text": html
    }
    return data