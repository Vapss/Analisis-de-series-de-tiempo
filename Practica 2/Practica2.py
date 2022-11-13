import io
import shutil
from math import sqrt

import numpy as np
import pandas as pd
import requests
from fastapi import FastAPI, Form, Query, UploadFile
from matplotlib import pyplot
from pandas import read_csv
# basemodel
from pydantic import BaseModel
from sklearn.metrics import mean_squared_error
from statsmodels.tsa.ar_model import AutoReg
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi import FastAPI, Request




class Item(BaseModel):
    data_url : str


from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from library.helper import *


app = FastAPI()

templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    data = openfile("home.md")
    return templates.TemplateResponse("page.html", {"request": request, "data": data})
    
@app.get("/page/{page_name}", response_class=HTMLResponse)
async def show_page(request: Request, page_name: str):
    data = openfile(page_name+".md")
    return templates.TemplateResponse("page.html", {"request": request, "data": data})

@app.post("/trend/detrending/linear")
async def detrending_linear(item: Item):
    r = requests.get(item.data_url)
    with open("data.csv", "wb") as buffer:
        buffer.write(r.content)
    df = pd.read_csv("data.csv")

    data = df["T1"]

    # split dataset
    X = data.values
    train, test = X[1:len(X)-7], X[len(X)-7:]
    # train autoregression
    model = AutoReg(train, lags=29)
    model_fit = model.fit()
    #print('Coefficients: %s' % model_fit.params)
    # make predictions
    predictions = model_fit.predict(start=len(train), end=len(train)+len(test)-1, dynamic=False)
    #for i in range(len(predictions)):
	 #   print('predicted=%f, expected=%f' % (predictions[i], test[i]))
    rmse = sqrt(mean_squared_error(test, predictions))
    #print('Test RMSE: %.3f' % rmse)
    # plot results
    #pyplot.plot(test)
    #pyplot.plot(predictions, color='red')
    #pyplot.show()

    # Coefficients to list
    coef = model_fit.params.tolist()
    # Predictions to list
    predictions = predictions.tolist()
    # Expected to list
    expected = test.tolist()
    # Create a list of lists
    list_of_lists = [predictions, expected]

    # Return
    return {"Model_weights": coef, "predictions": predictions, "expected": expected}








