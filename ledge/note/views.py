#!/usr/bin/env python
#-*- coding:utf-8 -*-

from flask import render_template, redirect, url_for

from ledge.corelib.views import as_view, MethodView
from ledge.note import app
from ledge.note.forms import EditTopicForm
from ledge.note.models import Topic
from ledge.note.services import edit_topic


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
