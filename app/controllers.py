import datetime
from flask import render_template, g, session, send_file
from werkzeug.exceptions import abort
from werkzeug.utils import redirect

from app.services.forms import get_form, create_form_from_form, update_form_from_form, sign_form_from_form
from app import app
from app.forms.profile import EditProfileForm
from app.forms.eventDates import EditEventDatesForm
from app.forms.eventInformation import EditEventInformationForm
from app.forms.eventRegister import EventRegisterForm
from app.forms.formSign import FormSignForm
from app.forms.formRegister import FormRegisterForm
from app.forms.login import LoginForm
from app.forms.password import PasswordForm
from app.forms.pin import PinForm
from app.forms.register import RegisterForm
from app.services.events import create_event_from_form, edit_event_information_from_form, \
    load_event_to_g_or_abort, get_event, get_event_participants, get_event_forms, get_event_form, download_event_form
from app.services.users import confirm_token, register_from_form, redirect_if_authorized, \
    login_from_form, logout, redirect_if_unauthorized, change_password_from_form, get_myself, \
    set_pin_from_form, edit_profile_from_form, reset_pin, only_for_admin, get_user, only_for_admin_and_chief_expert, \
    get_events, get_forms, get_events_to_assign


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


@app.route("/")
def meet_page():
    if get_myself() is not None:
        events = get_events(g.current_user['id'])
        forms = get_forms(g.current_user['id'])
        return render_template("dashboard.html", events=events, forms=forms)
    return render_template("main.html")


@app.route("/register", methods=["GET", "POST"])
@redirect_if_authorized
def register():
    form = RegisterForm()
    if register_from_form(form):
        return redirect("/profile")
    return render_template("profileRegister.html", form=form)


@app.route("/login", methods=["GET", "POST"])
@redirect_if_authorized
def login():
    form = LoginForm()
    if login_from_form(form):
        return redirect("/profile")
    return render_template("profileLogin.html", form=form)


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
    return render_template("profilePin.html", form=form)


@app.route("/profile/password", methods=["GET", "POST"])
@redirect_if_unauthorized
def change_password_():
    form = PasswordForm()
    if change_password_from_form(form):
        return redirect("/profile")
    return render_template("profilePassword.html", form=form)


@app.route("/profile/edit", methods=["GET", "POST"])
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
    return render_template("profileEdit.html", form=form)


@app.route("/profile", methods=["GET", "POST"])
@redirect_if_unauthorized
def profile():
    return render_template("profileSelf.html")


@app.route("/user/<int:user_id>")
@redirect_if_unauthorized
def user_profile(user_id):
    user = get_user(user_id)
    if user is None:
        abort(404)
    return render_template("profileUser.html", user=user)


@app.route("/profile/events")
@redirect_if_unauthorized
def self_events_to_assign():
    user_events = get_events_to_assign(g.current_user["id"])
    return render_template("profileEvents.html", user=g.current_user, events=user_events)


@app.route("/user/<int:user_id>/events")
@redirect_if_unauthorized
def user_events_to_assign(user_id):
    user = get_user(user_id)
    user_events = get_events_to_assign(user_id)
    if user is None:
        abort(404)
    return render_template("profileEvents.html", user=user, events=user_events)


@app.route("/user/list")
@redirect_if_unauthorized
@only_for_admin
def user_list():
    users = get_user()
    return render_template("profileList.html", users=users)


@app.route("/event/create", methods=["GET", "POST"])
@redirect_if_unauthorized
@only_for_admin
def create_event():
    form = EventRegisterForm()
    if create_event_from_form(form):
        return redirect("/event/list")
    return render_template("eventRegister.html", form=form)


@app.route("/event/<int:event_id>")
@redirect_if_unauthorized
def event_profile(event_id):
    event = get_event(event_id)
    if event is None:
        abort(404)
    return render_template("eventProfile.html", event=event)


@app.route("/event/list")
@redirect_if_unauthorized
@only_for_admin
def event_list():
    events = get_event()
    return render_template("eventList.html", events=events)


@app.route("/event/<int:event_id>/information", methods=["GET", "POST"])
@load_event_to_g_or_abort
@redirect_if_unauthorized
@only_for_admin_and_chief_expert
def edit_event_information_(event_id):
    form = EditEventInformationForm(title=g.current_event["title"])
    if edit_event_information_from_form(event_id, form):
        return redirect(f"/event/{event_id}")
    return render_template("eventInformation.html", form=form)


@app.route("/event/<int:event_id>/participants")
@load_event_to_g_or_abort
@redirect_if_unauthorized
@only_for_admin_and_chief_expert
def event_participants(event_id):
    participants = get_event_participants(event_id)
    return render_template("eventParticipants.html", participants=participants, event=g.current_event)


@app.route("/event/<int:event_id>/dates", methods=["GET", "POST"])
@load_event_to_g_or_abort
@redirect_if_unauthorized
@only_for_admin_and_chief_expert
def edit_event_dates_(event_id):
    st = datetime.datetime.strptime(g.current_event["dates"]["C-N"]["date"], '%Y-%m-%d')
    ms = datetime.datetime.strptime(g.current_event["dates"]["C1"], '%Y-%m-%d')
    fs = datetime.datetime.strptime(g.current_event["dates"]["C+1"], '%Y-%m-%d')
    fd = datetime.datetime.strptime(g.current_event["dates"]["C+N"]["date"], '%Y-%m-%d')
    form = EditEventDatesForm(start_date=st,
                              main_stage_date=ms,
                              final_stage_date=fs,
                              finish_date=fd)
    if edit_event_information_from_form(event_id, form):
        return redirect(f"/event/{event_id}")
    return render_template("eventDates.html", form=form, event=g.current_event)


@app.route("/event/<int:event_id>/forms")
@load_event_to_g_or_abort
@redirect_if_unauthorized
def event_forms(event_id):
    forms = get_event_forms(event_id)
    return render_template("formList.html", forms=forms, event=g.current_event)


@app.route("/form/create", methods=["GET", "POST"])
@redirect_if_unauthorized
@only_for_admin
def create_form():
    form = FormRegisterForm()
    if create_form_from_form(form):
        return redirect("/form/list")
    return render_template("formRegister.html", form=form)


@app.route("/form/<int:form_id>")
@redirect_if_unauthorized
def profile_form(form_id):
    form = get_form(form_id)
    return render_template("formProfile.html", form=form)


@app.route("/event/<int:event_id>/form/<int:form_id>")
@redirect_if_unauthorized
@load_event_to_g_or_abort
def event_form(event_id, form_id):
    form_of_event = get_event_form(event_id, form_id)
    return render_template("formEventProfile.html", eventForm=form_of_event)


@app.route("/event/<int:event_id>/form/<int:form_id>/download")
@redirect_if_unauthorized
@load_event_to_g_or_abort
def download_event_form_(event_id, form_id):
    file = download_event_form(event_id, form_id)
    if file is not None:
        return send_file(file, as_attachment=True, attachment_filename="form.docx")
    abort(400)


@app.route("/form/list")
@redirect_if_unauthorized
@only_for_admin
def list_form():
    forms = get_form()
    return render_template("formList.html", forms=forms)


@app.route("/event/<int:event_id>/form/<int:form_id>/sign", methods=["GET", "POST"])
@redirect_if_unauthorized
def sign_form(event_id, form_id):
    form_data = get_event_form(event_id, form_id)
    if datetime.datetime.now() >= datetime.datetime.strptime(form_data['date'], "%Y-%m-%d")\
            and g.current_user['id'] in form_data['must_sign']:
        form = FormSignForm()
        if sign_form_from_form(event_id, form_id, form):
            return redirect(f"/event/{event_id}/form/{form_id}")
        return render_template("formSign.html", form=form, doc=form_data)
    return redirect('/')


@app.route("/form/<int:form_id>/edit", methods=["GET", "POST"])
@redirect_if_unauthorized
def edit_form(form_id):
    form_data = get_form(form_id)
    form = FormRegisterForm(title=form_data["title"],
                            day=form_data["day"],
                            content=form_data["content"],
                            role=form_data["role"]
                            )
    if update_form_from_form(form_id, form):
        return redirect(f"/form/{form_id}")
    return render_template("formRegister.html", form=form, form_data=form_data, edit=True)
