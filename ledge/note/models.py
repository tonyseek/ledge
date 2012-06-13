#!/usr/bin/env python
#-*- coding:utf-8 -*-

import datetime

from sqlalchemy.ext.hybrid import hybrid_property

from ledge.extensions import db
from ledge.corelib.mixins.comment import Commentable
from ledge.corelib.mixins.jsonize import Jsonizable
from ledge.corelib.utils import format
from ledge.account.models import User


# ----------------
# Topic Topic Tree
# ----------------

class TopicRelated(db.Model):
    """The relation closure of the Topic."""

    topic_id = db.Column(db.ForeignKey("topic.id"), primary_key=True)
    related_id = db.Column(db.ForeignKey("topic.id"), primary_key=True)


class Topic(Jsonizable, db.Model):
    """The topic Topic."""

    JSONIZE_ATTRS = ("id", "name", "created")

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Unicode(20), nullable=False)
    description = db.Column(db.Unicode(200))
    created = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    related_topics = db.relationship("Topic",
            primaryjoin=(TopicRelated.related_id == id),
            secondary=TopicRelated.__table__,
            secondaryjoin=(TopicRelated.topic_id == id))


# ----------------
# Note and Version
# ----------------

class Note(db.Model):
    """The note."""

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Unicode(20), nullable=False)
    Topic_id = db.Column(db.ForeignKey(Topic.id), nullable=False)
    owner_id = db.Column(db.ForeignKey(User.id), nullable=False)
    Topic = db.relationship(Topic, lazy="joined", uselist=False,
            primaryjoin=(Topic.id == Topic_id))
    owner = db.relationship(User, lazy="joined", uselist=False,
            primaryjoin=(User.primary_key == owner_id))
    created = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    @hybrid_property
    def latest_version(self):
        return self.versions.order_by(NoteVersion.id.desc()).first()

    @hybrid_property
    def latest_modified(self):
        return self.last_version.created

    def get_version(self, hex_id):
        """Get a special version by it's hex-style created datetime."""
        try:
            created = format.timestamp_to_datetime(hex_id, from_hex=True)
        except ValueError:
            return None
        return self.versions.filter_by(note=self, created=created).one()


class NoteVersion(Commentable, db.Model):
    """The version of the note."""

    id = db.Column(db.Integer, primary_key=True)
    note_id = db.Column(db.ForeignKey(Note.id), nullable=False)
    note = db.relationship(Note, lazy="joined", uselist=False,
            backref=db.backref("versions", lazy="dynamic"))
    created = db.Column(db.DateTime, default=datetime.datetime.utcnow,
            nullable=False)

    __mapper_args__ = {'order_by': created.desc()}
    __commentable__ = {'owner_class': User, 'owner_id': User.primary_key,
            'subject_id': id}

    @property
    def hex_id(self):
        return format.datetime_to_timestamp(self.created)
