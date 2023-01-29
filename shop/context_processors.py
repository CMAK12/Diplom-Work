from .models import Category, Product, Cart, CartItem, Wishlist, WishlistItem
from .views import _cart_id

def categorys(request):
    links = Category.objects.all()
    return dict(links=links)

def wishlist_counter(request):
	item_count = 0
	if 'admin' in request.path:
		return {} 
	else:
		try:
			wishlist = Wishlist.objects.filter(cart_id=_cart_id(request))
			wishlist_items = WishlistItem.objects.all().filter(wishlist=wishlist[:1])
			for wishlist_item in wishlist_items:
				item_count += wishlist_item.quantity
		except Wishlist.DoesNotExist:
			item_count = 0
	return dict(items_count=item_count)

def counter(request):
	item_count = 0
	if 'admin' in request.path:
		return {} 
	else:
		try:
			cart = Cart.objects.filter(cart_id=_cart_id(request))
			cart_items = CartItem.objects.all().filter(cart=cart[:1])
			for cart_item in cart_items:
				item_count += cart_item.quantity
		except Cart.DoesNotExist:
			item_count = 0
	return dict(item_count=item_count)