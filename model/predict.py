import pickle
import pandas as pd

with open("model/model.pkl", "rb") as f:
    model = pickle.load(f)

MODEL_VERSION = "1.0.1"
classlabels = model.classes_.tolist()

def predict_output(user_input: dict):
    df = pd.DataFrame([user_input])
    
    output = model.predict(df)[0]
    probs = model.predict_proba(df)[0]
    confidence = max(probs)

    # Safely convert output to a standard Python value
    predicted_class = output.item() if hasattr(output, "item") else output

    prob_dict = {
        str(label): round(float(prob), 4) 
        for label, prob in zip(classlabels, probs)
    }

    return {
        "predicted_class": predicted_class,
        "class_probabilities": prob_dict,
        "confidence": round(float(confidence), 4)
    }