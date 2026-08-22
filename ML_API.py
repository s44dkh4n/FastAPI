from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from schema.userinput import UserInfo
from model.predict import predict_output, model, MODEL_VERSION

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Hello to Insurance Plan Prediction Website"}

@app.get("/health")
def health_check():
    return {
            "status": "OK",
            "Model Version": MODEL_VERSION,
            "model loaded": model is not None
        }

@app.post("/predict")
def predict_premium(data: UserInfo):
    user_input = {
        "age_group": data.age_group,
        "bmi": data.bmi,
        "city_tier": data.city_tier,
        "lifestyle_risk": data.lifestyle_risk,
        "occupation": data.occupation,
        "income_lpa": data.income
    }
    try:
        prediction = predict_output(user_input)
    
        return JSONResponse(
            status_code=200, 
            content={
                "response": {
                    "predicted_category": prediction,
                }
            }
        )
    except Exception as e:
        return JSONResponse(status_code=500, content= str(e))