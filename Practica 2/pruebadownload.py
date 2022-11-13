from fastapi import FastAPI
from fastapi import UploadFile, Query, Form
import pandas as pd
import shutil
import requests
import io

app = FastAPI()

@app.post("/check")
def foo(file: str):
    r = requests.get(file)
    
    if not file.filename.lower().endswith(('.csv',".xlsx",".xls")):
            return 404,"Please upload xlsx,csv or xls file."

    if file.filename.lower().endswith(".csv"):
            extension = ".csv"
    elif file.filename.lower().endswith(".xlsx"):
            extension = ".xlsx"
    elif file.filename.lower().endswith(".xls"):
            extension = ".xls"

        # eventid = datetime.datetime.now().strftime('%Y%m-%d%H-%M%S-') + str(uuid4())
    filepath = "./downloads"+ extension

    with open(filepath, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
        
    try:
        if filepath.endswith(".csv"):
            df = pd.read_csv(filepath)
        else:
            df = pd.read_excel(filepath)
    except:
            return 401, "File is not proper"