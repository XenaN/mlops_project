import os

import joblib
import numpy
import pandas
import uvicorn
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

with open("model.clf", "rb") as f:
    model = joblib.load(f)
with open("dataset.csv") as f:
    df = pandas.read_csv(f)
aqi_fact = df["AQI"].tolist()
df = df.drop(columns=["AQI"])

labels = numpy.arange(1, df.shape[0]).tolist()
data = model.predict(df).tolist()

fact = {
    "data": aqi_fact,
    "label": "AQI Index Fact",
    "borderColor": "#fc5286",
    "fill": False,
}

predicted = {
    "data": data,
    "label": "AQI Index predict",
    "borderColor": "#0e4cfd",
    "fill": False,
}

full_data = {
    "labels": labels,
    "datasets": [predicted, fact],
}


templates = Jinja2Templates(directory="templates")


@app.get("/")
async def read_item(request: Request):
    return templates.TemplateResponse(
        "index.html", {"request": request, "data": full_data}
    )


if __name__ == "__main__":
    uvicorn.run(app,
                host=os.getenv('SERVICE_HOST', '0.0.0.0'),
                port=int(os.getenv('SERVICE_PORT', 8000)),
                workers=int(os.getenv('SERVICE_WORKERS', '1')))
