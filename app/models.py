from django.db import models
from example.core.helper import TimestampModel

# Create your models here.
class User(TimestampModel):
    SUPPLIER = 1
    RETAILER = 2
    STORE_MEMBER = 3
    ADMIN = 4

    USER_TYPE_CHOICES = (
        (SUPPLIER, 'Supplier'),
        (RETAILER, 'Retailer'),
        (STORE_MEMBER, 'Staff Member')
    )
    user_id = models.PositiveIntegerField(primary_key=True, editable=False)
    email = models.EmailField('Email Address', unique=True)
    firstname = models.CharField('First Name', max_length=30, db_index=True)
    lastname = models.CharField(
        'Last Name', max_length=30, db_index=True, null=True, blank=True)
    mobile_number = models.CharField(
        'Mobile Number', max_length=20, null=True, blank=True)
    user_type = models.SmallIntegerField(
        choices=USER_TYPE_CHOICES, default=SUPPLIER)
    def get_full_name(self):
        return '{0} {1}'.format(self.firstname, self.lastname)

    def __str__(self):
        return '{0} {1}'.format(self.firstname, self.lastname)
