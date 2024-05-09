from django.db import models

# Create your models here.
class VendorModel(models.Model):
    name = models.CharField(max_length=256)
    contact_details = models.TextField()
    address = models.TextField()
    vendor_code = models.CharField(max_length=256)
    on_time_delivery_rate = models.FloatField(null=True)
    quality_rating_avg = models.FloatField(null=True)
    average_response_time = models.FloatField(null=True)
    fulfillment_rate = models.FloatField(null=True)

class PurchaseOrderModel(models.Model):
    po_number = models.CharField(max_length=256)
    vendor = models.ForeignKey(VendorModel, on_delete=models.CASCADE)
    order_date = models.DateTimeField()
    delivery_date = models.DateTimeField()
    items = models.JSONField()
    quantity = models.IntegerField()
    status = models.CharField(max_length=256, default='pending')
    quality_rating = models.FloatField(null=True)
    issue_date = models.DateTimeField(null=True)
    acknowledgement_date = models.DateTimeField(null=True)
    delivered_late = models.BooleanField(null=True)

class PerformanceHistory(models.Model):
    vendor = models.ForeignKey(VendorModel, on_delete=models.CASCADE)
    date = models.DateTimeField()
    on_time_delivery_rate = models.FloatField(null=True)
    quality_rating_avg = models.FloatField(null=True)
    average_response_time = models.FloatField(null=True)
    fulfillment_rate = models.FloatField(null=True)