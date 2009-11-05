#-*- coding: utf-8 -*-
import re


class TextParser(object):
    """
    Text parser allow to remove HTML tags from text and introduce his own
    tags format. Supported tags are stored in _valid_tags variable. Key names
    are used as tags names f.e. 'b' is [b][/b]. Values in dictionary define
    output formatting of tag. Three values can be used there:
    %(content)s - text inside [tag][/tag]
    %(tag)s - tag name
    %(param)s - tag parameter

    Normally creting object and using parse method on it should be enough
    but it is also possible to use not all methods.
    """
    _valid_tags = {'b': '<strong>%(content)s</strong>',
                   'i': '<i>%(content)s</i>',
                   'u': '<u>%(content)s</u>',
                   'code': '<pre>%(content)s</pre>',
                   'quote': '<blockquote>%(content)s</blockquote>',
                   'url': '<a href="%(param)s">%(content)s</a>',
                   'img': '<img src="%(content)s" alt="%(param)s" />'}

    def __init__(self, valid_tags=None):
        """
        Set new dictionary of tags.
        """
        if valid_tags is not None:
            self._valid_tags = valid_tags

    def parse(self, text):
        """
        Sanitize text: remove HTML tags, convert linebreaks to HTML tags and
        convert safe tags into HTML tags.
        """
        text = self.remove_html_tags(text)
        text = self.replace_linebreaks(text)
        text = self.parse_tags(text)
        return text

    def remove_html_tags(self, text):
        """
        Remove all HTML tags from text.
        """
        return re.sub(r'''<[a-zA-Z0-9/=.:;\'" ]+>''', '', text)

    def replace_linebreaks(self, text):
        text = re.sub(r'\r\n|\r|\n', '\n', text)
 	paragraphs = re.split('\n{2,}', text)
 	paragraphs = ['<p>%s</p>' % p.replace('\n', '<br />') for p in paragraphs]
 	return '\n\n'.join(paragraphs)

    def parse_tags(self, text):
        """
        Loop thru all tags in dictionary, find their usages in text and swap
        them to HTML tags according to dictionary values.
        """
        def _tag_convert(match):
            tag = match.group('tag')
            content = match.group('content')
            param = match.group('param')
            return self._valid_tags[tag] % {'content': content,
                                            'param': param}

        for tag in self._valid_tags.keys():
            tag_expr = r'''\[(?P<tag>%(tag)s)( ("|')(?P<param>[^\[^\]]*)("|'))?\](?P<content>[^\[^\]]*)\[/%(tag)s\]''' % {'tag': tag}
            text = re.sub(tag_expr, _tag_convert, text)

        return text
