from flask import Blueprint

auth = blueprint("auth", __name__)

from . import views