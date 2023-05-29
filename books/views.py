from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Book, Order, Cart, CartItem
from django.urls import reverse_lazy
from django.db.models import Q, Sum
from django.http import JsonResponse
import json
from django.contrib.auth.models import AnonymousUser
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from django.views import View

class BooksListView(ListView):
    model = Book
    paginate_by = 15
    ordering = 'id'
    template_name = 'list.html'


class BooksDetailView(DetailView):
    model = Book
    template_name = 'detail.html'


class SearchResultsListView(ListView):
    model = Book
    template_name = 'search_results.html'

    def get_queryset(self):
        query = self.request.GET.get('q')
        return Book.objects.filter(
            Q(title__icontains=query) | Q(author__icontains=query)
        )


class BookCheckoutView(LoginRequiredMixin, DetailView):
    model = Book
    template_name = 'checkout.html'
    login_url = 'login'

    def post(self, request, *args, **kwargs):
        book_id = self.kwargs['pk']
        book = Book.objects.get(id=book_id)
        cart, created = Cart.objects.get_or_create(user=request.user)
        cart_item, item_created = CartItem.objects.get_or_create(cart=cart, book=book)
        if not item_created:
            cart_item.quantity += 1
            cart_item.save()
        messages.success(request, 'Đã thêm vào giỏ hàng')
        return redirect('view_cart')


def paymentComplete(request):
    body = json.loads(request.body)
    print('BODY:', body)
    product = Book.objects.get(id=body['productId'])
    Order.objects.create(
        product=product
    )
    return JsonResponse('Payment completed!', safe=False)


def view_cart(request):
    try:
        if request.user.is_authenticated:
            cart = Cart.objects.get(user=request.user)
            cart_items = cart.cartitem_set.all()
            total_quantity = cart_items.aggregate(Sum('quantity'))['quantity__sum']
            cart_items_with_subtotal = []
            total_price = 0

            for cart_item in cart_items:
                subtotal = cart_item.book.price * cart_item.quantity
                total_price += subtotal
                cart_items_with_subtotal.append((cart_item, subtotal))
        else:
            cart = None
            cart_items = []
            total_quantity = 0
            cart_items_with_subtotal = []
            total_price = 0
    except (Cart.DoesNotExist, ObjectDoesNotExist):
        cart = None
        cart_items = []
        total_quantity = 0
        cart_items_with_subtotal = []
        total_price = 0

    return render(request, 'cart.html', {
        'cart': cart,
        'cart_items_with_subtotal': cart_items_with_subtotal,
        'total_quantity': total_quantity,
        'total_price': total_price
    })


def remove_from_cart(request, cart_item_id):
    try:
        cart_item = CartItem.objects.get(id=cart_item_id)
        cart_item.delete()
    except CartItem.DoesNotExist:
        pass
    return redirect('view_cart')


def update_cart(request, cart_item_id):
    try:
        cart_item = CartItem.objects.get(id=cart_item_id)
        if request.POST.get('quantity'):
            quantity = int(request.POST.get('quantity'))
            if quantity > 0:
                cart_item.quantity = quantity
                cart_item.save()
            else:
                cart_item.delete()
    except CartItem.DoesNotExist:
        pass
    return redirect('view_cart')


def clear_cart(request):
    try:
        if request.user.is_authenticated:
            cart = Cart.objects.get(user=request.user)
            cart.cartitem_set.all().delete()
    except (Cart.DoesNotExist, ObjectDoesNotExist):
        pass
    return redirect('view_cart')
