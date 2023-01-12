from django.shortcuts import render, get_object_or_404
from .models import Product, Category

def home(request, category_slug=None):
	sort_by = request.GET.get('sort')
	category_page = None
	products = None
	if category_slug != None:
			category_page = get_object_or_404(Category, slug=category_slug)
			if sort_by == 'expensive':
				products = Product.objects.filter(category=category_page, available=True).order_by('-price')
			elif sort_by == 'cheap':
				products = Product.objects.filter(category=category_page, available=True).order_by('price')
			else:
				products = Product.objects.filter(category=category_page, available=True).order_by('name')
	else:
		if sort_by == 'expensive':
			products = Product.objects.all().filter(available=True).order_by('-price')
		elif sort_by == 'cheap':
			products = Product.objects.all().filter(available=True).order_by('price')
		else:
			products = Product.objects.all().filter(available=True).order_by('name')
	return render(request, 'home.html', {'category':category_page, 'products': products})

def product(request, category_slug, product_slug):
	try:
		product = Product.objects.get(category__slug=category_slug, slug=product_slug)
	except Exception as e:
		raise e
	return render(request, 'product.html', {'product': product})

def search(request):
	search_query = request.GET['q']
	sort_by = request.GET.get('sort')

	if search_query == None:
		if sort_by == 'expensive':
			searching = Product.objects.all().filter(available=True).order_by('price')
		elif sort_by == 'cheap':
			searching = Product.objects.all().filter(available=True).order_by('-price')
		else:
			searching = Product.objects.all().filter(available=True).order_by('name')
	else:
		if sort_by == 'expensive':
			searching = Product.objects.filter(name__contains=search_query, available=True).order_by('price')
		elif sort_by == 'cheap':
			searching = Product.objects.filter(name__contains=search_query, available=True).order_by('-price')
		else:
			searching = Product.objects.filter(name__contains=search_query, available=True).order_by('name')
	quantity_of_goods = len(searching)
	return render(request, 'search.html', {'searches':searching, 'quantity':quantity_of_goods})
