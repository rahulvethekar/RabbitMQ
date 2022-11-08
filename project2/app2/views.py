from django.shortcuts import render
from .models import Employee
from .serializers import EmployeeSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
# Create your views here.

class EmployeeView(ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    def get(self,request):

        try:
           employees =self.queryset
           serializer = self.serializer_class(employees,many=True)
           return Response(serializer.data,status = status.HTTP_200_OK)

        except Exception as e:            
            return Response({"error":str(e)},status = status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self,request):
        try:
            serializer = self.serializer_class(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({"msg":"data created"},status=201)
            return Response({"error":serializer.errors},status=400)
        except Exception as e:
            
            return Response({"error":str(e)},status = 500)
            
    def put(self,request):
        
        try:
            emp = Employee.objects.get(id=request.data.get('id'))

        except Employee.DoesNotExist:
            return Response({'error':'record not found'},status=status.HTTP_204_NO_CONTENT)

        serializer = EmployeeSerializer(emp,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg':'data updated'},status=status.HTTP_205_RESET_CONTENT)
        return Response({'error':'invalid data'},status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)

    def delete(self,request):
        try:
            emp = Employee.objects.get(id=request.data.get('id'))
            emp.delete()
            return Response({'msg':'record deleted!'},status=status.HTTP_200_OK)  
              
        except Employee.DoesNotExist:
            return Response({'error':'record not found'},status=status.HTTP_204_NO_CONTENT)




    

    
        