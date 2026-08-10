import logging
import stripe
from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_GET
from .models import Item

logger = logging.getLogger(__name__)

stripe.api_key = settings.STRIPE_SECRET_KEY

@require_GET
def buy_item(request, item_id):
    item = get_object_or_404(Item, id=item_id)

    logger.info("Creating checkout session for item_id=%s", item_id)
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
            metadata={"item_id": str(item.id)},
        )
    except stripe.StripeError:
        logger.exception(f"Stripe error for {item_id}")
        return JsonResponse({"error": "Payment session could not be created"})

    logger.info("Created session_id=%s for item_id=%s", session.id, item_id)
    return JsonResponse({"session_id": session.id})
