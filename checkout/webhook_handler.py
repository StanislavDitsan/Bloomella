from django.http import HttpResponse
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from .models import Order, OrderLineItem
from products.models import Product
from profiles.models import UserProfile

import stripe
import json
import time


class StripeWH_Handler:
    """Handle Stripe webhooks"""

    def __init__(self, request):
        self.request = request

    def _send_confirmation_email(self, order):
        """ Send the user a confirmation email """
        cust_email = order.email
        admin_email = settings.ORDER_NOTIFICATION_EMAIL
        subject = render_to_string(
            'checkout/confirmation_emails/confirmation_email_subject.txt',
            {'order': order})

        body = render_to_string(
            'checkout/confirmation_emails/confirmation_email_body.txt', {
                'order': order,
                'contact_email': settings.DEFAULT_FROM_EMAIL
            })

        # Send email to customer
        send_mail(subject, body, settings.DEFAULT_FROM_EMAIL, [cust_email])

        # Send email notification to store admin
        admin_subject = f'New Order Placed - Order #{order.order_number}'
        admin_body = f'A new order has been placed.\nProduct Name: {item.product.name}\nOrder Number: {order.order_number}\nCustomer: {order.full_name}\nTotal Amount: €{order.grand_total}'
        send_mail(admin_subject, admin_body, settings.DEFAULT_FROM_EMAIL, [admin_email])

    def handle_event(self, event):
        """
        Handle a generic/unknown/unexpected webhook event
        """
        logger.info(f'Received webhook event: {event["type"]}')
        return HttpResponse(
            content=f'Unhandled webhook received: {event["type"]}', status=200)

    def handle_payment_intent_succeeded(self, event):
        """
        Handle the payment_intent.succeeded webhook from Stripe
        """
        try:
            intent = event.data.object
            pid = intent.id
            bag = intent.metadata.bag
            save_info = intent.metadata.save_info

            stripe_charge = stripe.Charge.retrieve(intent.latest_charge)

            billing_details = stripe_charge.billing_details
            shipping_details = intent.shipping
            grand_total = round(stripe_charge.amount / 100, 2)

            for field, value in shipping_details.address.items():
                if value == "":
                    shipping_details.address[field] = None

            profile = None
            username = intent.metadata.username
            if username != 'AnonymousUser':
                profile = UserProfile.objects.get(user__username=username)
                if save_info:
                    profile.default_full_name = shipping_details.name
                    profile.default_phone_number = shipping_details.phone
                    profile.default_country = shipping_details.address.country
                    profile.default_postcode = shipping_details.address.postal_code
                    profile.default_town_or_city = shipping_details.address.city
                    profile.default_street_address1 = shipping_details.address.line1
                    profile.default_street_address2 = shipping_details.address.line2
                    profile.default_county = shipping_details.address.state
                    profile.save()

            order_exists = False
            attempt = 1
            while attempt <= 5:
                try:
                    order = Order.objects.get(
                        full_name__iexact=shipping_details.name,
                        email__iexact=billing_details.email,
                        phone_number__iexact=shipping_details.phone,
                        country__iexact=shipping_details.address.country,
                        postcode__iexact=shipping_details.address.postal_code,
                        town_or_city__iexact=shipping_details.address.city,
                        street_address1__iexact=shipping_details.address.line1,
                        street_address2__iexact=shipping_details.address.line2,
                        county__iexact=shipping_details.address.state,
                        grand_total=grand_total,
                        original_bag=bag,
                        stripe_pid=pid,
                    )
                    order_exists = True
                    break
                except Order.DoesNotExist:
                    attempt += 1
                    time.sleep(1)

            if order_exists:
                self._send_confirmation_email(order)
                return HttpResponse(content=f'Webhook received: {event["type"]} \
                    | SUCCESS: Verified order already in the database',
                                    status=200)
            else:
                order = None
                try:
                    order = Order.objects.create(
                        full_name=shipping_details.name,
                        email=billing_details.email,
                        phone_number=shipping_details.phone,
                        country=shipping_details.address.country,
                        postcode=shipping_details.address.postal_code,
                        town_or_city=shipping_details.address.city,
                        street_address1=shipping_details.address.line1,
                        street_address2=shipping_details.address.line2,
                        county=shipping_details.address.state,
                        original_bag=bag,
                        stripe_pid=pid,
                    )

                    for item_id, item_data in json.loads(bag).items():
                        product = Product.objects.get(id=item_id)
                        if isinstance(item_data, int):
                            order_line_item = OrderLineItem(
                                order=order,
                                product=product,
                                quantity=item_data,
                            )
                            order_line_item.save()
                        else:
                            for size, quantity in item_data['items_by_size'].items():
                                order_line_item = OrderLineItem(
                                    order=order,
                                    product=product,
                                    quantity=quantity,
                                    product_size=size,
                                )
                                order_line_item.save()
                except Exception as e:
                    if order:
                        order.delete()
                    logger.error(f'Error handling {event["type"]} webhook: {e}')
                    return HttpResponse(
                        content=f'Webhook received: {event["type"]} | ERROR: {e}',
                        status=500)
            self._send_confirmation_email(order)
            return HttpResponse(content=f'Webhook received: {event["type"]} \
                | SUCCESS: Created order in webhook',
                                status=200)

        except Exception as e:
            logger.error(f'Error handling {event["type"]} webhook: {e}')
            return HttpResponse(
                content=f'Webhook received: {event["type"]} | ERROR: {e}',
                status=500)

    def handle_payment_intent_payment_failed(self, event):
        """
        Handle the payment_intent.payment_failed webhook from Stripe
        """
        logger.warning(f'Payment failed webhook received: {event["type"]}')
        return HttpResponse(content=f'Webhook received: {event["type"]}',
                            status=200)
