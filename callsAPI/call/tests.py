import datetime

from django.test import TestCase

# Create your tests here.
from rest_framework.test import APITestCase

from call.models import Call


class CallAPIViewTestCase(APITestCase):
    def setUp(self):
        self.url = 'http://localhost:8000/calls/'

        self.time_start = str(datetime.datetime(2018, 8, 2, 21, 0, 0))
        self.time_end = str(datetime.datetime(2018, 8, 2, 21, 10, 0, 0))
        self.time_end_wrong = str(datetime.datetime(2018, 8, 2, 20, 50, 0))

        self.time_start_outside = str(datetime.datetime(2018, 8, 2, 21, 50, 0))
        self.time_end_inside = str(datetime.datetime(2018, 8, 2, 22, 10, 0, 0))

        self.time_start_inside = str(datetime.datetime(2018, 8, 2, 5, 50, 0))
        self.time_end_outside = str(datetime.datetime(2018, 8, 2, 6, 10, 0, 0))

        self.start_data = {"call_id": 80, "timestamp": self.time_start, "type": "start", "source": "48999990000",
                           "destination": "48999990001"}
        self.end_data = {"call_id": 80, "timestamp": self.time_end, "type": "end"}
        self.wrong_end_data = {"call_id": 80, "timestamp": self.time_end_wrong, "type": "end"}

        self.start_data_billing1 = {"call_id": 81, "timestamp": self.time_start_outside, "type": "start",
                                    "source": "48999990001", "destination": "48999990002"}
        self.end_data_billing1 = {"call_id": 81, "timestamp": self.time_end_inside, "type": "end"}

        self.start_data_billing2 = {"call_id": 82, "timestamp": self.time_start_inside, "type": "start",
                                    "source": "48999990002", "destination": "48999990003"}
        self.end_data_billing2 = {"call_id": 82, "timestamp": self.time_end_outside, "type": "end"}

    def test_insert_start(self):
        response = self.client.post(self.url, self.start_data, format='json')
        self.assertEqual(201, response.status_code)

        call = Call.objects.get(call_id=80)

        self.assertEqual(call.time_start.strftime("%Y-%m-%d %H:%M:%S"), self.time_start)
        self.assertEqual(call.source, '48999990000')
        self.assertEqual(call.destination, '48999990001')
        self.assertEqual(call.time_end, None)
        self.assertEqual(call.call_cost, None)

    def test_insert_end(self):
        response = self.client.post(self.url, self.end_data, format='json')
        self.assertEqual(201, response.status_code)

        call = Call.objects.get(call_id=80)

        self.assertEqual(call.time_start, None)
        self.assertEqual(call.source, None)
        self.assertEqual(call.destination, None)
        self.assertEqual(call.time_end.strftime("%Y-%m-%d %H:%M:%S"), self.time_end)
        self.assertEqual(call.call_cost, None)

    def test_insert_start_end(self):
        response = self.client.post(self.url, self.start_data, format='json')
        self.assertEqual(201, response.status_code)
        response = self.client.post(self.url, self.end_data, format='json')
        self.assertEqual(201, response.status_code)

        call = Call.objects.get(call_id=80)

        self.assertEqual(call.time_start.strftime("%Y-%m-%d %H:%M:%S"), self.time_start)
        self.assertEqual(call.source, '48999990000')
        self.assertEqual(call.destination, '48999990001')
        self.assertEqual(call.time_end.strftime("%Y-%m-%d %H:%M:%S"), self.time_end)
        self.assertEqual(call.call_cost, 1.26)

    def test_insert_start_end_billing1(self):
        response = self.client.post(self.url, self.start_data_billing1, format='json')
        self.assertEqual(201, response.status_code)
        response = self.client.post(self.url, self.end_data_billing1, format='json')
        self.assertEqual(201, response.status_code)

        call = Call.objects.get(call_id=81)

        self.assertEqual(call.time_start.strftime("%Y-%m-%d %H:%M:%S"), self.time_start_outside)
        self.assertEqual(call.source, '48999990001')
        self.assertEqual(call.destination, '48999990002')
        self.assertEqual(call.time_end.strftime("%Y-%m-%d %H:%M:%S"), self.time_end_inside)
        self.assertEqual(call.call_cost, 1.26)

    def test_insert_start_end_billing2(self):
        response = self.client.post(self.url, self.start_data_billing2, format='json')
        self.assertEqual(201, response.status_code)
        response = self.client.post(self.url, self.end_data_billing2, format='json')
        self.assertEqual(201, response.status_code)

        call = Call.objects.get(call_id=82)

        self.assertEqual(call.time_start.strftime("%Y-%m-%d %H:%M:%S"), self.time_start_inside)
        self.assertEqual(call.source, '48999990002')
        self.assertEqual(call.destination, '48999990003')
        self.assertEqual(call.time_end.strftime("%Y-%m-%d %H:%M:%S"), self.time_end_outside)
        self.assertEqual(call.call_cost, 1.26)

    def test_insert_end_start(self):
        response = self.client.post(self.url, self.end_data, format='json')
        self.assertEqual(201, response.status_code)
        response = self.client.post(self.url, self.start_data, format='json')
        self.assertEqual(201, response.status_code)

        call = Call.objects.get(call_id=80)

        self.assertEqual(call.time_start.strftime("%Y-%m-%d %H:%M:%S"), self.time_start)
        self.assertEqual(call.source, '48999990000')
        self.assertEqual(call.destination, '48999990001')
        self.assertEqual(call.time_end.strftime("%Y-%m-%d %H:%M:%S"), self.time_end)
        self.assertEqual(call.call_cost, 1.26)

    def test_insert_start_start(self):
        response = self.client.post(self.url, self.start_data, format='json')
        self.assertEqual(201, response.status_code)
        response = self.client.post(self.url, self.start_data, format='json')
        self.assertEqual(400, response.status_code)

    def test_insert_end_end(self):
        response = self.client.post(self.url, self.end_data, format='json')
        self.assertEqual(201, response.status_code)
        response = self.client.post(self.url, self.end_data, format='json')
        self.assertEqual(400, response.status_code)

    def test_insert_start_end_with_wrong_time(self):
        response = self.client.post(self.url, self.start_data, format='json')
        self.assertEqual(201, response.status_code)
        response = self.client.post(self.url, self.wrong_end_data, format='json')
        self.assertEqual(400, response.status_code)
