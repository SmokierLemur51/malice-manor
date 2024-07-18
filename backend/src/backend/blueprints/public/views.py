import os

from flask import Blueprint, redirect, render_template, url_for, request, current_app

from ...models.models import db
# from ...models import 

# from .forms import 


public = Blueprint('public', __name__, template_folder="templates/public", url_prefix="/")


@public.route("/")
def index():
    elements = {
        "title": "Welcome",
        "market_name": os.environ["MARKET_NAME"],
    }
    return render_template("index.html", elements=elements)



@public.route("/create-account")
def create_account():
    elements={
            "title": "Create Account",
            "market_name": os.environ["MARKET_NAME"],
        }
    return render_template("create_account.html", elements=elements)


@public.route("/login")
def login():
    elements={
            "title": "Login",
            "market_name": os.environ["MARKET_NAME"],
        }
    return render_template("login.html", elements=elements)


@public.route("/register-customer", methods=["GET", "POST"])
def register_customer():
    return render_template("register_customer.html")


@public.route("/register-vendor", methods=["GET", "POST"])
def register_vendor():
    #form = RegisterVendorForm()
    return render_template("register_vendor.html")


