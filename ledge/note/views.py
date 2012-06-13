#!/usr/bin/env python
#-*- coding:utf-8 -*-

from flask import render_template, redirect, url_for

from ledge.corelib.views import as_view, MethodView
from ledge.corelib.utils import render as render_utils
from ledge.note import app
from ledge.note.forms import EditTopicForm, EditNoteForm
from ledge.note.models import Topic, Note
from ledge.note.services import edit_topic, edit_note


@app.context_processor
def context_processor():
    """Assign some utils function to template."""
    return {'render_to_html': render_utils.render_to_html}


@app.route("/topic/new")
@as_view(name="new_topic")
class NewTopicView(MethodView):
    """The view to create a new topic."""

    def prepare(self):
        self.form = EditTopicForm()

    def get(self):
        return render_template("edit-topic.html", **vars(self))

    def post(self):
        if not self.form.validate():
            return self.get()
        topic = Topic()
        edit_topic(topic, name=self.form.name.data,
                related_topics=self.form.related_topics.data,
                description=self.form.description.data)
        return redirect(url_for("note.topic", id=topic.id))


@app.route("/topic/<int:id>/edit")
@as_view(name="edit_topic")
class EditTopicView(MethodView):

    def prepare(self, id):
        self.topic = Topic.query.get_or_404(id)
        self.form = EditTopicForm(obj=self.topic)

    def get(self):
        return render_template("edit-topic.html", **vars(self))

    def post(self):
        if not self.form.validate():
            return self.get()
        edit_topic(self.topic, name=self.form.name.data,
                related_topics=self.form.related_topics.data,
                description=self.form.description.data)
        return redirect(url_for("note.topic", id=self.topic.id))


@app.route("/topic/<int:id>")
def topic(id):
    return render_template("topic.html", topic=Topic.query.get_or_404(id))


@app.route("/note/new")
@as_view(name="new_note")
class NewNoteView(MethodView):

    def prepare(self):
        self.form = EditNoteForm()

    def get(self):
        return render_template("edit-note.html", **vars(self))

    def post(self):
        if not self.form.validate():
            return self.get()
        note = Note()
        edit_note(note, title=self.form.title.data,
                topics=self.form.topics.data,
                content=self.form.content.data,
                is_small_changed=self.form.is_small_changed.data)
        return redirect(url_for("note.note", id=note.id))


@app.route("/note/<int:id>/edit")
@as_view(name="edit_note")
class EditNoteView(MethodView):

    def prepare(self, id):
        self.note = Note.query.get_or_404(id)
        self.form = EditNoteForm(obj=self.note)

    def get(self):
        self.form.content.data = self.note.latest_version.content
        return render_template("edit-note.html", **vars(self))

    def post(self):
        if not self.form.validate():
            return self.get()
        edit_note(self.note, title=self.form.title.data,
                topics=self.form.topics.data,
                content=self.form.content.data,
                is_small_changed=self.form.is_small_changed.data)
        return redirect(url_for("note.note", id=self.note.id))


@app.route("/note/<int:id>/version/<string:hex_id>")
@app.route("/note/<int:id>")
def note(id, hex_id=None):
    _note = Note.query.get_or_404(id)
    _version = _note.get_version(hex_id) if hex_id else _note.latest_version
    return render_template("note.html", note=_note, version=_version)
