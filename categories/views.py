from django.shortcuts import render , redirect
from django.contrib import messages
from categories.forms import CategoriesForm
from categories.models import Categories
from django.contrib.auth import get_user_model


User = get_user_model()

# Create your views here.

def category_list(request):
    return render(request , 'categories/categories.html' )


def Create_categories(request):
    add_categories_form = CategoriesForm()
    if request.method == "POST":
        add_categories_form = CategoriesForm(request.POST)
        if add_categories_form.is_valid():
            add_categories_form.save()

            messages.success(request , "Categories created successfully !")
            return redirect('Organizer_Dashboard')
        else:
            messages.error(request , 'Something Went Wrong !')
            return redirect('Organizer_Dashboard')
    context = {  'add_categories':add_categories_form}
    return render(request , 'categories/create_categories.html' , context)


def update_categories(request , id):
    categories = Categories.objects.get(id=id)
    update_category_form = CategoriesForm(instance = categories)

    if request.method == "POST":
        update_category_form = CategoriesForm(request.POST, instance=categories)
        
        if update_category_form.is_valid() :
            update_category_form.save()
            messages.success(request, "Categories Update successfully !")
            return redirect('Organizer_Dashboard') 
    
    context = {'update_category_form':update_category_form}
    
    return render(request , 'categories/update_categories.html' , context)

def delete_Category(request , id):
    if request.method == "POST":
        category = Categories.objects.get(id=id)
        category.delete()

        messages.success(request , "Category Deleted successfully !")
        return redirect('Organizer_Dashboard')
    else:
        messages.error(request, "Something Went Wrong !")
        return redirect('Organizer_Dashboard')

