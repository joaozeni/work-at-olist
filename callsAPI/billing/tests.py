import datetime

from django.test import TestCase

# Create your tests here.
from rest_framework.test import APITestCase

from call.models import Call

class BillingViewTestCase(APITestCase):
    def setUp(self):
        self.url = 'http://localhost:8000/billing/{source}/'
        self.time_start = datetime.datetime(2018, 8, 2, 21, 0, 0).strftime("%Y-%m-%dT%H:%M:%SZ")
        self.time_end = datetime.datetime(2018, 8, 2, 21, 10, 0).strftime("%Y-%m-%dT%H:%M:%SZ")
        self.call_id = 80
        self.source = "48999990000"
        self.destination = "48999990001"
        self.call_cost = 10.0
        call = Call(call_id=self.call_id, time_start=self.time_start, time_end=self.time_end, source=self.source,
                    destination=self.destination, call_cost=self.call_cost)
        call.save()

    def test_get_billing(self):
        response = self.client.get(self.url.format(source=self.source), params={'period':'08/2018'})
        json_r = response.json()[0]

        self.assertEqual(self.time_start, json_r['time_start'])
        self.assertEqual(self.time_end, json_r['time_end'])
        self.assertEqual(self.call_id, json_r['call_id'])
        self.assertEqual(self.destination, json_r['destination'])
        self.assertEqual(self.call_cost, json_r['call_cost'])
