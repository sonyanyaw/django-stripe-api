from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
import stripe

from .models import Item, Order
from .utils import get_stripe_keys_by_currency

# Create your views here.
def main_page(request):
    items = Item.objects.all().order_by('name')
    orders = Order.objects.all()
    return render(request, 'home.html', {'items': items, 'orders': orders})

def checkout_session_view(request, id):
    """
    Stripe Checkout для Item 
    """
    item = get_object_or_404(Item, id=id)
    _, stripe.api_key = get_stripe_keys_by_currency(item.currency)

    success_url = request.build_absolute_uri(reverse('success'))
    cancel_url = request.build_absolute_uri(reverse('cancel'))

    session = stripe.checkout.Session.create(
        line_items=[
            {
                'price_data': {
                    'currency': item.currency,
                    'product_data': {
                        'name': item.name,
                        'description': item.description, 
                    },
                    'unit_amount': int(item.price * 100), 
                },
                "quantity": 1
            }
        ],
        mode="payment",
        success_url=success_url,
        cancel_url=cancel_url,
    )
    
    return JsonResponse({'id': session.id})


def item_details_view(request, id):
    item = get_object_or_404(Item, id=id)
    public_key, _ = get_stripe_keys_by_currency(item.currency)

    return render(request, 'item-detail.html', {
        'item': item,
        'public_key': public_key
    })


def order_checkout_view(request, id):
    """
    Stripe Checkout для Order 
    """
    order = get_object_or_404(Order, id=id)
    currency = order.currency()
    _, stripe.api_key = get_stripe_keys_by_currency(currency)

    success_url = request.build_absolute_uri(reverse('success'))
    cancel_url = request.build_absolute_uri(reverse('cancel'))

    tax_rate_id = None
    if order.tax:
        if currency == 'eur' and order.tax.stripe_id_eur:
            tax_rate_id = order.tax.stripe_id_eur
        else:
            tax_rate_id = order.tax.stripe_id_usd

    line_items = []

    for item in order.items.all():
        line_items.append({
            'price_data': {
                'currency': item.currency,
                'product_data': {'name': item.name,},
                'unit_amount': int(item.price * 100),
            },
            'quantity': 1,
            'tax_rates': [tax_rate_id] if tax_rate_id else []
        })

    discounts_list = []
    if order.discount:
        if currency == 'eur' and order.discount.stripe_id_eur:
            discounts_list.append({'coupon': order.discount.stripe_id_eur})
        else:
            discounts_list.append({'coupon': order.discount.stripe_id_usd})

    session = stripe.checkout.Session.create(
        line_items=line_items,
        discounts=discounts_list,
        mode='payment',
        success_url=success_url,
        cancel_url=cancel_url,
    )

    return JsonResponse({'id': session.id})


def order_detail_view(request, id):
    order = get_object_or_404(Order, id=id)
    public_key, _ = get_stripe_keys_by_currency(order.currency())
    
    return render(request, 'order-detail.html', {
        "order": order,
        "public_key": public_key
    })


def success_view(request):
    return render(request, 'success.html')


def cancel_view(request):
    return render(request, 'cancel.html')
