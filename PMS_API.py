from fastapi import FastAPI,HTTPException,Path,Query
from fastapi.responses import JSONResponse
from pydantic import BaseModel,Field,computed_field
from typing import Annotated,Literal,Optional
import json

def load_data():
    with open(r"D:\Course\GenAI-Code\FastAPI\patients.json","r") as f:
        data = json.load(f)

    return data

def save_data(data):
    with open(r"D:\Course\GenAI-Code\FastAPI\patients.json","w") as f:
        json.dump(data,f)

class Patient(BaseModel):
    id: Annotated[str, Field(..., description="ID of Patient", examples=["1","2","3"] )]
    name : Annotated[str, Field(..., description="Name of Patient", examples=["Saad Khan"])]
    age : Annotated[int, Field(..., description="Age og Patient",ge=1)]
    city : Annotated[str, Field(..., description="City to which Patient Belongs" , examples=["Risalpur"])]
    gender : Annotated[Literal["Male","Female"], Field(...,description="Gender of Patient")]
    height : Annotated[float, Field(..., description="Height of Patient in cm", ge=1)]
    weight : Annotated[float, Field(..., description="weight of Patient in kg", ge=1)]

    @computed_field
    @property

    def bmi (self) -> float:
        bmi = round(self.weight/((self.height / 100) **2),2 ) # round off bmi to 2 decimal digits
        return bmi

    @computed_field
    @property
    def verdict(self) -> str:
        if self.bmi < 18.5:
            return "underweight"
        elif self.bmi > 18.5 and self.bmi < 25.0:
            return "normal"
        elif self.bmi >= 25.0 and self.bmi < 30.0:
            return "overweight"
        elif self.bmi >= 30:
            return "obese"

class UpdatePatient(BaseModel):
    
    name : Annotated[Optional[str], Field(default=None)]
    age : Annotated[Optional[int], Field(default=None,ge=1)]
    city : Annotated[Optional[str], Field(default=None)]
    gender : Annotated[Optional[Literal["Male","Female"]], Field(default=None)]
    height : Annotated[Optional[float], Field(default=None, ge=1)]
    weight : Annotated[Optional[float], Field(default=None, ge=1)]

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

@app.post("/create_new_patient")
def create_patient(patient : Patient):

    data = load_data()

    if patient.id in data:
        raise HTTPException(status_code= 400, detail="Patient already exists")

    data[patient.id] = patient.model_dump(exclude=["id"])

    save_data(data)

    return JSONResponse(status_code=201, content={"message":"Patient created Successfully!"})

@app.put("/update_patient/{patient_id}")
def update_info(patient_id : str, update_patient : UpdatePatient):

    data = load_data()

    if patient_id not in data:
        raise HTTPException(status_code=400, detail="Patient not Found")

    exist_pat_data = data[patient_id]
    updated_pat_data = update_patient.model_dump(exclude_unset=True)
    
    for key, value in updated_pat_data.items():
        exist_pat_data[key] = value

    exist_pat_data["id"] = patient_id   
    pat_pydantic_obj = Patient(**exist_pat_data)

    updated_pat_data= pat_pydantic_obj.model_dump(exclude=["id"])
    data[patient_id] = updated_pat_data

    save_data(data=data)

    return JSONResponse(status_code= 200, content="Successfully Updated Patient Info")

@app.delete("/delete/patient_id")
def delete_patient(patient_id: str):
    data =load_data()

    if patient_id not in data:
        raise HTTPException(status_code=404, detail="Patient not Found")

    del data[patient_id]

    save_data(data= data)

    return JSONResponse(status_code=200, content={"message":"Operation done successfully"})