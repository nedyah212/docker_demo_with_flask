from . import db, bcrypt
from .forms import RegistrationForm
from .services import DatabaseServices
from .models import User

class Controller():

    def home():
        form = RegistrationForm()
        posted = False

        if form.validate_on_submit():
            hashed_pw = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
            user = User(username=form.username.data, email=form.email.data, password=hashed_pw)
            posted = DatabaseServices.add_user(user)

        users = DatabaseServices.get_all_users()

        return users, posted, form

    def delete_user(user_id):
        DatabaseServices.delete_user_by_id(user_id)