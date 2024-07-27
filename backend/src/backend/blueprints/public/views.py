import os

from quart import Blueprint, redirect, render_template, url_for, request, current_app

public = Blueprint('public', __name__, template_folder="templates/public", url_prefix="/")


@public.route("/")
async def index():
    elements = {
        "title": "Welcome",
        "market_name": os.environ["MARKET_NAME"],
    }
    return await render_template("index.html", elements=elements)



@public.route("/create-account")
async def create_account():
    elements={
            "title": "Create Account",
            "market_name": os.environ["MARKET_NAME"],
        }
    return await render_template("create_account.html", elements=elements)


@public.route("/login")
async def login():
    elements={
            "title": "Login",
            "market_name": os.environ["MARKET_NAME"],
        }
    return await render_template("login.html", elements=elements)


@public.route("/register-customer", methods=["GET", "POST"])
async def register_customer():
    return await render_template("register_customer.html")


@public.route("/register-vendor", methods=["GET", "POST"])
async def register_vendor():
    #form = RegisterVendorForm()
    return await render_template("register_vendor.html")


