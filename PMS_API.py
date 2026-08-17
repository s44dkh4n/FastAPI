from fastapi import FastAPI,HTTPException,Path,Query
import json

def load_data():
    with open(r"D:\Course\GenAI-Code\FastAPI\patients.json","r") as f:
        data = json.load(f)

    return data

app = FastAPI()

@app.get("/")
def hello():
    return {"message":"Patient Managment System"}

# End Point to view info about APP 
@app.get("/about")
def about():
    return {"message":"Fully Functional Patient Managment System API"}

# End Point to view info of ALL patients 
@app.get("/view")
def view_patients_record():
    data = load_data()
    return data

# End Point to view info of a individual patient using their ID
@app.get("/view/{patient_id}")
def view_patient(patient_id: str = Path(..., description="Patient ID for Pateint info you want", examples= ["1","2","3"])):

    data = load_data()
    if patient_id in data.keys():
        return data[patient_id]
    raise HTTPException(status_code=404, detail="Patient not Found")

@app.get("/sorted_patients")
def sorted_patients(
    sort_by: str = Query(description="Sort by feature: weight, height, or bmi"),
    order: str = Query("asc", description="Sort order: asc or desc")
):
    # Convert inputs to lowercase to match JSON keys
    sort_key = sort_by.strip().lower()
    order_normalized = order.strip().lower()

    valid_fields = ["weight", "height", "bmi"]
    valid_orders = ["asc", "desc"]

    if sort_key not in valid_fields:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid field '{sort_by}'. Select from {valid_fields}"
        )

    if order_normalized not in valid_orders:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid order '{order}'. Select from {valid_orders}"
        )

    data = load_data()
    reverse = order_normalized == "desc"

    # Direct key lookup on lowercase JSON fields
    sorted_data = sorted(
        data.values(),
        key=lambda x: x.get(sort_key, 0),
        reverse=reverse
    )

    return sorted_data