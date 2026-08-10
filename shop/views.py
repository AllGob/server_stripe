import logging
import stripe
from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render,get_object_or_404
from django.views.decorators.http import require_GET
from .models import Item, Order

logger = logging.getLogger(__name__)
stripe.api_key = settings.STRIPE_SECRET_KEY

@require_GET
def buy_item(request, item_id):
    item = get_object_or_404(Item, id=item_id) 
    logger.info("Sesion for item_id=%s", item_id)
    try:
        session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=[
                {
                    "price_data": {
                        "currency": "usd",
                        "product_data": {
                            "name": item.name,
                            "description": item.description,
                        },
                        "unit_amount": int(item.price * 100),
                    },
                    "quantity": 1,
                }
            ],
            mode="payment",
            success_url=request.build_absolute_uri("/success/"),
            cancel_url=request.build_absolute_uri("/cancel/"),
            metadata={"item_id": str(item.id)}, #webhook
        )
    except stripe.StripeError:
        logger.exception(f"Stripe error for {item_id}")
        return JsonResponse({"error": "Payment session could not be created"})
    logger.info("Created session_id=%s for item_id=%s", session.id, item_id)
    return JsonResponse({"session_id": session.id})
@require_GET
def payment_success(request):
    return render(request, "shop/success.html")
@require_GET
def payment_cancel(request):
    return render(request, "shop/cancel.html",status=400)
@require_GET
def item_detail(request, item_id):
    item = get_object_or_404(Item, id=item_id)
    return render(
        request,
        "shop/itemdetail.html",
        {"item": item, "stripe_publishable_key": settings.STRIPE_PUBLISHABLE_KEY},
        status=200,
    )
@require_GET
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(
        request,
        "shop/orderdetail.html",
        {
            "order": order,
            "total_price": order.total_price(),
            "stripe_publishable_key": settings.STRIPE_PUBLISHABLE_KEY,
        },
    )
@require_GET
def buy_order(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    tax_rate_id = get_or_create_stripe_tax_rate(order.tax) if order.tax else None
    line_items = [
        {
            "price_data": {
                "currency": "usd",
                "product_data": {
                    "name": item.name,
                    "description": item.description,
                },
                "unit_amount": int(item.price * 100),
                **({"tax_rates": [tax_rate_id]} if tax_rate_id else {}), #ДОБАВЛЕНИЕ TAX ТОЛЬКО ЕСЛИ СУЩЕСТВУЕТ
            },
            "quantity": 1,
        }
        for item in order.items.all()
    ]

    logger.info("Creating checkout session for order_id=%s", order_id)
    try:
        session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=line_items,
            mode="payment",
            success_url=request.build_absolute_uri("/success/"),
            cancel_url=request.build_absolute_uri("/cancel/"),
        )
    except stripe.StripeError:
        logger.exception(f"Stripe error for order {order_id}")
        return JsonResponse({"error": "Payment session could not be created"}, status=502)

    logger.info("Created session_id=%s for order_id=%s", session.id, order_id)
    return JsonResponse({"session_id": session.id})
def get_or_create_stripe_tax_rate(tax):
    if tax.stripe_tax_rate_id:
        return tax.stripe_tax_rate_id
    stripe_tax_rate = stripe.TaxRate.create(
        display_name=tax.name,
        percentage=float(tax.percentage),
        inclusive=False,
    )
    tax.stripe_tax_rate_id = stripe_tax_rate.id
    tax.save(update_fields=["stripe_tax_rate_id"])
    return tax.stripe_tax_rate_id
