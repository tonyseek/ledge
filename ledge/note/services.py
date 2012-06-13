#!/usr/bin/env python
#-*- coding:utf-8 -*-

from ledge.extensions import db
from ledge.account.context import current_user, authenticated
from ledge.note.models import NoteVersion


@authenticated
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


@authenticated
def edit_note(note, title, topics, content, is_small_changed=False):
    """Create or edit a note."""
    #: register to the database session
    if note not in db.session:
        db.session.add(note)

    #: assign the note property
    note.title = title
    note.owner = current_user()

    origin_topics = set(note.topics)
    new_topics = set(topics)

    #: clean old topics
    for removing in origin_topics - new_topics:
        note.topics.remove(removing)

    #: create new topics
    for creating in new_topics - origin_topics:
        note.topics.append(creating)

    #: assign the content
    if is_small_changed and hasattr(note, "latest_version"):
        note.latest_version.content = content
    else:
        note.versions.append(NoteVersion(content=content))

    #: store into database
    db.session.commit()
