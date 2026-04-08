from fastapi import FastAPI, HTTPException, Path, Query
from pydantic import BaseModel
import json


app =FastAPI()

def load_data():
    with open('patients.json', 'r') as f:
        data = json.load(f)
    return data


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
def view_patient(patient_id : str = Path(..., description = 'ID of the patient in DB', example = 'PXXX')):  

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


