from django.shortcuts import render, redirect, reverse, HttpResponse, get_object_or_404
from django.contrib import messages
from django.views.decorators.http import require_POST
from .forms import OrderForm
from cart.contexts import cart_contents
import stripe
from django.conf import settings
from checkout.models import Category
from .models import Order, OrderLineItem
from decimal import Decimal
import json


@require_POST
def cache_checkout_data(request):
    try:
        pid = request.POST.get('client_secret').split('_secret')[0]
        stripe.api_key = settings.STRIPE_SECRET_KEY
        stripe.PaymentIntent.modify(pid, metadata={
            'cart': json.dumps(request.session.get('cart', {})),
            'save_info': request.POST.get('save_info'),
            'username': request.user,
        })
        return HttpResponse(status=200)
    except Exception as e:
        messages.error(request, 'Sorry, your payment cannot be \
            processed right now. Please try again later.')
        return HttpResponse(content=e, status=400)


def checkout(request):
    stripe_public_key = settings.STRIPE_PUBLIC_KEY
    stripe_secret_key = settings.STRIPE_SECRET_KEY
    if request.method == 'POST':
        cart = request.session.get('cart', {})
        form_data = {
            'full_name': request.POST['full_name'],
            'email': request.POST['email'],
            'phone_number': request.POST['phone_number'],
            'country': request.POST['country'],
            'postcode': request.POST['postcode'],
            'town_or_city': request.POST['town_or_city'],
            'street_address1': request.POST['street_address1'],
            'street_address2': request.POST['street_address2'],
            'county': request.POST['county'],
        }
        order_form = OrderForm(form_data)
        if order_form.is_valid():
            order = order_form.save(commit=False)
            pid = request.POST.get('client_secret').split('_secret')[0]
            order.stripe_pid = pid
            order.original_cart = json.dumps(cart)
            order.save()
            for item in cart.items():
                item_price = 0
                delivery = False
                complexity = Decimal(item[1]["complexity"])
                variations = Decimal(item[1]["variations"])
                category = get_object_or_404(Category, pk=int(item[1]["category"]))
                item_price = category.price
                item_price = Decimal(item_price) * complexity
                item_price = Decimal(item_price) * variations
                if item[1]["fast_delivery"] == "True":
                    delivery = True
                    item_price = Decimal(item_price) * Decimal(settings.FAST_DELIVERY_CHARGE)
                    item_price = Decimal(round(item_price, 2))

                if id:
                    order_line_item = OrderLineItem(
                        order=order,
                        category=category,
                        complexity=item[1]["complexity"],
                        variations=item[1]["variations"],
                        user_description=item[1]["user_description"],
                        fast_delivery=delivery,
                        lineitem_total=Decimal(item_price),
                        )
                    order_line_item.save()

            request.session['save_info'] = 'save-info' in request.POST
            return redirect(reverse('checkout_success', args=[order.order_number]))

    else:
        cart = request.session.get('cart', {})
        if not cart:
            messages.error(request, "Your cart is empty.")
            return redirect(reverse('order'))

    
        current_cart = cart_contents(request)
        total = current_cart['total']
        stripe_total = round(total * 100)
        stripe.api_key = stripe_secret_key
        intent = stripe.PaymentIntent.create(
            amount=stripe_total,
            currency=settings.STRIPE_CURRENCY,
        )
                
        form = OrderForm()
        template = 'checkout/checkout.html'
        context = {
            'OrderForm': OrderForm,
            'stripe_public_key': stripe_public_key,
            'client_secret': intent.client_secret,

        }

    return render(request, template, context)


def checkout_success(request, order_number):
    """
    Handle successful checkouts
    """
    save_info = request.session.get('save_info')
    order = get_object_or_404(Order, order_number=order_number)
    messages.success(request, f'Order successfully processed! \
        Your order number is {order_number}. A confirmation \
        email will be sent to {order.email}.')

    if 'cart' in request.session:
        del request.session['cart']

    template = 'checkout/checkout_success.html'
    context = {
        'order': order,
    }

    return render(request, template, context)

