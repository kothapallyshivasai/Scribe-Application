from django.db import models

class Summary(models.Model):
    id = models.AutoField(primary_key=True)
    patient_data = models.TextField(null=False)
    summarized_text = models.TextField()
    date_time = models.DateTimeField(auto_now=True)