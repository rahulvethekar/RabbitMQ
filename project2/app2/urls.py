from django.urls import path
from .views import EmployeeView

urlpatterns = [
    path('employee/list/',EmployeeView.as_view({'get':'get'})),
    path('create/employee/',EmployeeView.as_view({'post':'post'})),
    path('update/employee/',EmployeeView.as_view({'put':'put'})),
    path('delete/employee/',EmployeeView.as_view({'delete':'delete'})),


]