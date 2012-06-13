#!/usr/bin/env python
#-*- coding:utf-8 -*-

from flask.ext.wtf import TextField, TextAreaField, QuerySelectMultipleField
from flask.ext.wtf import SubmitField, required, length
from flask.ext.babel import lazy_gettext as _

from ledge.corelib.forms import Form, unique
from ledge.note.models import Topic


class EditTopicForm(Form):
    """The form to create or edit a topic."""

    name = TextField(_("Name"), [required(), unique(Topic, Topic.name),
            length(1, 20)])
    description = TextAreaField(_("Description"), [length(0, 200)])
    related_topics = QuerySelectMultipleField(_("Related Topics"),
            query_factory=lambda: Topic.query.all(), get_label="name")
    submit = SubmitField(_("Confirm"))
