from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import ItemSerializer
from .models import Items

@api_view(['GET'])
def getData(request):
    items = Items.Facilities_Item(None,category='')
    serializer = ItemSerializer(items, many=True)
    serialized_data = serializer.data

    person = {'name': 'King', 'age': 28}
    return Response(serialized_data)