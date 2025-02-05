from django.contrib import admin
from django.urls import path
from categories.views import Categories , Create_categories,update_categories
urlpatterns = [
    path('admin/' , admin.site.urls),
    path('' , Categories,name="Categories" ),
    path('create-categories/' , Create_categories , name="create_categories"),
    path('update_categories/' , update_categories , name='update_categories'),
]