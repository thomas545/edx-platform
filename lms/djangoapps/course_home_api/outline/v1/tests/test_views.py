"""
Tests for Dates Tab API in the Course Home API
"""


import ddt

from django.urls import reverse

from course_modes.models import CourseMode
from lms.djangoapps.course_home_api.tests.utils import BaseCourseHomeTests
from student.models import CourseEnrollment


@ddt.ddt
class OutlineTabTestViews(BaseCourseHomeTests):
    """
    Tests for the Outline Tab API
    """
    @classmethod
    def setUpClass(cls):
        BaseCourseHomeTests.setUpClass()
        cls.url = reverse('course-home-outline-tab', args=[cls.course.id])

    @ddt.data(CourseMode.AUDIT, CourseMode.VERIFIED)
    def test_get_authenticated_enrolled_user(self, enrollment_mode):
        CourseEnrollment.enroll(self.user, self.course.id, enrollment_mode)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

        course_tools = response.data.get('course_tools')
        if course_tools:
            self.assertTrue(course_tools)
            self.assertEquals(course_tools[0]['analytics_id'], 'edx.bookmarks')

        # TODO: what else do I currently have to include in this test... will build out more when working on the API

        # if enrollment_mode == CourseMode.AUDIT:
        #     self.assertFalse(response.data.get('learner_is_verified'))
            # self.assertTrue(any(block.get('learner_has_access') is False for block in date_blocks))
        # else:
        #     self.assertTrue(response.data.get('learner_is_verified'))
        #     self.assertTrue(all(block.get('learner_has_access') for block in date_blocks))

    def test_get_authenticated_user_not_enrolled(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.data.get('learner_is_verified'))

    def test_get_unauthenticated_user(self):
        self.client.logout()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 403)

    # TODO: How is this test returning a 200 for a course that doesn't exist...
    # maybe it's because course tools coming back empty isn't a breaking element to Outline Tab
    def test_get_unknown_course(self):
        url = reverse('course-home-outline-tab', args=['course-v1:unknown+course+2T2020'])
        response = self.client.get(url)
        print(response)
        self.assertEqual(response.status_code, 404)
