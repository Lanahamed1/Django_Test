from rest_framework import serializers 
from .models import Order,OrderItem



class OrderItemSerilizer(serializers.Serializer):
    class Meta:
        model=OrderItem
        fields='__all__'




class OrderSerilizer(serializers.ModelSerializer):
    orderItems=serializers.SerializerMethodField(method_name='get_order_items',read_only=False)
    class Meta:
        model=Order
        fields='__all__'

    def get_order_items(self,obj):
        order_items=obj.orderitem.all()
        serializer=OrderItemSerilizer(order_items,many=True)
        return serializer.data