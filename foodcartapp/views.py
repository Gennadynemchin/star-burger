from django.http import JsonResponse
from django.templatetags.static import static
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework import renderers, serializers
from phonenumber_field.serializerfields import PhoneNumberField
from .models import Product, Order, Item
import phonenumbers
from phonenumbers import NumberParseException
from rest_framework.serializers import ModelSerializer, ListField, ValidationError


class PhoneNumberSerializer(serializers.Serializer):
    number = PhoneNumberField(region="RU")


def banners_list_api(request):
    # FIXME move data to db?
    return JsonResponse([
        {
            'title': 'Burger',
            'src': static('burger.jpg'),
            'text': 'Tasty Burger at your door step',
        },
        {
            'title': 'Spices',
            'src': static('food.jpg'),
            'text': 'All Cuisines',
        },
        {
            'title': 'New York',
            'src': static('tasty.jpg'),
            'text': 'Food is incomplete without a tasty dessert',
        }
    ], safe=False, json_dumps_params={
        'ensure_ascii': False,
        'indent': 4,
    })


def product_list_api(request):
    products = Product.objects.select_related('category').available()

    dumped_products = []
    for product in products:
        dumped_product = {
            'id': product.id,
            'name': product.name,
            'price': product.price,
            'special_status': product.special_status,
            'description': product.description,
            'category': {
                'id': product.category.id,
                'name': product.category.name,
            } if product.category else None,
            'image': product.image.url,
            'restaurant': {
                'id': product.id,
                'name': product.name,
            }
        }
        dumped_products.append(dumped_product)
    return JsonResponse(dumped_products, safe=False, json_dumps_params={
        'ensure_ascii': False,
        'indent': 4,
    })


class ItemSerializer(serializers.Serializer):
    class Meta:
        model = Item
        fields = ['product', 'order', 'quantity']


class OrderSerializer(ModelSerializer):
    products = ListField(child=ItemSerializer(), allow_empty=False)

    class Meta:
        model = Order
        fields = ['firstname', 'lastname', 'phonenumber', 'address', 'products']


@api_view(['POST'])
def register_order(request):
    frontend_data = request.data
    firstname = frontend_data.get('firstname')
    lastname = frontend_data.get('lastname')
    phonenumber = frontend_data.get('phonenumber')
    address = frontend_data.get('address')
    products = frontend_data.get('products', [])

    serializer_order = OrderSerializer(data=frontend_data)
    serializer_order.is_valid(raise_exception=True)

    if not isinstance(products, list):
        raise ValidationError('Expects products field be a list')

    order = Order.objects.create(firstname=firstname, lastname=lastname, phonenumber=phonenumber, address=address)
    for product in products:
        serializer_item = ItemSerializer(data=product)
        if Product.objects.filter(id=product['product']):
            serializer_item.is_valid(raise_exception=True)
            Item.objects.create(product=Product.objects.get(id=product['product']), order=order, quantity=product['quantity'])
            response = {"status": [{"200": "ok"}]}
        else:
            raise ValidationError('Requested id does not exist')
    return Response(response, status=status.HTTP_200_OK)
