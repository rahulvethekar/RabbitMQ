from django.shortcuts import render
from rest_framework.views import APIView 
from rest_framework.response import Response
from .serializers import EmployeeSerializer
from .parameters import *
import requests
from rest_framework import status
import json

# Create your views here.

class MiddlewareCallApi(APIView):

    def post(self,request):
        serializer = EmployeeSerializer(data=payload)
        print('------------------------------',request.data)
        
        try:
            if serializer.is_valid():
                url = f"{BASE_URL}/{END_POINT}"
                response = requests.post(url,data=(request.data))

                print('---------------------------',response.json())
                return Response(response.json(),status=status.HTTP_200_OK)
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error":str(e),'msg':'test'},status = status.HTTP_500_INTERNAL_SERVER_ERROR)
            


