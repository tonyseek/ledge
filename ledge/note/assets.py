#!/usr/bin/env python
#-*- coding:utf-8 -*-

from flask.ext.assets import Bundle

from ledge.extensions import assets


scripts_note = Bundle("note/scripts/topic.js",
        output="packed/note.packed.js")
stylesheets_note = Bundle("note/stylesheets/topic.css",
        output="packed/note.packed.css")

assets.register('scripts.note', scripts_note)
assets.register('stylesheets.note', stylesheets_note)
