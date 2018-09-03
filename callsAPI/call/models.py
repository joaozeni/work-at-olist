from django.db import models

# Create your models here.


class Call(models.Model):
    call_id = models.BigIntegerField(
        primary_key=True, db_column='call_id', blank=False, null=False)
    time_start = models.DateTimeField(
        blank=True, null=True, db_column='time_start')
    time_end = models.DateTimeField(
        blank=True, null=True, db_column='time_end')
    source = models.CharField(blank=True, null=True,
                              max_length=50, db_column='source')
    destination = models.CharField(
        blank=True, null=True, max_length=50, db_column='destination')

    class Meta:
        managed = True
        db_table = 'call'
