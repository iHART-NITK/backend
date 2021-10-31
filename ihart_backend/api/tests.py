from rest_framework.test import APITestCase
from .models import User
from django.urls import reverse

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
