from django.urls import path
from .views import (
    DetailViewPage,
    CreateViewPage,
    UpdateViewPage,
    DeleteViewPage,
    SearchPage,
    OrderViewPage,
    cart,
    checkout,
    store,
    updateItem)

urlpatterns=[
    path('post/<int:pk>/delete/', DeleteViewPage.as_view(), name='delete_post'),
    path('post/<int:pk>/edit/', UpdateViewPage.as_view() , name='update_post'),
    path('post/<int:pk>/', DetailViewPage.as_view(), name='detail_post'),
    path('post/new/', CreateViewPage.as_view(), name='create_newpost'),
    path('', store, name='home'),
    path('search/', SearchPage , name='search-post'),
    path('buyurtma/<int:pk>/',OrderViewPage.as_view(), name='buyurtma'),
    path('cart/', cart, name="cart"),
	path('checkout/',checkout, name="checkout"),
    path('update_item/',updateItem, name='update_item'),


]


