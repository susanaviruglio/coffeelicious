from django.http import HttpResponse


class StripeWH_Handler:
    """Handle Stripe webhooks"""

    def __init__(self, request):
        # the init method is called everytime an instance of a class is created
        self.request = request

    def handle_event(self, event):
        """
        It take the event that it has been sent and return a HTTP response
        """
        return HttpResponse(
            content=f'Webhook received: {event["type"]}',
            status=200)