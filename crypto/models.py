from django.db import models
from organizations.models import Organization


class CryptoPrice(models.Model):
    id = models.AutoField(primary_key=True)
    org = models.ForeignKey(
        Organization, on_delete=models.CASCADE, related_name="crypto_prices")
    symbol = models.CharField(max_length=10)  # e.g., "BTC", "ETH"
    price = models.DecimalField(max_digits=20, decimal_places=10)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.symbol} - {self.price} ({self.timestamp})"
