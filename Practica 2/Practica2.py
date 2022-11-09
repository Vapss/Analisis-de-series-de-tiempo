from fastapi import FastAPI
import pandas as pd
import io
from fastapi.responses import StreamingResponse
from sklearn.linear_model import LinearRegression
import numpy as np
from pydantic import BaseModel

class Item(BaseModel):
    data_url : str


app = FastAPI()

@app.post("/trend/detrending/linear")
async def detrending_linear(item: Item):

# Download and read the data from de data_url. Prediction Value is contained in the prediction column
    df = pd.read_csv(item.data_url)
    df = df.dropna()
    x = df.index.values.reshape(-1,1)
    y = df['prediction'].values.reshape(-1,1)
    model = LinearRegression()
    model.fit(x,y)
    trend = model.predict(x)
    detrended = y - trend
    df['detrended'] = detrended
    df['trend'] = trend
    df = df.drop(columns=['prediction'])
    csv = df.to_csv(index=False)
    return StreamingResponse(io.StringIO(csv), media_type="text/csv")





