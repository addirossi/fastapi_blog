import sqlalchemy as sa
from sqlalchemy.orm import relationship

from .database import Base


class User(Base):
    id = sa.Column(sa.Integer, primary_key=True)
    email = sa.Column(sa.String(50), unique=True, index=True)
    name = sa.Column(sa.String(30))
    password = sa.Column(sa.String())
    is_active = sa.Column(sa.Boolean, default=False)
    posts = relationship("Post", back_populates="author")

    __tablename__ = 'users'

    def __str__(self):
        return self.email

    def __repr__(self):
        return self.email


class Category(Base):
    title = sa.Column(sa.String(50), unique=True)
    slug = sa.Column(sa.String(50), primary_key=True)
    posts = relationship("Post", back_populates="category")

    __tablename__ = 'categories'

    def __str__(self):
        return self.title

    def __repr__(self):
        return self.title


class Tag(Base):
    title = sa.Column(sa.String(50), unique=True)
    slug = sa.Column(sa.String(50), primary_key=True)

    __tablename__ = 'tags'

    def __str__(self):
        return self.title

    def __repr__(self):
        return self.title


class Post(Base):
    id = sa.Column(sa.Integer, primary_key=True)
    title = sa.Column(sa.String(100), unique=True)
    slug = sa.Column(sa.String(100), unique=True, index=True)
    text = sa.Column(sa.Text())
    category_id = sa.Column(sa.String(50),
                            sa.ForeignKey("categories.slug"))
    category = relationship("Category", back_populates="posts")
    author_id = sa.Column(sa.Integer,
                          sa.ForeignKey("users.id"))
    author = relationship("User", back_populates="posts")
    created_at = sa.Column(sa.DateTime,
                           default=sa.sql.func.now())

    __tablename__ = 'posts'

    def __str__(self):
        return self.title

    def __repr__(self):
        return self.title






