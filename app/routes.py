from flask import (
    Flask,
    render_template,
    request as flask_request
)
import requests


app = Flask(__name__)

BACKEND_URL = "http://127.0.0.1:5000/tasks"

@app.get("/")
def home():
    return render_template("index.html")

@app.get("/about")
def about():
    return render_template("about.html")

@app.get("/tasks")
def task_list():
    response = requests.get(BACKEND_URL)
    if response.status_code == 200:
        task_data = response.json().get("tasks")
        return render_template("list.html", tasks=task_data)
    return (
        render_template("error.html", error=response.status_code),
        response.status_code
    )

@app.get("/tasks/<int:pk>/edit")
def edit_form(pk):
    url = "%s/%s" % (BACKEND_URL, pk)
    response = requests.get(url)
    if response.status_code == 200:
        single_task = response.json().get("task")
        return render_template("edit.html", task=single_task)
    return (
        render_template("error.html", error=response.status_code),
        response.status_code
    )

@app.post("/tasks/<int:pk>/edit")
def edit_task(pk):
    url = "%s/%s" % (BACKEND_URL, pk)
    response = requests.put(url, json=flask_request.form)
    if response.status_code == 204:
        return render_template("success.html", message="Task edited")
    return (
        render_template("error.html", error=response.status_code),
        response.status_code
    )

@app.delete("/tasks/<int:pk>")
def delete_task(pk):
    url = f"{BACKEND_URL}/{pk}"
    response = requests.delete(url)
    if response.status_code == 204:
        return render_template("success.html", message="Task deleted successfully!")
    return (
        render_template("error.html", error=response.status_code),
        response.status_code
    )

# @app.post("/tasks")
# def create_task():
#     task_data = requests.jsontask.create_task(task_data)
#     return "", 204

@app.post("/tasks/create")
def create_task():
    task_data = flask_request.form 
    response = requests.post(BACKEND_URL, json=task_data)
    if response.status_code == 204:
        return render_template("success.html", message="Task created successfully!")
    return (
        render_template("error.html", error=response.status_code),
        response.status_code
    )

    
    # assignment is to have full crud support 2/5/25