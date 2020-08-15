from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.registerPage, name="register"),
    path('login/', views.loginPage, name="login"),
    path('logout/', views.logoutUser, name="logout"),
    path('', views.home, name="home"),
   # path('update_product/<str:id>/', views.update_product, name="update_product"),
    path('product_view/<str:id>/', views.product_view, name="product_view"),
    path('products/', views.products_view, name='products'),
    path('product_add/', views.product_add, name='product_add'),
    path('product_configure/', views.product_configure, name='product_configure'),
    path('reports/', views.reports, name='reports'),

]
