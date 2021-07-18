from django.apps import AppConfig


class CheckoutConfig(AppConfig):
    name = 'checkout'

    def ready(self):
        import checkout.signals


class CategoryAdmin(AppConfig):
    name = 'category'