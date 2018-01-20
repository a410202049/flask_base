from flask import Blueprint

home = Blueprint('home', __name__)

from app.controller.home import views

