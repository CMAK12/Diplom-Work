from django.shortcuts import render, get_object_or_404
from .models import Product, Category

def home(request, category_slug=None):
	category_page = None
	products = None
	if category_slug != None:
		category_page = get_object_or_404(Category, slug=category_slug)
		products = Product.objects.filter(category=category_page, available=True)
	else:
		products = Product.objects.all().filter(available=True)
	return render(request, 'home.html', {'category':category_page, 'products': products})

def product(request, category_slug, product_slug):
	try:
		product = Product.objects.get(category__slug=category_slug, slug=product_slug)
	except Exception as e:
		raise e
	return render(request, 'product.html', {'product': product})

def search(request):
	search_query = request.GET['q']

	if search_query == None:
		searching = Product.objects.all().filter(available=True).order_by('price')
		return render(request, 'search.html', {'searches':searching})
	else:
		searching = Product.objects.filter(
            name__contains=search_query,
			available=True
        ).order_by('price')
		return render(request, 'search.html', {'searches':searching})
