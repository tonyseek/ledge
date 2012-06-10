#!/usr/bin/env python
#-*- coding:utf-8 -*-

import flask.ext.wtf
import flask.ext.wtf.form
import wtforms.ext.i18n.form


# ---------
# Base Form
# ---------

class Form(flask.ext.wtf.Form, wtforms.ext.i18n.form.Form):
    """Mixed the secret form and the i18n form."""
    pass


def apply_monkey_patch():
    """Apply a monkey patch to the Flask-WTF extension."""
    flask.ext.wtf.form.Form = Form
    flask.ext.wtf.Form = Form


# ----------
# Validators
# ----------

def unique(column):
    """A validator to ensure the record is unique in the database."""
    model_class = column.class_

    def validate_unique(form, field):
        if model_class.query.filter(column == field.data).count() == 0:
            return True
        message = field.gettext(u"The %s has been used.") % field.label.text
        raise flask.ext.wtf.ValidationError(message)

    return validate_unique
