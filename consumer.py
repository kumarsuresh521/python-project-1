import json
import os

import django

from kafka import KafkaConsumer

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "example.settings")
django.setup()

from django.conf import settings
from app.models import User
'''
Consumer for update retailer in microservices.
'''
def update_create_user(value):
    try:
        User.objects.update_or_create(user_id=value['id'], defaults={"firstname": value['firstname'],
        "email": value['email'], "lastname": value['lastname'], "mobile_number": value['mobile_number']
        , "user_type": value['user_type'], "is_active": value['is_active']})
    except User.DoesNotExist:
        pass

consumer = KafkaConsumer('update_retailer', bootstrap_servers=settings.HUB_EXAMPLE_USER_KAFKA_SERVER)
for data in consumer:
    value = json.loads(data.value)
    print(value)
    if data.topic == 'update_retailer':
        update_create_user(value)
consumer.flush()
