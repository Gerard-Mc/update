from django.shortcuts import render
import uuid
from order.forms import CustomProductForm


def view_cart(request):
    """ Returns the cart page """

    return render(request, 'cart/cart.html')

def add_to_cart(request):
    """ Add item to the cart page """
    id = str(uuid.uuid4())
    item_type = request.POST.get('category')
    complexity = request.POST.get('complexity')
    variations = request.POST.get('variations')
    user_description = request.POST.get('user_description')
    fast_delivery = request.POST.get('fast_delivery')

    cart_product = {
      "category": item_type, "complexity": complexity,
      "variations": variations, "user_description": user_description,
      "fast_delivery": fast_delivery,
}
    product_id = { f"{id}": [cart_product]}
    cart = request.session.get('cart', {})
    cart.__setitem__(id, cart_product)
    request.session['cart'] = cart
    form = CustomProductForm()
    context = {
        'form': form
    }

    return render(request, 'order/order.html', context)

def remove_from_cart(request):
    """ Returns item from the cart page """
    id = request.POST.get('id')
    cart = request.session.get('cart', {})
    del cart[id]
    request.session['cart'] = cart

    return render(request, 'cart/cart.html')
