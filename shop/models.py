from django.db import models
from django.urls import reverse

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=170, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.CharField(max_length=100, blank=True)

    class Meta:
        ordering = ('name', )
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
    
    def get_url(self):
        return reverse('products_by_category', args=[self.slug])

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=250, unique=True)
    slug = models.SlugField(max_length=250, unique=True)
    description = models.TextField(blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='images')
    stock = models.IntegerField()
    available = models.BooleanField(default=True)

    class Meta:
        ordering = ('name', )
        verbose_name = 'Product'
        verbose_name_plural = 'Products'

    def name_limit(self):
        return self.name[:47]+'...'
    
    def get_url(self):
        return reverse('product_detail', args=[self.category.slug, self.slug])

    def __str__(self):
        return self.name

class Cart(models.Model):
	cart_id = models.CharField(max_length=250, blank=True)
	date_added = models.DateField(auto_now_add=True)
	class Meta:
		ordering = ['date_added']
		db_table = 'Cart'


	def __str__(self):
		return self.cart_id

class CartItem(models.Model):
	product = models.ForeignKey(Product, on_delete=models.CASCADE)
	cart = models.ForeignKey(Cart, on_delete= models.CASCADE)
	quantity = models.IntegerField()
	active = models.BooleanField(default=True)

	class Meta:
		db_table = 'CartItem'


	def sub_total(self):
		return self.product.price * self.quantity


	def __str__(self):
		return self.product
