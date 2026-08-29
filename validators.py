import re

from wtforms import ValidationError


class UniqueValue:
    def __init__(self, model, column_name, message=None, current_id=None, id_column=None):
        self.model = model
        self.column_name = column_name
        self.message = message or "This value is already registered."
        self.current_id = current_id
        self.id_column = id_column

    def __call__(self, form, field):
        column = getattr(self.model, self.column_name)
        query = self.model.query.filter(column == field.data)

        if self.current_id is not None and self.id_column is not None:
            query = query.filter(getattr(self.model, self.id_column) != self.current_id)

        if query.first() is not None:
            raise ValidationError(self.message)


class SimpleEmail:
    def __init__(self, message=None):
        self.message = message or "Enter a valid email address."

    def __call__(self, form, field):
        if not re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", field.data or ""):
            raise ValidationError(self.message)


class MatchesText:
    def __init__(self, expected, message=None):
        self.expected = expected
        self.message = message or f"Enter {expected} to confirm."

    def __call__(self, form, field):
        if field.data != self.expected:
            raise ValidationError(self.message)
