from store.signals import order_created
from django.dispatch import receiver

# used to decouple the code and make it more reusable
@receiver(order_created)
def on_order_created(sender, **kwargs):
    print(kwargs['order'])