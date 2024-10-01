from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from model.spell_number import spell_number
from fastapi.staticfiles import StaticFiles
from cam.gphoto2 import take_picture

app = FastAPI()
templates = Jinja2Templates(directory="templates/")

app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/")
def read_form(request: Request):
    return templates.TemplateResponse("home.html", {"request": request, "result": None})


@app.get("/takephoto")
def takephoto(request: Request):
    result = take_picture()
    return {"message": result}


@app.post("/scan")
def scan(request: Request):
    return {"message": "Scanning"}


@app.get("/form")
def form_get(request: Request):
    result = "Type a number"
    return templates.TemplateResponse(
        "form.html", context={"request": request, "result": result}
    )


@app.post("/form")
def form_post(request: Request, num: int = Form(...)):
    result = spell_number(num)
    return templates.TemplateResponse(
        "form.html", context={"request": request, "result": result}
    )
