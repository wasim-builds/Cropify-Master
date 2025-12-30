from flask_mail import Mail
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from flask_babel import Babel

mail = Mail()
db = SQLAlchemy()
bcrypt = Bcrypt()
babel = Babel()
