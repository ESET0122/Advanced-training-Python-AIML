from typing import Union
 
from fastapi import FastAPI
 
from pydantic import BaseModel
import joblib
from sklearn.datasets import load_iris
import pandas as pd
import numpy as np
 
app = FastAPI()
 
model = joblib.load('iris_model.pkl')
 
class IrisInput(BaseModel):
    sepal_length: float
    sepal_width: float
    petal_length: float
    petal_width: float
 
class IrisPrediction(BaseModel):
    predicted_class: int
    predicted_class_name: str
 
@app.get("/")
def read_root():
    return {"Hello": "World"}
 
@app.post("/predict/",response_model=IrisPrediction)
def predict(data:IrisInput):
   
    ## Prepare input data
    InputData = pd.DataFrame([[data.sepal_length, data.sepal_width, data.petal_length, data.petal_width]],
                             columns=['sepal length (cm)', 'sepal width (cm)', 'petal length (cm)', 'petal width (cm)'])
   
    ## Model Prediction
    predict_class = model.predict(InputData)[0]
    predict_class_name = load_iris().target_names[predict_class]
    return IrisPrediction(predicted_class=predict_class, predicted_class_name=predict_class_name)
 
 
 
 
 
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8088)
 