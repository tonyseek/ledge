#!/usr/bin/env python
#-*- coding:utf-8 -*-

import datetime

from sqlalchemy.ext.declarative import declared_attr

from ledge.extensions import db


class BaseComment(db.Model):

    __abstract__ = True
    __commentable__ = {'owner_id': None, 'subject_id': None,
            'subject_class': None, 'owner_class': None}
    __mapper_args__ = {'order_by': "created.desc()"}

    id = db.Column(db.Integer, primary_key=True, unique=True)
    created = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    @declared_attr
    def owner_id(cls):
        owner_pk = cls.__commentable__['owner_id']
        return db.Column(db.ForeignKey(owner_pk), nullable=False)

    @declared_attr
    def subject_id(cls):
        subject_pk = cls.__commentable__['subject_id']
        return db.Column(db.ForeignKey(subject_pk), nullable=False)

    @declared_attr
    def owner(cls):
        owner_class = cls.__commentable__['owner_class']
        return db.relationship(owner_class, lazy="joined", uselist=False)

    @declared_attr
    def __tablename__(cls):
        subject_class = cls.__commentable__['subject_class']
        return "%s_comment" % subject_class.__tablename__


class Commentable(db.Model):

    __abstract__ = True
    __commentable__ = {'owner_class': None, 'owner_id': None,
            'subject_id': None}

    @declared_attr
    def comments(cls):
        #: make the meta data of the subject class
        arguments = dict(cls.__commentable__)
        arguments['subject_class'] = cls

        #: create a comment class
        class_name = "%sComment" % cls.__name__
        class_bases = (BaseComment,)
        class_members = {'__commentable__': arguments}
        comment_class = type(class_name, class_bases, class_members)
        comment_class.__doc__ = "The comment of the %s." % class_name

        #: assign the comment class to the subject class
        setattr(cls, class_name, comment_class)

        #: create and return the relationship to the comment
        return db.relationship(comment_class, lazy="dynamic",
                backref=db.backref("subject", lazy="joined", uselist=False))
