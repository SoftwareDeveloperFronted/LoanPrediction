from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
import pickle
import numpy as np

app = FastAPI()

# Templates folder
templates = Jinja2Templates(directory="templates")

# Load model
model = pickle.load(open('model.pkl', 'rb'))

# Dummy user store
users = {}

# Home
@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


# Predict
@app.get("/predict", response_class=HTMLResponse)
def predict_page(request: Request):
    return templates.TemplateResponse("prediction.html", {"request": request})


@app.post("/predict", response_class=HTMLResponse)
def predict(
    request: Request,
    gender: str = Form(...),
    married: str = Form(...),
    dependents: str = Form(...),
    education: str = Form(...),
    employed: str = Form(...),
    credit: float = Form(...),
    area: str = Form(...),
    loan: str = Form(...),
    ApplicantIncome: float = Form(...),
    CoapplicantIncome: float = Form(...),
    LoanAmount: float = Form(...),
    Loan_Amount_Term: float = Form(...)
):

    # Transformations
    male = 1 if gender == "Male" else 0
    married_yes = 1 if married == "Yes" else 0

    dependents_1 = dependents_2 = dependents_3 = 0
    if dependents == '1':
        dependents_1 = 1
    elif dependents == '2':
        dependents_2 = 1
    elif dependents == '3+':
        dependents_3 = 1

    not_graduate = 1 if education == "Not Graduate" else 0
    employed_yes = 1 if employed == "Yes" else 0

    semiurban = urban = 0
    if area == "Semiurban":
        semiurban = 1
    elif area == "Urban":
        urban = 1

    # Logs
    ApplicantIncomelog = np.log(ApplicantIncome)
    totalincomelog = np.log(ApplicantIncome + CoapplicantIncome)
    LoanAmountlog = np.log(LoanAmount)
    Loan_Amount_Termlog = np.log(Loan_Amount_Term)

    prediction = model.predict([[credit, ApplicantIncomelog, LoanAmountlog,
                                 Loan_Amount_Termlog, totalincomelog,
                                 male, married_yes, dependents_1,
                                 dependents_2, dependents_3,
                                 not_graduate, employed_yes,
                                 semiurban, urban]])

    prediction = "Yes" if prediction[0] != "N" else "No"

    return templates.TemplateResponse("prediction.html", {
        "request": request,
        "prediction_text": f"Loan status is {prediction}"
    })


# About
@app.get("/about", response_class=HTMLResponse)
def about(request: Request):
    return templates.TemplateResponse("aboutus.html", {"request": request})


# Features
@app.get("/features", response_class=HTMLResponse)
def features(request: Request):
    return templates.TemplateResponse("features.html", {"request": request})


# Check Eligibility
@app.get("/check_eligibility", response_class=HTMLResponse)
def check_eligibility_page(request: Request):
    return templates.TemplateResponse("check_eligibility.html", {"request": request})


@app.post("/check_eligibility", response_class=HTMLResponse)
def check_eligibility(
    request: Request,
    ApplicantIncome: float = Form(...),
    CoapplicantIncome: float = Form(...),
    employed: str = Form(...),
    credit: float = Form(...)
):

    if ApplicantIncome >= 25000 and CoapplicantIncome >= 25000 and employed == "Yes" and credit >= 600:
        result = "Congratulations! You are eligible for the loan."
    else:
        result = "Sorry, you do not meet the eligibility criteria."

    return templates.TemplateResponse("result.html", {
        "request": request,
        "result": result
    })


# Eligibility page
@app.get("/eligibility", response_class=HTMLResponse)
def eligibility(request: Request):
    return templates.TemplateResponse("eligibility.html", {"request": request})


# Blog
@app.get("/blog", response_class=HTMLResponse)
def blog(request: Request):
    return templates.TemplateResponse("blog.html", {"request": request})


# Contact
@app.get("/contact", response_class=HTMLResponse)
def contact_page(request: Request):
    return templates.TemplateResponse("contact.html", {"request": request})


@app.post("/contact")
def contact(
    request: Request,
    name: str = Form(...),
    number: str = Form(...),
    email: str = Form(...),
    message: str = Form(...)
):
    return RedirectResponse(url="/contact", status_code=303)


# Signin
@app.get("/signin", response_class=HTMLResponse)
def signin_page(request: Request):
    return templates.TemplateResponse("signin.html", {"request": request})


@app.post("/signin")
def signin(username: str = Form(...), password: str = Form(...)):
    if username in users:
        return RedirectResponse(url="/signin", status_code=303)

    users[username] = password
    return RedirectResponse(url="/login", status_code=303)


# Login
@app.get("/login", response_class=HTMLResponse)
def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@app.post("/login")
def login(username: str = Form(...), password: str = Form(...)):
    if users.get(username) == password:
        return HTMLResponse("Welcome to Loan Approval Dashboard!")
    return RedirectResponse(url="/login", status_code=303)


# Forgot Password
@app.get("/forgot", response_class=HTMLResponse)
def forgot_page(request: Request):
    return templates.TemplateResponse("forgot.html", {"request": request})


@app.post("/forgot")
def forgot(email: str = Form(...)):
    return RedirectResponse(url="/forgot", status_code=303)