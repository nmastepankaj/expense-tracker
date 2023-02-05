from datetime import datetime
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.
class Expense(models.Model):
    """A class containing all the important info about an expense."""

    
    owner = models.ForeignKey(
        User, null=True, blank=True, on_delete=models.CASCADE
    )
    cost = models.DecimalField(
        max_digits=9, decimal_places=2
    )
    note = models.CharField(
        max_length=500, null=False, blank=False, unique=False
    )
    transaction_date = models.DateTimeField(
        default=datetime.now(), blank=False
    )

    def __str__(self) -> str:
        """Return the string representation of the Expense object."""
        if self.note != "":
            return self.note
        return f"Expense({self.id})"
