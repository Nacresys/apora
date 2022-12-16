
from django.contrib import admin
from django.urls import path, include

from picker import views

app_name = 'picker'

urlpatterns = [
    path('picker_login',views.picker_login,name='picker_login'),
    path('picker_view',views.picker_view,name="picker_view"),
    path('picker_dashboard',views.picker_dashboard,name="picker_dashboard"),
    path('start_pick/<str:pickid>/',views.start_pick,name="start_pick"),
    path('logout',views.logout,name="logout"),
    path('pickqr/<int:proid>/',views.pickqr,name="pickqr"),
    path('test',views.test,name="test"),
    path('qrvaluefetch',views.qrvaluefetch,name="qrvaluefetch"),
    path('bincode',views.bincode,name="bincode"),
    path('orderdetails/<str:oid>/',views.orderdetails,name="orderdetails"),
    path('qrverify',views.qrverify,name="qrverify"),
    path('binqrvalue',views.binqrvalue,name="binqrvalue"),
    path('qrvalidation',views.qrvalidation,name="qrvalidation"),
    path('pickdrop/<int:proid>/<int:oqty>/<int:pqty>/<str:pname>/<str:oid>/',views.pickdrop,name="pickdrop"),
]