
from django.urls import path
from categories.views import category_list , Create_categories,update_categories ,delete_Category
urlpatterns = [
    path('' , category_list,name="Categories" ),
    path('create-categories/' , Create_categories , name="create_category"),
    path('update_categories/<int:id>/' , update_categories , name='update_categories'),
    path('delete_categories/<int:id>/' , delete_Category , name='delete_Category'),
]