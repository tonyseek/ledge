#!/usr/bin/env python
#-*- coding:utf-8 -*-

from flask.ext.wtf import (TextField, TextAreaField,
        QuerySelectMultipleField, BooleanField, SubmitField)
from flask.ext.wtf import required, length
from flask.ext.babel import lazy_gettext as _

from ledge.corelib.forms import Form, unique
from ledge.note.models import Topic, Note


class EditTopicForm(Form):
    """The form to create or edit a topic."""

    name = TextField(_("Name"), [required(), unique(Topic, Topic.name),
            length(1, 20)])
    description = TextAreaField(_("Description"), [length(0, 200)])
    related_topics = QuerySelectMultipleField(_("Related Topics"),
            query_factory=lambda: Topic.query.all(), get_label="name")
    submit = SubmitField(_("Save"))


class EditNoteForm(Form):
    """The form to create or edit a note."""

    title = TextField(_("Title"), [required(), unique(Note, Note.title),
            length(1, 20)])
    content = TextAreaField(_("Entry"), [required()])
    topics = QuerySelectMultipleField(_("Topics"), get_label="name",
            query_factory=lambda: Topic.query.all())
    is_small_changed = BooleanField(_("This is a small changed"))
    submit = SubmitField(_("Save"))
