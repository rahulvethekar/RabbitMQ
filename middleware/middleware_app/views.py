from sys import api_version
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
import requests
from rest_framework import status
from .generate_queue import *

# Create your views here.
class ConsumeApiView(APIView):
    #Broker Queue parameters
    HOST = 'localhost'
    QUEUE = 'queue1'
    ROUTING_KEY = 'queue1'
    
    BASE_URL = 'http://127.0.0.1:8002'    #url for consume data


    def post(self,request):
        data = request.data
        endpoint = request.data.get('url')
        url = f"{self.BASE_URL}/{endpoint}"
        #print('middleware',request.data)
        #print(request.data.get('fname'))
        d = request.data
        d1 = {}
        for i in d:
            if i != 'url' and i != 'method':
                d1[i] = request.data.get(i)
        # print(d1)


        try:
            if request.data.get('method') == 'get':
                response = requests.get(url)
                return Response(response.json(),status = status.HTTP_200_OK)#GET Request

            elif request.data.get('method') == 'post':
                
                response = requests.post(url,data=d1)
                return Response(response.json(),status=status.HTTP_201_CREATED)#POST Request

            elif request.data.get('method') == 'put':
                response = requests.put(url,data=d1)
                return Response(response.json(),status=status.HTTP_205_RESET_CONTENT)#PUT Request

            elif request.data.get('method') == 'delete':
                response = requests.delete(url,data=d1)
                return Response(response.json(),status=status.HTTP_202_ACCEPTED)#DELETE Request

            
        except Exception as e:
            data = data.dict()
            data['retry_count'] = 0
            generate_queue(
                    queue = self.QUEUE,
                    host = self.HOST,
                    routing_key = self.ROUTING_KEY,
                    data = data
                    
                        )
            return Response({"error":"Trying again....."},status = status.HTTP_500_INTERNAL_SERVER_ERROR)




