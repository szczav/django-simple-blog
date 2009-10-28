#-*- coding: utf-8 -*-
from django.core.urlresolvers import reverse
from django.test import TestCase
from django.contrib.auth.models import User

from entries.models import Category, Tag, Entry


class EntriesCustomViewsTests(TestCase):
    """
    Test custom views without entries in database.
    """

    def setUp(self):
        self.category = Category.objects.create(name='Test category', slug='test-category', description='test description')
        self.tag = Tag.objects.create(name='test tag', slug='test-tag')

    def tearDown(self):
        self.category.delete()
        self.tag.delete()

    def test_category_custom_list(self):
        response = self.client.get(reverse('entries-archive-custom', args=['categories', self.category.slug, '1']))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'entries/entry_custom_list.html')
        self.assertContains(response, self.category.name)

    def test_tag_custom_list(self):
        response = self.client.get(reverse('entries-archive-custom', args=['tags', self.tag.slug, '1']))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'entries/entry_custom_list.html')
        self.assertContains(response, self.tag.name)

    def test_category_custom_list_index(self):
        response = self.client.get(reverse('entries-index-custom', args=['categories',]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'entries/entry_custom_index.html')
        self.assertContains(response, self.category.name)

    def test_tag_custom_list_index(self):
        response = self.client.get(reverse('entries-index-custom', args=['tags',]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'entries/entry_custom_index.html')
        self.assertContains(response, self.tag.name)


class ModelsTests(TestCase):
    """
    Test Category, Tag and Entry models.
    """
    def setUp(self):
        self.category = Category.objects.create(name='Test category', slug='test-category', description='test description')
        self.tag = Tag.objects.create(name='test tag', slug='test-tag')
        self.user = User.objects.create_user('Steve', 'steve@test.com', 'password')
        self.entry = Entry.objects.create(title='Entry test title', slug='entry-test-title', content='test content', author=self.user)
        self.entry.categories.add(self.category)
        self.entry.tags.add(self.tag)

    def tearDown(self):
        self.category.delete()
        self.tag.delete()
        self.entry.delete()
        self.user.delete()

    def test_unicode(self):
        self.assertEqual(self.category.__unicode__(), self.category.name)
        self.assertEqual(self.tag.__unicode__(), self.tag.name)
        self.assertEqual(self.entry.__unicode__(), self.entry.title)

    def test_absolute_url(self):
        response = self.client.get(self.category.get_absolute_url())
        self.assertEqual(response.status_code, 200)

        response = self.client.get(self.tag.get_absolute_url())
        self.assertEqual(response.status_code, 200)

        response = self.client.get(self.entry.get_absolute_url())
        self.assertEqual(response.status_code, 200)

class FeedsTests(TestCase):
    """
    Test feeds.
    """
    def setUp(self):
        self.category = Category.objects.create(name='Test category', slug='test-category', description='test description')

    def tearDown(self):
        self.category.delete()

    def test_latest_entries_feed(self):
        response = self.client.get(reverse('entries-feeds', args=['latest',]))
        self.assertEqual(response.status_code, 200)

    def test_latest_entries_by_category_feed(self):
        url = "%s/%s" % ('category', self.category.slug)
        response = self.client.get(reverse('entries-feeds', args=[url]))
        self.assertEqual(response.status_code, 200)
