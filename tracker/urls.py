from django.urls import path
from .import views
urlpatterns = [


    path('',views.login_page),
    path('home/',views.home,name="home"),
    path('edit/<int:data_id>',views.edit,name="edit"),
    path('delete_it/<int:data_id>',views.delete_it,name="delete_it"),



    path('profile/',views.profile),
    path('about/',views.about),
    path('contact/',views.contact_us),

    path('login/',views.login_page,name="login"),
    path('logout/',views.logout_page,name="logout"),
    path('register/',views.register_page),
    path('expense/',views.expense,name="expense"),
    path('add_expense/',views.add_expense,name="add_expense"),


]
