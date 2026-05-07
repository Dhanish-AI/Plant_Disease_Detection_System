from flask_login import LoginManager, UserMixin, login_required, login_user, logout_user
from functools import wraps
from flask import redirect, url_for, flash
from models import User

login_manager = LoginManager()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id)) 