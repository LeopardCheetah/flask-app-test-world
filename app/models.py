from typing import Optional
from datetime import datetime, timezone

from werkzeug.security import generate_password_hash, check_password_hash

# database shenanigans
import sqlalchemy as sa
import sqlalchemy.orm as so
from app import db

from flask_login import UserMixin
from app import login

from hashlib import md5




class User(UserMixin, db.Model):
    ########## CONSTS/USER Vars ######################
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    # seems like something x2 here happened here
    username: so.Mapped[str] = so.mapped_column(sa.String(16), index=True, unique=True)

    password_hash: so.Mapped[str] = so.mapped_column(sa.String(256))

    # 120 char description
    about_me: so.Mapped[Optional[str]] = so.mapped_column(sa.String(120))

    # not formally added in but this relationship does exist
    posts: so.WriteOnlyMapped['Post'] = so.relationship(back_populates='author')

    #----------------------------------
    #----------Methods-------------


    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User {}>'.format(self.username)
    
    def avatar(self, size):
        _salt = 'pair2025'
        digest = md5((self.username.lower() + _salt).encode('utf-8')).hexdigest()
        return f'https://www.gravatar.com/avatar/{digest}?d=identicon&s={size}'
    
    def set_description(self, description):
        # assume description <= 120 chars
        _d = description[:120]
        self.about_me = _d

    # end 
    



class Post(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    body: so.Mapped[str] = so.mapped_column(sa.String(1024))
    timestamp: so.Mapped[datetime] = so.mapped_column(index=True, default=lambda: datetime.now(timezone.utc))
    user_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(User.id), index=True)

    # add link back
    author: so.Mapped[User] = so.relationship(back_populates='posts')

    def __repr__(self):
        return '<Post {}>'.format(self.body)
    


@login.user_loader
def load_user(id):
    return db.session.get(User, int(id))