from django.test import TestCase
from models import *
from api import *
from django.test.client import RequestFactory
import json

TEST_USER_ID = '524156482'
TEST_ACCESS_TOKEN = 'CAAUOQD9mzrYBABdluvUoC59g4H76pNa7QBbncfrmVaoE5bqliLhGCzbrWDZBmNxIu0ZC7EaZBKMu9QT6H83uyGMx8lKDJxnGx4LtUq3bYoamtNTiZATRbCIoglSZAZAROzW8p1pf1SgSKmP6zRfPwdd3VeLZBr2AZCoEDUjJ1zvpCamYhIIECl08s6J8fyTDIdXZASMEEcFiTbQZDZD'

TEST_USER_ID_2 = '570053410'
TEST_ACCESS_TOKEN_2 = ''

TEST_ABOUT_ME = 'Hello Im demitri and this is my about me'
TEST_USER_TITLES = ['Software Engineer', 'Student', 'Designer']
TEST_USER_SKILLS = ['Python', 'JavaScript', 'HTML/CSS']

TEST_NONPROFIT = {
    'name': 'CStuy',
    'mission': 'Help underprivelaged students get CS opportunities',
    'description': ' Having dealt with the frustrations of working within the system to try to bring more opportunities to more youngsters and inspired by their alumni community, Mike, Sam, and JonAlf, have joined with Jennifer Hsu and Artie Jordan along with other members of the Stuy CS Community to form CSTUY, Computer Science and Technology for Urban Youth. An organization dedicated to bringing computer science and '
                   'technology related educational opportunities to high school and middle school students. ',
    'address': 'Manhattan, New York',
    'website': 'https://cstuy.org'
}

TEST_JOB = {
    'name': 'Event planner for fancy dinner',
    'description': 'CStuy is looking for an event planner to plan all parts '
                   'of a dinner for our annual fundraising event.',
    'compensation': '20/hr',
    'state': 'NY',
    'city': 'New York City',
    'titles': ['Event planner', 'Chef'],
    'skills': ['Event planning', 'Cooking', 'Catering']
}


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

    def createNonprofit(self):
        request = self.factory.post(
            '/createNonprofit',
            {
                'userId': TEST_USER_ID,
                'nonprofit': json.dumps(TEST_NONPROFIT)
            }
        )
        return createNonprofit(request)

    def postJob(self):
        self.createNonprofit()
        nonprofit = getUserNonprofits(self.account)[0]
        nonprofitId = str(nonprofit.pk)
        request = self.factory.post(
            '/postJobAsNonprofit',
            {
                'userId': TEST_USER_ID,
                'nonprofitId': nonprofitId,
                'jobToPost': json.dumps(TEST_JOB)
            }
        )
        return postJobAsNonprofit(request)

    def viewProfile(self):
        self.updateProfile()
        request = self.factory.post(
            '/viewOtherProfile',
            {
                'userId': str(self.account.userId)
            }
        )
        return viewOtherProfile(request)

    def viewJob(self):
        self.postJob()
        job = getNonprofitPostedJobs(Nonprofit.objects.get(
            name=TEST_NONPROFIT['name']))[0]
        request = self.factory.post(
            '/viewJob',
            {
                'jobId': str(job.pk),
                'jobType': POSTED_JOB_TYPE
            }
        )
        return viewJob(request)

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
        self.assertTrue(responseIsSuccess(response))
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

    def testCreateNonprofit(self):
        requiredFields = ['myNonprofits', 'newNonprofit']
        requiredFieldsInNewNonprofit = ['nonprofitId', 'name', 'mission',
                                        'description', 'website', 'jobs',
                                        'affiliates']
        response = self.createNonprofit()

        data = getResponseObject(response)['data']
        newNonprofit = data['newNonprofit']

        self.assertTrue(hasFields(data, requiredFields))
        self.assertTrue(
            hasFields(
                newNonprofit,
                requiredFieldsInNewNonprofit)
        )
        self.assertTrue(Nonprofit.objects.filter(name=TEST_NONPROFIT['name'])
                        .exists())
        self.assertEqual(
            newNonprofit['name'],
            TEST_NONPROFIT['name']
        )
        self.assertEqual(
            newNonprofit['mission'],
            TEST_NONPROFIT['mission'],
        )
        self.assertEqual(
            newNonprofit['description'],
            TEST_NONPROFIT['description']
        )
        self.assertEqual(
            newNonprofit['website'],
            TEST_NONPROFIT['website']
        )

    def testPostJob(self):
        requiredFields = ['nonprofitPostedJobs', 'newPostedJob']
        requiredFieldsInNewPostedJob = [
            'jobId', 'name', 'description', 'compensation', 'city', 'state',
            'titles', 'skills', 'nonprofitId', 'nonprofitName', 'timeCreated'
        ]

        response = self.postJob()
        data = getResponseObject(response)['data']
        newPostedJob = data['newPostedJob']

        self.assertTrue(responseIsSuccess(response))
        self.assertTrue(hasFields(data, requiredFields))
        self.assertTrue(hasFields(newPostedJob, requiredFieldsInNewPostedJob))
        self.assertTrue(PostedJob.objects.filter(pk=newPostedJob['jobId'])
                        .exists())

    def testViewProfile(self):
        requiredFields = ['userToView']
        requiredFieldsInUserToView = ['userId', 'name', 'aboutMe', 'titles',
                                      'skills', 'jobs', 'nonprofits',
                                      'profileImageUrl']

        response = self.viewProfile()
        data = getResponseObject(response)['data']
        userToView = data['userToView']

        self.assertTrue(responseIsSuccess(response))
        self.assertTrue(hasFields(data, requiredFields))
        self.assertTrue(hasFields(userToView, requiredFieldsInUserToView))
        self.assertEqual(
            TEST_ABOUT_ME,
            userToView['aboutMe']
        )
        self.assertEqual(
            'Demitri Nava',
            userToView['name']
        )
        self.assertEqual(
            TEST_USER_ID,
            userToView['userId']
        )
        self.assertEqual(
            len(TEST_USER_SKILLS),
            len(userToView['skills'])
        )
        self.assertEqual(
            len(TEST_USER_TITLES),
            len(userToView['titles'])
        )

    def testViewJob(self):
        requiredFields = ['jobToView']
        requiredFieldsInJobToView = ['jobId', 'nonprofitName', 'nonprofitId',
                                     'name', 'description', 'compensation',
                                     'city', 'state', 'titles', 'skills']

        response = self.viewJob()
        self.assertTrue(responseIsSuccess(response))

        data = getResponseObject(response)['data']
        jobToView = data['jobToView']

        self.assertTrue(hasFields(data, requiredFields))
        self.assertTrue(hasFields(jobToView, requiredFieldsInJobToView))
        self.assertEqual(
            TEST_JOB['name'],
            jobToView['name']
        )
        self.assertEqual(
            TEST_JOB['description'],
            jobToView['description']
        )
        self.assertEqual(
            TEST_JOB['compensation'],
            jobToView['compensation']
        )
        self.assertEqual(
            TEST_JOB['city'],
            jobToView['city']
        )
        self.assertEqual(
            TEST_JOB['state'],
            jobToView['state']
        )
        self.assertEqual(
            TEST_NONPROFIT['name'],
            jobToView['nonprofitName']
        )
        self.assertEqual(
            len(TEST_JOB['skills']),
            len(jobToView['skills'])
        )
        self.assertEqual(
            len(TEST_JOB['titles']),
            len(jobToView['titles'])
        )