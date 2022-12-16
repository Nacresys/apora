

from django.urls import path

from supervisor import views

app_name = 'supervisor'

urlpatterns = [
    path('supervisor_login',views.supervisor_login,name='supervisor_login'),
    path('bincode_generation',views.bincode,name='bincode'),
    path('orderdetails/<str:odrid>/',views.orderdetails,name="orderdetails"),
    path('qrgeneration',views.qrgeneration,name="qrgeneration"),
    path('activity_status',views.activity_status,name="activity_status"),
    path('orderwise_pl/<str:odrid>/',views.orderwise_pl,name="orderwise_pl"),
    path('pickerwise_pl/<int:pickerid>/',views.pickerwise_pl,name="pickerwise_pl"),
    path('pickwise_pl/<str:pickid>/',views.pickwise_pl,name="pickwise_pl"),
    path('planogram',views.planogram,name="planogram"),
    path('add_product',views.addpro,name="addpro"),
    path('picklist_reassign',views.picklist_reassign,name="picklist_reassign"),
    path('reassign',views.reassign,name="reassign"),
    path('logout',views.logout,name='logout'),
]