#!/usr/bin/env python
#-*- coding:utf-8 -*-

import markdown


def markdown_to_html(raw_text):
    """Render raw markdown text to html."""
    return markdown.markdown(raw_text)


renders = {("markdown", "html"): markdown_to_html}


def render_to_html(from_format, raw_text):
    """Render a special format to html."""
    return renders[from_format, "html"](raw_text)
