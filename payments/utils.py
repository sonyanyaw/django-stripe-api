from django.conf import settings


def get_stripe_keys_by_currency(currency):
    if currency.lower() == 'eur':
        return settings.STRIPE_PUBLIC_KEY_EUR, settings.STRIPE_SECRET_KEY_EUR
    
    return settings.STRIPE_PUBLIC_KEY_USD, settings.STRIPE_SECRET_KEY_USD