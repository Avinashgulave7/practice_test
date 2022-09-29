from django.shortcuts import render
from .models import *
from .serializers import *
from rest_framework.decorators import api_view,permission_classes,authentication_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from rest_framework.pagination import PageNumberPagination
# Create your views here.
@api_view(['GET','POST','PUT','PATCH','DELETE'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def Product_Api(request,pk=None):
    if request.method == 'GET':
        if pk is not None:
            prod=Product.objects.get(id=pk)
            serializer=ProductSerializer(prod)
            return Response(serializer.data,status=status.HTTP_200_OK)
        paginator = PageNumberPagination()
        paginator.page_size = 10
        prod=Product.objects.all()
        result_page = paginator.paginate_queryset(prod, request)
        serializer=ProductSerializer(result_page,many=True)
        return paginator.get_paginated_response(serializer.data)

    if request.method=="POST":
        serializer=ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

    if request.method=="PUT":
        prod=Product.objects.get(pk=pk)
        serializer=ProductSerializer(prod,data=request.data,partial=False)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

    if request.method=="PATCH":
        prod=Product.objects.get(pk=pk)
        serializer=ProductSerializer(prod,data=request.data,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

    if request.method=="DELETE":
        prod=Product.objects.get(pk=pk)
        prod.delete()
        return Response(status=status.HTTP_200_OK)
