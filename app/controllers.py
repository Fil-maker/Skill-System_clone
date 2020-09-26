from flask import render_template

from app import app
from app.forms.register import RegisterForm


@app.route("/")
def test():
    form = RegisterForm()
    return render_template('register.html', form=form)
