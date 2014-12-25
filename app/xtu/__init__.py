from flask import Blueprint

xtu = Blueprint("xtu", __name__)

from . import views, errors
# from .models import Permission


# @xtu.app_context_processor
# def inject_permissions():
#     return dict(Permission=Permission)