from fastapi import FastAPI, HTTPException, Path, Query
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, computed_field
from typing import Annotated, Literal
import json


app =FastAPI()

class Patient(BaseModel):

    id: Annotated[str,Field(..., description = 'ID of the Patient', examples= ['P001','PXXX'])]
    name: Annotated[str, Field(..., description = 'Name of the Patient' )]
    city: Annotated[str, Field(..., description = 'City where Patient is Living')]
    age: Annotated[int, Field(..., gt = 0, lt= 120, description = 'Age of the Patient')]
    gender: Annotated[Literal['male','female','others'], Field (..., description ='Gender of the Patient') ]
    height: Annotated[float, Field(..., gt = 0, description = 'Height of the Patient in Mtrs.')]
    weight: Annotated[float, Field(..., gt = 0, description = 'Weight of the patient in Kgs.')]

    @computed_field
    @property
    def bmi(self) -> float:
        bmi = (self.weight/(self.height**2),2)
        return bmi 
    
    @computed_field
    @property
    def verdict(self) -> str:
        
        if self.bmi <18.5:
            return 'Underweight'
        elif self.bmi <25:
            return 'Normal'
        elif self.bmi < 30:
            return 'Normal'
        else:
            return 'obese'


def load_data():
    with open('patients.json', 'r') as f:
        data = json.load(f)
    return data

def save_data(data):
    with open('Patients.json', 'w') as f:
        json.dump(data,f)


@app.get("/")

def hello():
    return {'message' : 'Patient Management System'} 


@app.get("/about")
def about():
    return {'message' : 'Fully functional API to manage patient records'}


@app.get('/view')
def view():
    data = load_data()

    return data 

@app.get('/patient/{patient_id}')
def view_patient(patient_id : str = Path(..., description = 'ID of the patient in DB', examples = 'PXXX')):  

#load all the patients

    data = load_data()

    if patient_id in data:
        return data[patient_id]
    raise HTTPException(status_code = 404, detail = 'Patient Not Found')

@app.get('/sort')

def sort_patients(sort_by : str = Query(..., description = 'Sort on the basis of height, weight, or BMI'), order: str = Query('asc', description = 'sort in asc or desc order')):

    valid_fields = ['height', 'weight', 'BMI']
    if sort_by not in valid_fields:
        raise HTTPException(status_code = 400, detail = f'Invaid field select from {valid_fields}')
    
    if order not in ['asc','desc',]:
        raise HTTPException (status_code = 400, detail = 'Invalid order select between ASC and DESC')
    
    data = load_data()

    sort_order = True if order == 'desc' else False 

    sorted_data = sorted(data.values(), key = lambda x:x.get(sort_by,0), reverse = sort_order)

    return sorted_data


@app.post('/create')
def create_patient(patient:Patient):

    # load existing data 

    data = load_data()
    
    # check if the patient already exist 

    if patient.id in data:
        raise HTTPException(status_code = 400, detail = 'Patient already exists')
    

    # add new patient to the DB

    data[patient.id]  = patient.model_dump(exclude =['id'])

    # save into the json file 

    save_data(data)

    return JSONResponse(status_code = 201, content = {'message':'Patient record created Successfully!'})






    
