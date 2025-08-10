from django.db import models
from django.contrib.auth.models import User
import hashlib
import json

class UserProfile(models.Model):
    ROLE_CHOICES = (('producer', 'Producer'), ('consumer', 'Consumer'))
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='consumer')
    energy_tokens = models.FloatField(default=0.0)

    def __str__(self):
        return f"{self.user.username} ({self.role})"

class EnergyTransaction(models.Model):
    sender = models.ForeignKey(User, related_name='energy_sent', on_delete=models.SET_NULL, null=True, blank=True)
    receiver = models.ForeignKey(User, related_name='energy_received', on_delete=models.SET_NULL, null=True)
    energy_kwh = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender} → {self.receiver} : {self.energy_kwh} kWh"

class BlockchainBlock(models.Model):
    index = models.IntegerField()
    transaction = models.OneToOneField(EnergyTransaction, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    previous_hash = models.CharField(max_length=128)
    hash = models.CharField(max_length=128)

    def compute_hash(self):
        block_string = json.dumps({
            "index": self.index,
            "sender": self.transaction.sender.id if self.transaction.sender else None,
            "receiver": self.transaction.receiver.id,
            "energy": self.transaction.energy_kwh,
            "timestamp": self.timestamp.isoformat(),
            "previous_hash": self.previous_hash,
        }, sort_keys=True).encode()

        return hashlib.sha256(block_string).hexdigest()
