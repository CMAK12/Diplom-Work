from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, Category, Cart, CartItem, Wishlist, WishlistItem
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import send_mail
from .forms import SendMailToUser

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
				products = Product.objects.filter(category=category_page, available=True)
	else:
		if sort_by == 'expensive':
			products = Product.objects.all().filter(available=True).order_by('-price')
		elif sort_by == 'cheap':
			products = Product.objects.all().filter(available=True).order_by('price')
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
	search_query = request.GET['search']
	sort_by = request.GET.get('sort')

	if search_query == None:
		if sort_by == 'expensive':
			searching = Product.objects.all().filter(available=True).order_by('price')
		elif sort_by == 'cheap':
			searching = Product.objects.all().filter(available=True).order_by('-price')
		else:
			searching = Product.objects.all().filter(available=True)
	else:
		if sort_by == 'expensive':
			searching = Product.objects.filter(name__contains=search_query, available=True).order_by('price')
		elif sort_by == 'cheap':
			searching = Product.objects.filter(name__contains=search_query, available=True).order_by('-price')
		else:
			searching = Product.objects.filter(name__contains=search_query, available=True)
	quantity_of_goods = len(searching)
	return render(request, 'search.html', {'searches':searching, 'quantity':quantity_of_goods})

def _cart_id(request):
	cart = request.session.session_key
	if not cart:
		cart = request.session.create()
	return cart

def add_cart(request, product_id):
	product = Product.objects.get(id=product_id)
	try:
		cart = Cart.objects.get(cart_id=_cart_id(request))
	except Cart.DoesNotExist:
		cart = Cart.objects.create(cart_id=_cart_id(request))
		cart.save()
	try:
		cart_item = CartItem.objects.get(product=product, cart=cart)
		if cart_item.quantity < cart_item.product.stock:
			cart_item.quantity += 1
		cart_item.save()
	except CartItem.DoesNotExist:
		cart_item = CartItem.objects.create(product=product, quantity=1, cart=cart)
		cart_item.save()
	return redirect('cart_detail')

def cart_remove(request, product_id):
	cart = Cart.objects.get(cart_id=_cart_id(request))
	product = get_object_or_404(Product, id=product_id)
	cart_item = CartItem.objects.get(product=product, cart=cart)
	if cart_item.quantity > 1:
		cart_item.quantity -= 1
		cart_item.save()
	else:
		cart_item.delete()
	return redirect('cart_detail')

def cart_delete(request, product_id):
	cart = Cart.objects.get(cart_id=_cart_id(request))
	product = get_object_or_404(Product, id=product_id)
	cart_item = CartItem.objects.get(product=product, cart=cart)
	cart_item.delete()
	return redirect('cart_detail')

def cart_detail(request, total=0, counter=0, cart_items=None):
	try:
		cart = Cart.objects.get(cart_id=_cart_id(request))
		cart_items = CartItem.objects.filter(cart=cart, active=True)
		for cart_item in cart_items:
			total += (cart_item.product.price * cart_item.quantity)
			counter += cart_item.quantity
	except ObjectDoesNotExist:
		pass
	return render(request, 'cart.html', dict(cart_items=cart_items, total=total, counter=counter))

def buying(request):
	form = SendMailToUser(request.POST)
	if request.method == 'POST':
		if form.is_valid():
			firstname = form.cleaned_data['firstname']
			lastname = form.cleaned_data['lastname']
			email = form.cleaned_data['email']
			cart_item = CartItem.objects.all()

			send_mail(
				'Purchase complete!',
				f'Дякую за покупку, {firstname} {lastname}', 
				'phoneshop@samsa.com',
				[email]
				)

			cart_item.delete()

			return redirect('buyed')
	return render(request, 'buy.html', {'form':form})

def buyed(request):
	return render(request, 'buyed.html')

def wishlist_add(request, product_id):
	product = Product.objects.get(id=product_id)
	try:
		wishlist = Wishlist.objects.get(wishlist_id=_cart_id(request))
	except Wishlist.DoesNotExist:
		wishlist = Wishlist.objects.create(wishlist_id=_cart_id(request))
		wishlist.save()
	try:
		wishlist_item = WishlistItem.objects.get(product=product, wishlist=wishlist)
		wishlist_item.save()
	except WishlistItem.DoesNotExist:
		wishlist_item = WishlistItem.objects.create(product=product, quantity=1, wishlist=wishlist)
		wishlist_item.save()
	return redirect('wishlist')

def wishlist_delete(request, product_id):
	wishlist = Wishlist.objects.get(wishlist_id=_cart_id(request))
	product = get_object_or_404(Product, id=product_id)
	wishlist_item = WishlistItem.objects.get(product=product, wishlist=wishlist)
	wishlist_item.delete()
	return redirect('wishlist')

def wishlist(request, total=0, counter=0, wishlist_items=None):
	try:
		wishlist = Wishlist.objects.get(wishlist_id=_cart_id(request))
		wishlist_items = WishlistItem.objects.filter(wishlist=wishlist, active=True)
		for wishlist_item in wishlist_items:
			total += (wishlist_item.product.price * wishlist_item.quantity)
			counter += (wishlist_item.product.price * wishlist_item.quantity)
	except ObjectDoesNotExist:
		pass
	return render(request, 'wishlist.html', dict(wishlist_items=wishlist_items, total=total, counter=counter))