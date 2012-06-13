#!/usr/bin/env python
#-*- coding:utf-8 -*-

from ledge.extensions import db


def edit_topic(topic, name, related_topics, description=None):
    """Create a edit a topic."""
    # change property
    topic.name = name
    topic.description = description

    #: set related to a topic
    origin_related_topics = set(topic.related_topics)
    new_related_topics = set(related_topics)

    #: could not be related to itself
    if topic in new_related_topics:
        new_related_topics.remove(topic)

    #: clean old related
    for removing in origin_related_topics - new_related_topics:
        topic.related_topics.remove(removing)
        removing.related_topics.remove(topic)

    #: create new related
    for creating in new_related_topics - origin_related_topics:
        topic.related_topics.append(creating)
        creating.related_topics.append(topic)

    #: store into database
    if topic not in db.session:
        db.session.add(topic)
    db.session.commit()
