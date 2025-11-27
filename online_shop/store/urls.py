from .views import (UserProfileViewSet,CategoryListAPIView,FavoriteViewSet,
                    SubCategoryListAPIView,SubCategoryDetailAPIView,ProductListAPIView,ProductDetailAPIView,CategoryDetailAPIView,
                    ReviewViewSet,CartViewSet,CartItemViewSet,RegisterView, LoginView, LogoutView,FavoriteItemViewSet )

from rest_framework import  routers
from  django.urls import path, include

router = routers.DefaultRouter()
router.register(r'users', UserProfileViewSet)
router.register(r'Review',ReviewViewSet)
router.register(r'favorites', FavoriteViewSet, basename='favorites')
router.register(r'favorite-items', FavoriteItemViewSet, basename='favorite-items')
router.register(r'cart', CartViewSet, basename='cart')
router.register(r'cart_items', CartItemViewSet, basename='cart_items')

urlpatterns = [
    path('', include(router.urls)),
    path('product/', ProductListAPIView.as_view(),name='product_list'),
    path('product/<int:pk>/', ProductDetailAPIView.as_view(), name='product_detail'),
    path('category/', CategoryListAPIView.as_view(),name='category_list'),
    path('category/<int:pk>/', CategoryDetailAPIView.as_view(), name='category_detail'),
    path('subcategory/', SubCategoryListAPIView.as_view(), name='subcategory_list'),
    path('subcategory/<int:pk>/', SubCategoryDetailAPIView.as_view(), name='subcategory_detail'),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='register'),
    path('logout/', LogoutView .as_view(), name='logout'),
    # path('cart/', CartViewSet.as_view(), name='cart_detail'),
    # path('cart_items/', CartItemViewSet.as_view({'get': 'list', 'post': 'create'})),
    # path('cart_items/<int:pk>/', CartItemViewSet.as_view({'put': 'update', 'delete': 'destroy'}))

]
