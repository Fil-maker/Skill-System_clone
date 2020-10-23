from flask import render_template, g, session
from werkzeug.utils import redirect
from app import app
from app.forms.editProfile import EditProfileForm
from app.forms.eventDates import EditEventDatesForm
from app.forms.eventInformation import EditEventInformationForm
from app.forms.eventRegister import EventRegisterForm
from app.forms.login import LoginForm
from app.forms.participant import ParticipantForm
from app.forms.password import PasswordForm
from app.forms.pin import PinForm
from app.forms.register import RegisterForm
from app.services.events import create_event_from_form, edit_event_information_from_form, \
    load_event_to_g_or_abort
from app.services.users import confirm_token, register_from_form, redirect_if_authorized, \
    login_from_form, logout, redirect_if_unauthorized, change_password_from_form, get_myself, \
    set_pin_from_form, edit_profile_from_form, reset_pin, only_for_admin


@app.before_request
def before_request():
    if session.get("token", None):
        current_user = get_myself()
        if current_user is None:
            session.pop("token", None)
            return redirect("/")
        g.current_user = current_user


@app.route("/confirm/<token>")
def confirm(token):
    return "ok" if confirm_token(token) else "not ok"


@app.route("/register", methods=["GET", "POST"])
@redirect_if_authorized
def register():
    form = RegisterForm()
    if register_from_form(form):
        return redirect("/profile")
    return render_template("register.html", form=form)


@app.route("/login", methods=["GET", "POST"])
@redirect_if_authorized
def login():
    form = LoginForm()
    if login_from_form(form):
        return redirect("/profile")
    return render_template("login.html", form=form)


@app.route("/logout")
@redirect_if_unauthorized
def logout_():
    logout()
    return redirect("/login")


@app.route("/pin", methods=["GET", "POST"])
@redirect_if_unauthorized
def pin():
    if g.current_user["is_pin_set"]:
        reset_pin()
    form = PinForm()
    if set_pin_from_form(form):
        return redirect("/profile")
    return render_template("pin.html", form=form)


@app.route("/change-password", methods=["GET", "POST"])
@redirect_if_unauthorized
def change_password_():
    form = PasswordForm()
    if change_password_from_form(form):
        return redirect("/profile")
    return render_template("password.html", form=form)


@app.route("/edit-profile", methods=["GET", "POST"])
@redirect_if_unauthorized
def edit_profile_():
    form = EditProfileForm(first_name=g.current_user["first_name"],
                           last_name=g.current_user["last_name"],
                           country=g.current_user["country"]["id"],
                           about=g.current_user["about"])
    if g.current_user["region"] is not None:
        form.region.process_data(g.current_user["region"]["id"])
    if edit_profile_from_form(form):
        return redirect("/profile")
    return render_template("editProfile.html", form=form, current_user=g.current_user)


@app.route("/profile", methods=["GET", "POST"])
@redirect_if_unauthorized
def profile():
    return render_template("selfProfile.html", current_user=g.current_user)


# TODO: Получить данные
@app.route("/user/<int:user_id>")
@redirect_if_unauthorized
def user_profile(user_id):
    user = []
    return render_template('userProfile.html', user=user)


@app.route("/create-event", methods=["GET", "POST"])
@redirect_if_unauthorized
@only_for_admin
def create_event_():
    form = EventRegisterForm()
    if create_event_from_form(form):
        return redirect("/events")
    return render_template("eventRegister.html", form=form)


# TODO: Получить данные
@app.route("/event/<int:event_id>")
@redirect_if_unauthorized
def event_profile(event_id):
    event = []
    return render_template('eventProfile.html', event=event)


# TODO: Получить данные
@app.route("/event-list")
@redirect_if_unauthorized
@only_for_admin
def event_list():
    events = []
    return render_template('eventList.html', events=events)


@app.route("/event/<int:event_id>/information", methods=["GET", "POST"])
@load_event_to_g_or_abort
@redirect_if_unauthorized
@only_for_admin
def edit_event_information_(event_id):
    form = EditEventInformationForm(title=g.current_event["title"])
    if edit_event_information_from_form(event_id, form):
        return redirect(f"/event/{event_id}/information")
    return render_template("eventInformation.html", form=form)


# TODO: Получить данные
@app.route("/event/<int:event_id>/participants")
@redirect_if_unauthorized
@only_for_admin
def participants_manage(event_id):
    form = ParticipantForm()
    users = []
    return render_template('participantsManage.html', form=form, users=users)

# @app.route("/event/<int:event_id>/dates", methods=["GET", "POST"])
# @load_event_to_g_or_abort
# @redirect_if_unauthorized
# @only_for_admin
# def edit_event_dates_(event_id):
#     form = EditEventDatesForm(start_date=g.current_event["start_date"],
#                               main_stage_date=g.current_event["main_stage_date"],
#                               final_stage_date=g.current_event["final_stage_date"],
#                               finish_date=g.current_event["finish_date"])
#     if edit_event_information_from_form(event_id, form):
#         return redirect(f"/event/{event_id}/dates")
#     return render_template("eventDates.html", form=form)
# # TODO: создать шаблон eventDates.html и просто раскомментировать этот кусок
