from django.contrib.auth.models import User
from django.db import models
from django.conf import settings

# Create your models here.
class P_S_Info(models.Model):
    ENTRY_CHOICES = [
        ('purchase', 'Purchase'),
        ('stock_Movement', 'Stock Movement'),
    ]
    
    SorP = models.CharField(
        max_length=50,  # Adjust the max length based on your needs
        choices=ENTRY_CHOICES,  # Set the choices option to restrict the field to these options
    )
    date=models.DateField()
    mr_mh_no=models.CharField(max_length=30)
    item=models.CharField(max_length=30)
    unit_of_measure=models.CharField(max_length=30)
    quantity=models.IntegerField()
    supplier_name=models.CharField(max_length=30)
    project_no=models.CharField(max_length=30)
    invoice_no=models.CharField(max_length=30)

    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.item
    
    @staticmethod
    def get_available_stock(item_name, user):
        """
        Calculate available stock for the given item and user.
        """
        # Total purchased by the user
        purchase_quantity = (
            P_S_Info.objects.filter(item=item_name, SorP='purchase', created_by=user)
            .aggregate(total=models.Sum('quantity'))['total'] or 0
        )
        
        # Total moved by the user
        stock_movement_quantity = (
            P_S_Info.objects.filter(item=item_name, SorP='stock_movement', created_by=user)
            .aggregate(total=models.Sum('quantity'))['total'] or 0
        )

        # Available stock = total purchases - total movements
        return purchase_quantity - stock_movement_quantity




