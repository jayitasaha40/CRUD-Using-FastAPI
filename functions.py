# Base URL of the FastAPI backend
import requests
from PIL import Image
import io
import streamlit as st

base_url = "http://localhost:8000"

# Function to add a new student
def add_student(name, gender, branch, year, uploaded_file):
    data = {"name": name, "gender": gender, "branch": branch, "year": year}
    files = {"image": uploaded_file.getvalue()} if uploaded_file else None
    response = requests.post(f"{base_url}/students/", data=data, files=files)
    return response

# Function to get student details
def get_student_details(student_id):
    response = requests.get(f"{base_url}/students/{student_id}")
    return response

# Function to update student details
def update_student(student_id, branch, uploaded_file):
    data = {"branch": branch}
    files = {"image": uploaded_file.getvalue()} if uploaded_file else None
    response = requests.put(f"{base_url}/students/{student_id}", data=data, files=files)
    return response

# Function to delete a student
def delete_student(student_id):
    response = requests.delete(f"{base_url}/studentdelete/{student_id}")
    return response

# Function to get list of all students
def get_student_list():
    response = requests.get(f"{base_url}/studentlist/")
    return response.json() if response.status_code == 200 else None

# Function to display student image
def display_student_image(student_id):
    image_response = requests.get(f"{base_url}/students/{student_id}/image")
    return image_response