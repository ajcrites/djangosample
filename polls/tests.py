import datetime

from django.utils import timezone
from django.test import TestCase

from polls.models import Poll

from django.core.urlresolvers import reverse

def create_poll(question, days):
    return Poll.objects.create(question=question, pub_date=timezone.now() + datetime.timedelta(days=days))

class PollViewTests(TestCase):
    def test_index_view_with_no_polls(self):
        response = self.client.get(reverse("polls:index"))
        self.assertEqual(response.status_code, 20)
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context["latest_poll_list"], [])

class PollMethodTests(TestCase):
    def test_was_published_recently_with_future_poll(self):
        future_poll = Poll(pub_date=timezone.now() + datetime.timedelta(days=30))
        self.assertEqual(future_poll.was_published_recently(), False)

    def test_was_published_recently_with_old_poll(self):
        old_poll = Poll(pub_date=timezone.now() - datetime.timedelta(days=30))
        self.assertEqual(old_poll.was_published_recently(), False)

    def test_was_published_recently_with_recent_poll(self):
        recent_poll = Poll(pub_date=timezone.now() - datetime.timedelta(hours=1))
        self.assertEqual(recent_poll.was_published_recently(), True)
