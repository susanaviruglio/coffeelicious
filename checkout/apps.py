from django.apps import AppConfig


class CheckoutConfig(AppConfig):
    """Import the signal module to the app"""
    name = 'checkout'

    def ready(self):
        import checkout.signals