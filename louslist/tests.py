from django.test import TestCase
from django.urls import reverse, resolve
from django.test import Client
from django.contrib.auth.models import User
from .models import Dept, Subject, CourseRating, Rating, Schedule, Event
from django.db.utils import IntegrityError
# Create your tests here.


class UrlTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.client.login(username='testuser', password='12345')
        Schedule.objects.create(user=self.user)
        
    def test_blank_url(self):
        response = self.client.get('')
        self.assertEqual(response.status_code, 200)
        
    def test_home_url(self):
        response = self.client.get("/home/")
        self.assertEqual(response.status_code, 200)
        
    def test_schedule_url(self):
        response = self.client.get('/schedule/')
        self.assertEqual(response.status_code, 200)
        
    def test_friend_schedule_url(self):
        response = self.client.get(f'/schedule/{self.user.username}/')
        self.assertEqual(response.status_code, 200)
        
    def test_friends_url(self):
        response = self.client.get('/friends/')
        self.assertEqual(response.status_code, 200)
    
    def test_friend_request_url(self):
        response = self.client.get('/friends/request')
        self.assertEqual(response.status_code, 200)
    
    def test_courses_url(self):
        response = self.client.get('/courses/')
        self.assertEqual(response.status_code, 200)
        
    def test_courses_dept_url(self):
        for dept in Dept.objects.all():
            response = self.client.get(f'/courses/{dept.dept_url_shorthand}')
            self.assertEqual(response.status_code, 200)
        
    def test_search_url(self):
        response = self.client.get('/search/')
        self.assertEqual(response.status_code, 200)
        
    

class SearchModelTests(TestCase):
    """
    def test_search_works(self):
        c = Client()
        # try to send a blank request to test logic behind loading screen that says "try searching for something else"
        # response = c.post('/search/', {'mnemonic':'BAD', 'course_num':'0000'}, content_type='application/json')
        response.content
    """

class DeptModelTests(TestCase):
    def setUp(self):
        Dept.objects.create(dept_name="Math", dept_url_shorthand="math")
        Dept.objects.create(dept_name="Biology", dept_url_shorthand="biol")
        Subject.objects.create(dept_name=Dept.objects.get(dept_name="Biology"), mnemonic="BIOL", subj_name="Biology")
        Subject.objects.create(dept_name=Dept.objects.get(dept_name="Biology"), mnemonic="HBIO", subj_name="Human Biology")

    def test_str_is_equal_to_name(self):
        sample_dept = Dept.objects.get(dept_name="Math")
        self.assertEqual(str(sample_dept), sample_dept.dept_name)
        
    def test_get_related_subjects(self):
        sample_dept = Dept.objects.get(dept_name="Biology")
        expected = [Subject.objects.get(mnemonic="BIOL"), Subject.objects.get(mnemonic="HBIO")]
        self.assertQuerysetEqual(expected, sample_dept.subject_set.all())
        
    def tearDown(self):
        Subject.objects.get(dept_name=Dept.objects.get(dept_name="Biology"), mnemonic="BIOL", subj_name="Biology").delete()
        Subject.objects.get(dept_name=Dept.objects.get(dept_name="Biology"), mnemonic="HBIO", subj_name="Human Biology").delete()
        Dept.objects.get(dept_name="Math", dept_url_shorthand="math").delete()
        Dept.objects.get(dept_name="Biology", dept_url_shorthand="biol").delete()

class SubjectModelTests(TestCase):
    def setUp(self):
        Dept.objects.create(dept_name="Math", dept_url_shorthand="math")
        Subject.objects.create(dept_name=Dept.objects.get(dept_name="Math"), mnemonic="MATH", subj_name="Mathematics")
       
    def test_str_is_equal_to_subj_name(self):
        sample_subj = Subject.objects.get(mnemonic="MATH")
        self.assertEqual(str(sample_subj), sample_subj.subj_name)
        
    def tearDown(self):
        Subject.objects.get(dept_name=Dept.objects.get(dept_name="Math"), mnemonic="MATH", subj_name="Mathematics").delete()
        Dept.objects.get(dept_name="Math", dept_url_shorthand="math").delete()
        
        
class CourseRatingTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.client.login(username='testuser', password='12345')
        CourseRating.objects.create(course_num=15991)
        CourseRating.objects.create(course_num=19660)
        Rating.objects.create(user=self.user, course=CourseRating.objects.get(course_num=19660), rating=1)
        
    def test_average_rating_no_ratings(self):
        sample_cr = CourseRating.objects.get(course_num=15991)
        self.assertEqual(float(str(sample_cr)), sample_cr.average_rating())
        
    def test_average_rating_with_ratings(self):
        sample_cr = CourseRating.objects.get(course_num=19660)
        self.assertEqual(float(str(sample_cr)), sample_cr.average_rating())
        
    def tearDown(self):
        Rating.objects.get(user=self.user, course=CourseRating.objects.get(course_num=19660), rating=1).delete()
        CourseRating.objects.get(course_num=19660).delete()
        CourseRating.objects.get(course_num=15991).delete()
        self.client.logout()
        
        