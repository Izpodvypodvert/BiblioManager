from django.db.models.signals import post_delete
from django.dispatch import receiver
from .models import BookLoan


@receiver(post_delete, sender=BookLoan)
def update_book_on_loan_delete(sender, instance, **kwargs):
    if instance.book:
        instance.book.borrowed_by = None
        instance.book.save()
