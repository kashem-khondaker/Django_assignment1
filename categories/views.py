from django.shortcuts import render , redirect
from django.contrib import messages
from categories.forms import CategoriesForm

# Create your views here.

def Categories(request):
    return render(request , 'categories/categories.html' )


def Create_categories(request):
    add_categories_form = CategoriesForm()
    if request.method == "POST":
        add_categories_form = CategoriesForm(request.POST)
        if add_categories_form.is_valid():
            add_categories_form.save()

            messages.success(request , "Categories created successfully !")
            return redirect('Categories')
        else:
            messages.error(request , 'Something Went Wrong !')
            return redirect('Categories')
    context = {  'add_categories':add_categories_form}
    return render(request , 'categories/create_categories.html' , context)