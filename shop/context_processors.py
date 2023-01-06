from .models import Category, Product

def categorys(request):
    links = Category.objects.all()
    return dict(links=links)