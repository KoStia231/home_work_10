# Утилиты для платежки
import stripe
from django.conf import settings

stripe.api_key = settings.STRIPE_SECRET_KEY


def create_product(name):
    """
    Создание продукта в Stripe.

    :param name: Название продукта.
    :return: Объект продукта от Stripe.
    """
    try:
        product = stripe.Product.create(name=name)
        return product
    except Exception as e:
        return {"error": str(e)}


def create_price(product_id, amount, currency='usd'):
    """
    Создание цены для продукта в Stripe.

    :param product_id: ID продукта.
    :param amount: Сумма в копейках.
    :param currency: Валюта.
    :return: Объект цены от Stripe.
    """
    try:
        price = stripe.Price.create(
            product=product_id,
            unit_amount=amount,
            currency=currency,
        )
        return price
    except Exception as e:
        return {"error": str(e)}


def create_checkout_session(price_id):
    """
    Создание сессии для платежа в Stripe.

    :param price_id: ID цены.
    :return: Объект сессии от Stripe.
    """
    try:
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price': price_id,
                'quantity': 1,
            }],
            mode='payment',
            success_url='http://localhost:8000/',
            cancel_url='http://localhost:8000/',
        )
        return session
    except Exception as e:
        return {"error": str(e)}


def get_session_status(session_id):
    """
    Получение статуса сессии платежа из Stripe.

    :param session_id: ID сессии.
    :return: Объект сессии от Stripe.
    """
    try:
        session = stripe.checkout.Session.retrieve(session_id)
        return session
    except Exception as e:
        return {"error": str(e)}

