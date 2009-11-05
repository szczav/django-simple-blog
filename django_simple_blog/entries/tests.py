#-*- coding: utf-8 -*-
from django.core.urlresolvers import reverse
from django.test import TestCase
from django.contrib.auth.models import User

from entries.models import Category, Tag, Entry
from entries.text_parser import TextParser


class EntriesCustomViewsTests(TestCase):
    """
    Test custom views without entries in database.
    """

    def setUp(self):
        self.category = Category.objects.create(name='Test category', slug='test-category')
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
        self.category = Category.objects.create(name='Test category', slug='test-category')
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
        self.category = Category.objects.create(name='Test category', slug='test-category')
        self.tag = Tag.objects.create(name='super tag', slug='super-tag')

    def tearDown(self):
        self.category.delete()

    def test_latest_entries_feed(self):
        response = self.client.get(reverse('entries-feeds', args=['latest',]))
        self.assertEqual(response.status_code, 200)

    def test_latest_entries_by_category_feed(self):
        url = "%s/%s" % ('category', self.category.slug)
        response = self.client.get(reverse('entries-feeds', args=[url]))
        self.assertEqual(response.status_code, 200)

    def test_latest_entries_by_tag_feed(self):
        url = "%s/%s" % ('tag', self.tag.slug)
        response = self.client.get(reverse('entries-feeds', args=[url]))
        self.assertEqual(response.status_code, 200)


class TextParserTests(TestCase):
    """
    Test text parser.
    """
    _test_tags = {'b': '<strong>%(content)s</strong>',
                  'i': '<i>%(content)s</i>',
                  'url': '<a href="%(param)s">%(content)s</a>',
                  'img': '<img src="%(content)s" alt="%(param)s" />'}

    _text_with_html_tags = """\
<p>This is <b>sample</b> text.</p> It contains standard HTML tags.\
<a href='http://www.test.com'><img src='testme.png'></a>\
"""
    _text_without_html_tags = """\
This is sample text. It contains standard HTML tags.\
"""
    _text_with_tags = """\
This is [b]sample[/b] text. [b]It contains standard HTML tags.[/b]\
I hope it will [i]help[/i]. [url "http://www.wp.pl"]this is 1st link - yeah[/url]\
[img "image description"]path/to/some/img.png[/img]\
"""
    _parsed_text_with_tags = """\
This is <strong>sample</strong> text. <strong>It contains standard HTML tags.</strong>\
I hope it will <i>help</i>. <a href="http://www.wp.pl">this is 1st link - yeah</a>\
<img src="path/to/some/img.png" alt="image description" />\
"""

    _text_with_linebreaks = """\
section 1\n\n\
section 2\n\n\
section 3\nsubsection\n\
"""

    _parsed_text_with_linebreaks = """\
<p>section 1</p>\n\n\
<p>section 2</p>\n\n\
<p>section 3<br />subsection<br /></p>\
"""

    def setUp(self):
        self.parser = TextParser(self._test_tags)

    def test_remove_html_tags(self):
        output_text = self.parser.remove_html_tags(self._text_with_html_tags)
        self.assertEqual(output_text, self._text_without_html_tags)

    def test_replace_linebreaks(self):
        output_text = self.parser.replace_linebreaks(self._text_with_linebreaks)
        self.assertEqual(output_text, self._parsed_text_with_linebreaks)

    def test_parse_tags(self):
        output_text = self.parser.parse_tags(self._text_with_html_tags)
        self.assertEqual(output_text, self._text_with_html_tags)

        output_text = self.parser.parse_tags(self._text_without_html_tags)
        self.assertEqual(output_text, self._text_without_html_tags)

        output_text = self.parser.parse_tags(self._text_with_tags)
        self.assertEqual(output_text, self._parsed_text_with_tags)
