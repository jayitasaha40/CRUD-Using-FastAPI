import streamlit as st
import requests
from PIL import Image
import io
import pandas as pd


# Base URL of the FastAPI backend
base_url = "http://localhost:8000"
st.set_page_config(
    page_title="Student Management System",
    page_icon="👨‍🎓",
    layout="wide",
    initial_sidebar_state="collapsed",
   
)

st.title("Student Management System")


# CRUD operations
option = st.sidebar.selectbox("Choose an operation", ["Home","Add Student", "View Student", "Update Student", "Delete Student","View List"])
# st.sidebar.markdown(
#     """
#     <style>
#     .menu-button {
#         display: block;
#         width: 100%;
#         padding: 10px;
#         margin: 5px 0;
#         text-align: center;
#         background-color: #f0f0f0;
#         color: black;
#         border: none;
#         border-radius: 5px;
#         cursor: pointer;
#     }
#     .menu-button:hover {
#         background-color: #e0e0e0;
#     }
    
#     </style>
#     """, unsafe_allow_html=True
# )

# # Sidebar menu buttons
# option = "Home"

# if st.sidebar.button("🏠 Home", key="home"):
#     option = "Home"
# if st.sidebar.button("➕ Add Student", key="add_student"):
#     option = "Add Student"
# if st.sidebar.button("🔍 View Student", key="view_student"):
#     option = "View Student"
# if st.sidebar.button("✏️ Update Student", key="update_student"):
#     option = "Update Student"
# if st.sidebar.button("❌ Delete Student", key="delete_student",):
#     option = "Delete Student"
# if st.sidebar.button("📄 View List", key="view_list"):
#     option = "View List"


def display_student_image(student_id):
    image_response = requests.get(f"{base_url}/students/{student_id}/image")
    if image_response.status_code == 200:
        image = Image.open(io.BytesIO(image_response.content))
        st.image(image, caption="Student Image", use_column_width=True)
    else:
        st.warning("No image available for this student.")

if option == "Home":
    st.image("Images/FEATURESPAGE.gif")
        
if option == "Add Student":
    st.subheader("➕ Add a new student")
    st.image("Images/add.png",width=150)
    name = st.text_input("Name")
    gender = st.selectbox("Gender", ["Female", "Male", "Other"], index=0)
    year = st.number_input("year", min_value=1995,max_value=2028)
    branch = st.selectbox("Branch", ["CSE", "ECE", "EE","BME"], index=0)
    uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
    if st.button("Add"):
        if uploaded_file is not None:
            files = {"image": uploaded_file.getvalue()}
            data = {
                "name": name,
                "gender": gender,
                "branch": branch,
                "year": year
            }
            response = requests.post(f"{base_url}/students/", data=data, files={"image": uploaded_file})
            if response.status_code == 200:
                st.success("Student added successfully!")
            else:
                st.error(f"Failed to add student: {response.json().get('detail')}")
                
    

elif option == "View Student":
    st.subheader("🔍 View student details")
    student_id = st.number_input("Student ID", min_value=0)
    if st.button("View"):
        response = requests.get(f"{base_url}/students/{student_id}")
        if response.status_code == 200:
            student = response.json()
            st.write(f"ID: {student['id']}")
            st.write(f"Name: {student['name']}")
            st.write(f"Gender: {student['gender']}")
            st.write(f"Branch: {student['branch']}")
            st.write(f"Year: {student['year']}")
            image_response = requests.get(f"{base_url}/students/{student_id}/image")
            if image_response.status_code == 200:
                image = Image.open(io.BytesIO(image_response.content))
                st.image(image, caption="Student Image")
            else:
                st.warning("No image available for this student.")
        else:
            st.error(f"Student not found: {response.json().get('detail')}")

elif option == "Update Student":
    st.subheader("✏️ Update student details")
    student_id = st.number_input("Student ID", min_value=1, step=1)
    branch = st.selectbox("Branch", ["CSE", "ECE", "EE","BME"], index=0)
    uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

    if st.button("Update"):
        data = {"branch": branch}
        files = {"image": uploaded_file} if uploaded_file else None
        response = requests.put(f"{base_url}/students/{student_id}", data=data, files=files)
        if response.status_code == 200:
            st.success("Student updated successfully!")
        else:
            st.error(f"Failed to update student: {response.json().get('detail')}")


elif option == "Delete Student":
    st.subheader("❌ Delete a student")
    student_id = st.number_input("Student ID", min_value=1, step=1)
    if st.button("Delete"):
        response = requests.delete(f"{base_url}/studentdelete/{student_id}")
        if response.status_code == 200:
            st.success("Student deleted successfully!")
        else:
            st.error(f"Failed to delete student: {response.json().get('detail')}")

if option == "View List":
    st.subheader("📄 View list of all students")
    st.image("Images/list.png")
    response = requests.get(f"{base_url}/studentlist/")
    if response.status_code == 200:
        student_list = response.json()
        df = pd.DataFrame(student_list)
        df['year'] = df['year'].astype(str)

        # Add a column for image URLs, assuming your API provides them or you have a mapping function
        df['Image'] = df['id'].apply(lambda x: f"{base_url}/students/{x}/image")

        # Display the table with images using st.data_editor
        st.data_editor(
            df,
            column_config={
                "Image": st.column_config.ImageColumn(
                    "Student Image", help="Click to view student image"
                )
            },
            hide_index=True,
        )

    else:
        st.error(f"Failed to fetch student list: {response.json().get('detail')}")


