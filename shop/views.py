from django.http import HttpResponse
from django.shortcuts import render
from .models import Product

# My wonderful views go here~

def product_list_view(request):
    #Using the Product model, we can retrieve all products from the database and display them
    products = Product.objects.filter(is_active=True)  # Filter only active products

    # Create a simple HTML response to display the products
    html = "<h1>Active Products</h1>"
    html += "<ul>"
    for p in products:
        html += f"<li>{p.name} - ${p.price}</li>"
    html += "</ul>"

    return HttpResponse(html)

    #Pass data into the template
    #Fetch all active products from the database using ORM
    active_products = Product.objects.filter(is_active=True)

    #Package the data into a context dictionary to pass to the template
    context = {
        'products': active_products
    }

    #Render the template with the context data
    return render(request, 'product_list.html', context)