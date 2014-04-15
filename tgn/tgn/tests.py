from django.test import TestCase
from models import *
from api import *
from django.test.client import RequestFactory
import json

TEST_USER_ID = '524156482'
TEST_ACCESS_TOKEN = 'CAAUOQD9mzrYBADbSyFj1V87GLJ45C1dojSjWNZBCe81a8lPhASqDLlSZBoAfR5Hw3Q5qSDBSLu9wAZCWNgo6yLje7P91F28BMRDwjIamZAv4mgKZBtKZA06LsiwmNOIyeMOsgnfCM8q9krpkSZCD9xvZCZCZBPZCkJ3994GfcKPw5vterHq8LGDZCtdAVYrE8qDkdS3Wcd0V7vflywZDZD'

TEST_USER_ID_2 = '570053410'
TEST_ACCESS_TOKEN_2 = ''

TEST_ABOUT_ME = 'Hello Im demitri and this is my about me'
TEST_USER_TITLES = ['Software Engineer', 'Student', 'Designer']
TEST_USER_SKILLS = ['Python', 'JavaScript', 'HTML/CSS']


def responseIsSuccess(response):
    obj = getResponseObject(response)
    return not obj['isError']


def getResponseObject(response):
    lenToRemove = len('Content-Type: application/json')
    obj = str(response)[lenToRemove:]
    return json.loads(obj)


def hasFields(data, fields):
    missingFields = []
    for field in fields:
        if not field in data:
            missingFields.append(field)

    return True if not missingFields else missingFields


class testAllRequests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.loginWithFacebook()
        self.account = Account.objects.get(userId=TEST_USER_ID)

    def tearDown(self):
        pass

    def loginWithFacebook(self):
        request = self.factory.post(
            '/loginWithFacebook',
            {
                'accessToken': TEST_ACCESS_TOKEN,
            }
        )
        return loginWithFacebook(request)

    def updateProfile(self):
        request = self.factory.post(
            '/updateProfile',
            {
                'userId': TEST_USER_ID,
                'profile': json.dumps({
                    'aboutMe': TEST_ABOUT_ME,
                    'titles': TEST_USER_TITLES,
                    'skills': TEST_USER_SKILLS
                })
            }
        )
        return updateProfile(request)

    def testLoginWithFacebook(self):
        requiredFields = ['me']
        requiredFieldsInMe = ['userId', 'name', 'titles', 'aboutMe',
                              'skills', 'jobs', 'nonprofits',
                              'profileImageUrl']
        response = self.loginWithFacebook()
        data = getResponseObject(response)['data']

        self.assertTrue(hasFields(data, requiredFields))
        self.assertTrue(hasFields(data['me'], requiredFieldsInMe))
        self.assertTrue(Account.objects.filter(userId=TEST_USER_ID).exists())
        self.assertTrue(responseIsSuccess(response))

    def testUpdateProfile(self):
        requiredFields = ['aboutMe', 'titles', 'skills']
        response = self.updateProfile()
        data = getResponseObject(response)['data']
        account = Account.objects.get(userId=TEST_USER_ID)
        self.assertTrue(hasFields(data, requiredFields))
        self.assertEqual(
            len(TEST_USER_SKILLS),
            len(getUserSkills(account))
        )
        self.assertEqual(
            len(TEST_USER_TITLES),
            len(getUserTitles(account))
        )
        self.assertEqual(
            TEST_ABOUT_ME,
            str(account.aboutMe)
        )