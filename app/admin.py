from sqladmin import ModelAdmin

from app.models import Category, Post, User


class CategoryAdmin(ModelAdmin, model=Category):
    form_columns = [Category.title, Category.slug]
    form_include_pk = True


class PostAdmin(ModelAdmin, model=Post):
    form_columns = [Post.title, Post.slug, Post.text, Post.category, Post.author]


class UserAdmin(ModelAdmin, model=User):
    form_columns = [User.email, User.name, User.password, User.is_active]