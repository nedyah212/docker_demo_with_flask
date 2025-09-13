from .models import User
from . import db, bcrypt
from .forms import RegistrationForm


class Controller():
    
    def home():
        form = RegistrationForm()
        posted = False
        users = User.query.all()

        if form.validate_on_submit():    
            hashed_pw = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
            user = User(username=form.username.data, email=form.email.data, password=hashed_pw)
                
            db.session.add(user)
            db.session.commit()
            posted=True         

        users = User.query.all()
        
        return users, posted, form
    
    def delete_user(user_id):
        user = User.query.get(user_id)
        
        if user:
            db.session.delete(user)
            db.session.commit()