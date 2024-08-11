from django.urls import path
from . import views 
urlpatterns = [
    path('',views.home, name='home-page'),
    path('signup', views.signup,name="signup-page"),
    path('signout', views.signout,name="signout-page"),
    path('add_to_cart/<int:p_id>', views.add_to_cart,name="add_to_cart-page"),
    path('item/<int:p_id>', views.viewitem,name="view_item"),

    path('allcart', views.viewCart,name="vcart-page"),
    path('remove_cart/<int:id>', views.removeCart,name="remove_cart-page"),
    path("initiate-payment/", views.initiate_payment, name="initiate_payment"),
    path("payment-success/", views.payment_success, name="payment_success"),
    path("payment-failed/", views.payment_failed, name="payment_failed"),
    path("order/", views.viewOrders, name="order-page"),
    path("allprod/", views.allprod, name="allprod-page"),
    path("profile/", views.profile, name="profile-page"),
     path("contact/", views.contact_us, name='contact_us'),
     path('search/', views.search_results, name='search_results'),
     path('rm_to_cart/<int:p_id>', views.rm_to_cart,name="remove_to_cart-page"),







]