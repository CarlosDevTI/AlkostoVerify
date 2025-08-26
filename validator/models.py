from django.db import models

class ValidationRecord(models.Model):
    cedula = models.CharField(max_length=20)
    fecha_expedicion = models.CharField(max_length=10, null=True, blank=True)
    user_answers = models.JSONField(null=True, blank=True)
    validation_success = models.BooleanField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    user_info = models.JSONField(null=True, blank=True)

    def __str__(self):
        return f"Validation for {self.cedula} at {self.timestamp}"