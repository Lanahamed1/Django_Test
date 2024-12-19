from django.shortcuts import get_object_or_404, render
from rest_framework.decorators import api_view,permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from product.filters import ProductsFilter
from .models import Product,Review
from .serializer import ProductSerializer
from rest_framework import status
from django.db.models import Avg
# Create your views here.




@api_view(['Get'])
def get_all_prodects(request):
    # products=Product.objects.all()
    filterset=ProductsFilter(request.GET,queryset=Product.objects.all().order_by('id'))
    serializer=ProductSerializer(filterset.qs,many=True)
    # print(products)
    return Response({'Products':serializer.data})

@api_view(['Get'])
def get_by_id_product(request,pk):
    products=get_object_or_404(Product,id=pk)
    serializer=ProductSerializer(products,many=False)
    print(products)
    return Response({'Products':serializer.data})



@api_view(['POST'])
@permission_classes([IsAuthenticated])
def new_product(request):
    data=request.data
    serializer = ProductSerializer(data = data)


    if  serializer.is_valid():
        products = Product.objects.create(**data, user=request.user)
        result=ProductSerializer(products,many=False)

        return Response({"products":result.data})
    else:
        return Response(serializer.errors)




@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def updata_product(request,pk):
    product=get_object_or_404(Product,id=pk)



    if product.user !=request.user:
       return Response({"errors":"sorry you can not updata this product "}
                       ,status=status.HTTP_403_FORBIDDEN)

    product.name=request.data['name']
    product.description=request.data['description']
    product.price=request.data['price']
    product.category=request.data['category']
    product.stock=request.data['stock']
    product.ratings=request.data['ratings']

    product.save()
    serializer=ProductSerializer(product,many=False)
    return Response({"products":serializer.data})



@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_product(request,pk):
    product=get_object_or_404(Product,id=pk)



    if product.user !=request.user:
       return Response({"errors":"sorry you can not updata this product "}
                       ,status=status.HTTP_403_FORBIDDEN)

    

    product.delete()
    return Response({"details":'Delete action is done'},status=status.HTTP_200_OK)








@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_review(request, pk):
    user = request.user
    product = get_object_or_404(Product, id=pk)
    data = request.data
    review = product.reviews.filter(user=user)  

    if data['rating'] <= 0 or data['rating'] > 10:
        return Response({"error": 'Please select a rating between 1 to 10'}, status=status.HTTP_400_BAD_REQUEST)

    elif review.exists():
        new_review = {'rating': data['rating'], 'comment': data['comment']}
        review.update(**new_review)

        rating = product.reviews.aggregate(avg_ratings=Avg('rating'))
        product.ratings = rating['avg_ratings']
        product.save()
        return Response({"details": "Product review updated"})

    else:
        Review.objects.create(
            user=user,
            product=product,
            rating=data['rating'],
            comment=data['comment']
        )

        rating = product.reviews.aggregate(avg_ratings=Avg('rating'))
        product.ratings = rating['avg_ratings']
        product.save()
        return Response({"details": "Product review created"})
