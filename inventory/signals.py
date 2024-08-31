# inventory/signals.py
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Discount, DiscountHistory, PriceHistory, InventoryTransaction, ProductVariant

@receiver(post_save, sender=Discount)
def create_discount_history(sender, instance, created, **kwargs):
    """
    Signal to create a DiscountHistory entry whenever a Discount is created or updated.
    """
    if not created:
        # Only log changes for updates
        old_instance = Discount.objects.get(pk=instance.pk)
        if (instance.discount_type != old_instance.discount_type or
            instance.discount_value != old_instance.discount_value):
            DiscountHistory.objects.create(
                discount=instance,
                old_discount_type=old_instance.discount_type,
                old_discount_value=old_instance.discount_value,
                new_discount_type=instance.discount_type,
                new_discount_value=instance.discount_value
            )

@receiver(post_save, sender=PriceHistory)
def update_product_variant_price(sender, instance, **kwargs):
    """
    Signal to update the ProductVariant's price when a PriceHistory entry is created.
    """
    product_variant = instance.product_variant
    # Update the product variant price to the new price
    product_variant.price = instance.new_price
    product_variant.save()

@receiver(post_save, sender=InventoryTransaction)
def update_inventory_on_transaction(sender, instance, **kwargs):
    """
    Signal to update ProductVariant stock quantity based on InventoryTransaction.
    """
    product_variant = instance.product_variant
    if instance.transaction_type == 'IN':
        product_variant.stock_quantity += instance.quantity
    elif instance.transaction_type == 'OUT':
        product_variant.stock_quantity -= instance.quantity
    product_variant.save()

# Optional: Clean up associated objects if necessary (e.g., on delete of the parent object)
@receiver(post_delete, sender=Discount)
def delete_discount_history(sender, instance, **kwargs):
    """
    Signal to delete related DiscountHistory entries when a Discount is deleted.
    """
    DiscountHistory.objects.filter(discount=instance).delete()


@receiver(post_save, sender=ProductVariant)
def create_price_history(sender, instance, **kwargs):
    """
    Signal to create a PriceHistory entry whenever a ProductVariant's price is updated.
    """
    if kwargs.get('created', False):
        # Do not create PriceHistory for newly created ProductVariants
        return

    # Fetch the old price from the database
    old_instance = ProductVariant.objects.get(pk=instance.pk)

    # Check if the price has changed
    if old_instance.price != instance.price:
        PriceHistory.objects.create(
            product_variant=instance,
            old_price=old_instance.price,
            new_price=instance.price
        )