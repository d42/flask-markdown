# -*- coding: utf-8 -*-
"""
flaskext.markdown
~~~~~~~~~~~~~~~~~

Markdown filter class for Flask
To use::

    from flaskext.markdown import Markdown
    md = Markdown(app)

Then in your template::

    {% filter markdown %}
    Your Markdown
    =============
    {% endfilter %}

You can also do::

    {{ mymarkdown|markdown}}


Optionally, you can keep a reference to the Markdown instance and use that
to register custom extensions by calling :func:`register_extension` or
decorating the extension class with :func:`extend`

:copyright: (c) 2013 by Dan Colish.
:license: BSD, MIT see LICENSE for more details.
"""
from __future__ import absolute_import
from flask import Markup
import bleach
from jinja2 import evalcontextfilter
import markdown as md
from markdown import (
    blockprocessors,
    Extension,
    preprocessors,
)


__all__ = ['blockprocessors', 'Extension', 'Markdown', 'preprocessors']



MARKDOWN_TAGS = ['a', 'abbr', 'acronym', 'b', 'blockquote', 'em', 'i', 'li', 'br',
                 'ol', 'strong', 'ul', 'p', 'h1', 'h2', 'h3', 'pre', 'code', 'hr', 'img']

MARKDOWN_ATTRIBUTES = bleach.ALLOWED_ATTRIBUTES.copy()
MARKDOWN_ATTRIBUTES['img'] = ['src']


class Markdown(object):
    """
    :param app: Your Flask app instance
    :param markdown_options: Keyword args for the Markdown instance
    """

    def __init__(self, app, filter_name='markdown', bleach=False,
                 bleach_attributes=None, **markdown_options):
        self._instance = md.Markdown(**markdown_options)

        self.bleach_attributes = {'tags': MARKDOWN_TAGS,
                                  'attributes': MARKDOWN_ATTRIBUTES,
                                  'strip': True}
        self.bleach = bleach
        if bleach_attributes: self.bleach_attributes.update(bleach_attributes)

        app.jinja_env.filters[filter_name] = self.markdown

    def convert(self, stream, run_bleach):
        html = self._instance.reset().convert(stream)
        if run_bleach:
            html = bleach.clean(html, **self.bleach_attributes)
        return html

    @evalcontextfilter
    def markdown(self, eval_ctx, stream):
        return Markup(self.convert(stream, run_bleach=self.bleach))
