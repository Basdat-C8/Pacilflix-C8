from uuid import uuid4
from django.db import models

# Create your models here.
class Tayangan(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    judul = models.CharField(max_length=100)
    sinopsis = models.CharField(max_length=255)
    asal_negara = models.CharField(max_length=50)
    sinopsis_trailer = models.CharField(max_length=255)
    url_video_trailer = models.CharField(max_length=255)
    release_date_trailer = models.DateField()
    # id_sutradara = models.ForeignKey(Sutradara, on_delete=models.CASCADE)

    class Meta:
        db_table = 'TAYANGAN'