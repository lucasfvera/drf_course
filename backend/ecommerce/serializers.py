from collections import OrderedDict
from .models import Item, Order
from rest_framework_json_api import serializers
from rest_framework import status
from rest_framework.exceptions import APIException

# This should be in a separate file with all exceptions
class NotEnoughStockException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "There is not enough stock"
    default_code = "invalid"


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = (
            "title",
            "stock",
            "price",
        )


class OrderSerializer(serializers.ModelSerializer):

    item = serializers.PrimaryKeyRelatedField(queryset=Item.objects.all(), many=False)

    class Meta:
        model = Order
        fields = (
            "item",
            "quantity",
        )

    # is_valid method will call this method
    def validate(self, res: OrderedDict):
        """
        Used to validate Item stock levels
        """
        item = res.get("item")
        quantity = res.get("quantity")
        # Check if we got enough stock
        if not item.check_stock(quantity):
            raise NotEnoughStockException
        return res
