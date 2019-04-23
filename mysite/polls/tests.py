import datetime

from django.test import TestCase
from django.utils import timezone

from django.urls import reverse

from .models import Question


class QuestionModelTests(TestCase):

	def test_was_published_recently_with_future_question(self):
		"""测试将来的返回结果是否正确"""
		time = timezone.now() + datetime.timedelta(days=30)
		future_question = Question(pub_date=time)
		self.assertIs(future_question.was_published_recently(), False)

	def test_was_published_recently_with_old_question(self):
		"""测试过去返回值是否正确"""
		time = timezone.now() - datetime.timedelta(days=1, seconds=1)
		old_question = Question(pub_date=time)
		self.assertIs(old_question.was_published_recently(), False)

	def test_was_published_recently_with_recent_question(self):
		"""测试最近24小时的返回值"""
		time = timezone.now() - datetime.timedelta(hours=23, minutes=59,
												seconds=59)
		recent_question = Question(pub_date=time)
		self.assertIs(recent_question.was_published_recently(), True)


'''
针对视图的测试
'''

# 一个快捷函数用于创建投票问题
def create_question(question_text, days):
	time = timezone.now() + datetime.timedelta(days=days)
	return Question.objects.create(question_text=question_text,
								   pub_date=time)


class QuestionIndexViewTests(TestCase):

	def test_no_question(self):
		'''
		如果问题不存在，判断是否返回为No polls。。
		:return:
		'''
		response = self.client.get(reverse('polls:index'))

		# 判断返回的状态码
		self.assertEqual(response.status_code, 200)

		# 判断返回的是否是No polls..
		self.assertContains(response, "No polls are available.")

		# 判断latest_question_list是否为空
		self.assertQuerysetEqual(response.context['latest_question_list'],
								[])

	def test_past_question(self):

		# 创建一个过去的问题
		create_question(question_text="Past question.", days=-30)
		response = self.client.get(reverse('polls:index'))
		self.assertQuerysetEqual(
			response.context['latest_question_list'],
			['<Question: Past question.>']
		)

	def test_future_question(self):

		# 创建一个未来的问题
		create_question(question_text="Future question.", days=30)
		response = self.client.get(reverse("polls:index"))
		self.assertContains(response, "No polls are available.")
		self.assertQuerysetEqual(response.context['latest_question_list'],
								 [])

	def test_future_question_and_past_question(self):

		create_question(question_text="Past question.", days=-30)
		create_question(question_text="Future question.", days=30)
		response = self.client.get(reverse('polls:index'))
		self.assertQuerysetEqual(
			response.context['latest_question_list'],
			['<Question: Past question.>']
		)

	def test_two_past_question(self):

		create_question(question_text='Past question 1.', days=-30)
		create_question(question_text="Past question 2.", days=-5)
		response = self.client.get(reverse("polls:index"))
		self.assertQuerysetEqual(
			response.context["latest_question_list"],
			['<Question: Past question 2.>, <>Question: Past question 1.']
		)


class QuestionDetailViewTests(TestCase):
	def test_future_question(self):
		"""
		发布于将来的问题，应该返回为404
		:return:
		"""
		future_question = create_question(question_text='Future question.', days=5)
		url = reverse('polls:detail', args=(future_question.id))
		response = self.client.get(url)
		self.assertQuerysetEqual(response.status_code, 404)

	def test_past_question(self):

		past_question = create_question(question_text='Past question.', days=-5)
		url = reverse('polls:detail', args=(past_question.id))
		response = self.client.get(url)
		self.assertQuerysetEqual(response.status_code, past_question.question_text)