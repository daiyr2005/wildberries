from .models import Product
from  django_filters import  FilterSet

class ProductListFilter(FilterSet):
    class Meta:
        model = Product
        fields = {
            'subcategory': ['exact'],
            'price': ['gt',  'lt']
        }
