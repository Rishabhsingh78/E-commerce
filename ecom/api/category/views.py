from rest_framework import viewsets
from .serializers import CategorySerializer
from .models import Category
# Create your views here.

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all().order_by('name') # this write the queryset in db 

    serializer_class = CategorySerializer # this will convert the query in the json format
