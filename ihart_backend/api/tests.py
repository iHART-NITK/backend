from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
import datetime

from .models import Appointment, Diagnosis, Emergency, Inventory, MedicalHistory, Schedule, User, Appointment, Prescription
from django.urls import reverse

def authenticate_user(client) :
    email = "test01@nitk.edu.in"
    cid = "11111222223333344444"
    user = User.objects.create(username="test01", password="PA$$w0rD123", email=email , customer_id=cid)
    client.force_authenticate(user=user)
    token = Token.objects.create(user=user)
    client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

class ListAPITests(APITestCase):
    '''
    Test cases for the List API endpoint
    '''
    def testGetListApis(self):
        '''
        Ensure that GET requests are made successfully
        '''
        url = reverse('list-apis')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.data, list)
        print(f"\nGET Request on {url} tested successfully!")

class AuthTests(APITestCase):
    '''
    Test cases for the User class
    '''
    def testPostRegister(self):
        '''
        Ensure that POST requests are made successfully
        '''
        url = reverse('register')
        data = {
            "username": "test01",
            "password": "PA$$w0rD123",
            "email": "test01@nitk.edu.in",
            "phone": "9123456789",
            "first_name": "TestFirst",
            "middle_name": "TestMiddle",
            "last_name": "TestLast",
            "customer_id": "11111222223333344444",
            "user_type": "Stu",
            "gender": "M",
        }
        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.data, dict)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().username, "test01")
        print(f"\nPOST Request on {url} tested successfully!")

    def testPostVerifyIfRegistered(self):
        email1 = "test02@nitk.edu.in"
        email2 = "test03.191cs101@nitk.edu.in"
        cid1 = "11111222223333344444"
        cid2 = "55555666667777788888"

        user1 = User.objects.create(username="test02", password="PA$$w0rD123", email=email1 , customer_id=cid1)
        user2 = User.objects.create(username="test03", password="PA$$w0rD123", email=email2 , customer_id=cid2)

        url = reverse('verify-if-registered')
        data1 = {
            'email': email1,
            'customer_id': cid1
        }
        response1 = self.client.post(url, data1, format="json")

        self.assertEqual(response1.status_code, 200)
        self.assertIsInstance(response1.data, dict)
        self.assertTrue(response1.data["verified"])
        self.assertEqual(response1.data["id"], user1.id)
        self.assertEqual(response1.data["user_type"], "Fac")

        data2 = {
            "email": email2,
            "customer_id": cid2
        }
        response2 = self.client.post(url, data2, format="json")

        self.assertEqual(response2.status_code, 200)
        self.assertIsInstance(response2.data, dict)
        self.assertTrue(response2.data["verified"])
        self.assertEqual(response2.data["id"], user2.id)
        self.assertEqual(response2.data["user_type"], "Stu")

        data3 = {
            "email": email1,
            "customer_id": cid2
        }
        response3 = self.client.post(url, data3, format="json")

        self.assertEqual(response3.status_code, 403)
        self.assertIsInstance(response3.data, dict)
        self.assertTrue(response3.data["error"])

        print(f"\nPOST Request on {url} tested successfully!")


class EmergencyTests(APITestCase):
    '''
    Test cases for the Emergency Module
    '''
    def testGetLocations(self):
        '''
        Ensure that GET requests are made successfully
        '''
        authenticate_user(self.client)
        url = reverse('locations')
        response = self.client.get(url, format="json")

        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.data, dict)
        print(f"\nGET Request on {url} tested successfully!")

    def testGetEmergencies(self):
        '''
        Ensure that GET requests are made successfully
        '''
        authenticate_user(self.client)
        url = reverse('emergency-list')
        response = self.client.get(url, format="json")

        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.data, list)
        print(f"\nGET Request on {url} tested successfully!")

    def testPostEmergencies(self):
        '''
        Ensure that POST requests are made successfully when all data is sent
        '''
        authenticate_user(self.client)
        url = reverse('emergency-create')
        data = {
            "location": "BEA",
            "reason": "Test Reason",
            "status": "R"
        }
        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.data, dict)

        def validate_response(data):
            keys = ["reason", "location", "status"]
            expected_response = {
                "reason": "Test Reason",
                "location": "Beach Gate",
                "status": "Received"
            }
            for key in keys:
                if expected_response[key] != data[key]:
                    return False
            return True

        self.assertEqual(validate_response(response.data), True)
        self.assertEqual(Emergency.objects.count(), 1)
        print(f"\nPOST Request on {url} tested successfully!")


class MedicalHistoryTests(APITestCase):
    '''
    Test cases for the Medical History Module
    '''
    def testGetMedicalHis(self):
        '''
        Ensure that GET requests are made successfully
        '''
        authenticate_user(self.client)
        url = reverse('medical-histories')
        response = self.client.get(url, format="json")

        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.data, list)
        print(f"\nGET Request on {url} tested successfully!")


    def testPostMedical(self):
        '''
        Ensure that POST requests are made successfully when all data is sent
        '''
        authenticate_user(self.client)
        url = reverse('medical-history-create')
        data = {
            "category": "A",
            "description": "test description",
        }
        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.data, dict)

        def validate_response(data):
            keys = ["category", "description"]
            expected_response = {
                "category": "Allergies",
                "description": "test description",
            }
            for key in keys:
                if expected_response[key] != data[key]:
                    return False
            return True

        self.assertEqual(validate_response(response.data), True)
        self.assertEqual(MedicalHistory.objects.count(), 1)
        print(f"\nPOST Request on {url} tested successfully!")

class Prescriptions(APITestCase):
    '''
    Test cases for the Prescriptions Module
    '''
    def testGetAllPrescriptions(self):
        '''
        Ensure that GET requests for all prescriptions
        are made successfully
        '''
        authenticate_user(self.client)
        url = reverse('prescriptions')
        response = self.client.get(url, format="json")

        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.data, list)
        print(f"\nGET Request on {url} tested successfully!")

    def testGetAppointmentPrescriptions(self):
        '''
        Ensure that GET requests for prescriptions
        corresponding to an appointment are made successfully
        '''

        authenticate_user(self.client)
        user1 = User.objects.create(username="doctor", password="PA$$w0rD123", email='email1@email.com' , customer_id="123123123")
        user2 = User.objects.create(username="patient", password="PA$$w0rD345", email='email2@email.com' , customer_id="456456456")
        schedule1 = Schedule.objects.create(user=user1, entry_time=datetime.datetime.now().time(), exit_time=datetime.datetime.now().time(), day='Mon')
        appointment1 = Appointment.objects.create(schedule=schedule1, user=user2, date = datetime.date.today(), start_time=datetime.datetime.now().time(), status='VI')
        url = reverse('prescriptions-by-user-appointment', kwargs={'pk':user2.id, 'a_pk': appointment1.id})
        response = self.client.get(url, format="json")

        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.data, list)
        print(f"\nGET Request on {url} tested successfully!")
