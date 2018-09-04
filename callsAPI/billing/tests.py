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

    def test_get_billing_with_one(self):
        response = self.client.get(self.url.format(source=self.source), params={'period':'08/2018'})
        json_r = response.json()[0]

        self.assertEqual(self.time_start, json_r['time_start'])
        self.assertEqual(self.time_end, json_r['time_end'])
        self.assertEqual(self.call_id, json_r['call_id'])
        self.assertEqual(self.destination, json_r['destination'])
        self.assertEqual(self.call_cost, json_r['call_cost'])

    def test_get_billing_with_two(self):
        time_start_2 = datetime.datetime(2018, 8, 2, 22, 0, 0).strftime("%Y-%m-%dT%H:%M:%SZ")
        time_end_2 = datetime.datetime(2018, 8, 2, 22, 10, 0).strftime("%Y-%m-%dT%H:%M:%SZ")
        call_id_2 = 81
        source_2 = "48999990000"
        destination_2 = "48999990002"
        call_cost_2 = 11.0
        call_2 = Call(call_id=call_id_2, time_start=time_start_2, time_end=time_end_2, source=source_2,
                      destination=destination_2, call_cost=call_cost_2)
        call_2.save()

        response = self.client.get(self.url.format(source=self.source), params={'period':'08/2018'})
        json_r_1 = response.json()[0]
        json_r_2 = response.json()[1]

        self.assertEqual(self.time_start, json_r_1['time_start'])
        self.assertEqual(self.time_end, json_r_1['time_end'])
        self.assertEqual(self.call_id, json_r_1['call_id'])
        self.assertEqual(self.destination, json_r_1['destination'])
        self.assertEqual(self.call_cost, json_r_1['call_cost'])

        self.assertEqual(time_start_2, json_r_2['time_start'])
        self.assertEqual(time_end_2, json_r_2['time_end'])
        self.assertEqual(call_id_2, json_r_2['call_id'])
        self.assertEqual(destination_2, json_r_2['destination'])
        self.assertEqual(call_cost_2, json_r_2['call_cost'])
