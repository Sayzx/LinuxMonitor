from app import app
from flask_login import LoginManager, UserMixin
login_manager = LoginManager()
login_manager.init_app(app)

class User(UserMixin):
    def __init__(self, id):
        self.id = id

@login_manager.user_loader
def load_user(user_id):
    return User(user_id)

if __name__ == '__main__':
    app.run(debug=True)
