from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Product
from .documents import ProductDocument


@receiver(post_save, sender=Product)
def update_product_document(sender, instance=None, created=False, **kwargs):
    """Update the product document in Elasticsearch when a product is saved."""
    try:
        ProductDocument().update(instance)
    except Exception as e:
        print(f"Elasticsearch update error: {e}")


@receiver(post_delete, sender=Product)
def delete_product_document(sender, instance=None, **kwargs):
    """Delete the product document from Elasticsearch when a product is deleted."""
    try:
        ProductDocument().delete(instance)
    except Exception as e:
        print(f"Elasticsearch delete error: {e}")
