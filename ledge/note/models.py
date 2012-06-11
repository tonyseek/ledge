#!/usr/bin/env python
#-*- coding:utf-8 -*-

import datetime

from sqlalchemy.ext.hybrid import hybrid_property

from ledge.extensions import db
from ledge.corelib import mixins
from ledge.account.models import User


# ---------------
# Topic Node Tree
# ---------------

class NodeClosure(db.Model):
    """The level closure of the Node."""

    parent_id = db.Column(db.ForeignKey("node.id"), primary_key=True)
    child_id = db.Column(db.ForeignKey("node.id"), primary_key=True)


class Node(db.Model):
    """The topic node."""

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Unicode(20), nullable=False)
    created = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    parents = db.relationship("Node", secondary=NodeClosure.__table__,
            primaryjoin=(NodeClosure.child_id == id),
            secondaryjoin=(NodeClosure.parent_id == id))
    children = db.relationship("Node", secondary=NodeClosure.__table__,
            primaryjoin=(NodeClosure.parent_id == id),
            secondaryjoin=(NodeClosure.child_id == id))


# ----------------
# Note and Version
# ----------------

class Note(db.Model):
    """The note."""

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Unicode(20), nullable=False)
    node_id = db.Column(db.ForeignKey(Node.id), nullable=False)
    owner_id = db.Column(db.ForeignKey(User.id), nullable=False)
    node = db.relationship(Node, lazy="joined", uselist=False,
            primaryjoin=(Node.id == node_id))
    owner = db.relationship(User, lazy="joined", uselist=False,
            primaryjoin=(User.primary_key == owner_id))
    created = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    @hybrid_property
    def latest_version(self):
        return self.versions.order_by(NoteVersion.id.desc()).first()

    @hybrid_property
    def latest_modified(self):
        return self.last_version.created


class NoteVersionQuery(db.Query):
    """The query handler of the NoteVersion."""

    pass


class NoteVersion(mixins.Commentable, db.Model):
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
