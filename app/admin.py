from sqladmin import ModelAdmin

from app.models import Category, Post


class CategoryAdmin(ModelAdmin, model=Category):
    form_columns = [Category.title, Category.slug]
    form_include_pk = True


class PostAdmin(ModelAdmin, model=Post):
    pass