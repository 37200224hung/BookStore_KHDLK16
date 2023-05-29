from django.urls import path
from .views import BooksListView, BooksDetailView, BookCheckoutView, paymentComplete, SearchResultsListView, view_cart, remove_from_cart, update_cart, clear_cart

urlpatterns = [
    path('', BooksListView.as_view(), name='list'),
    path('<int:pk>/', BooksDetailView.as_view(), name='detail'),
    path('<int:pk>/checkout/', BookCheckoutView.as_view(), name='checkout'),
    path('complete/', paymentComplete, name='complete'),
    path('search/', SearchResultsListView.as_view(), name='search_results'),
    path('cart/', view_cart, name='view_cart'),
    path('cart/remove/<int:cart_item_id>/', remove_from_cart, name='remove_from_cart'),
    path('cart/update/<int:cart_item_id>/', update_cart, name='update_cart'),
    path('cart/clear/', clear_cart, name='clear_cart'),
]
