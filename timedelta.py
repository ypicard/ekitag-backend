# -*- coding: utf-8 -*-
from flask_restplus.fields import Raw, MinMaxMixin, MarshallingError
from datetime import timedelta


class TimeDelta(MinMaxMixin, Raw):
    __schema_type__ = 'string'
    __schema_format__ = 'timedelta'

    def __init__(self, dt_format='iso8601', **kwargs):
        super(TimeDelta, self).__init__(**kwargs)

    def parse(self, value):
        if value is None:
            return None
        elif isinstance(value, float):
            return timedelta(seconds=float(value))
        elif isinstance(value, timedelta):
            return value
        else:
            raise ValueError('Unsupported TimeDelta format')

    def format(self, value):
        try:
            value = self.parse(value)
            return value.total_seconds()
        except (ValueError) as e:
            raise MarshallingError(e)

    def _for_schema(self, name):
        value = self.parse(self._v(name))
        return self.format(value) if value else None

    def schema(self):
        schema = super(TimeDelta, self).schema()
        schema['default'] = self._for_schema('default')
        schema['minimum'] = self._for_schema('minimum')
        schema['maximum'] = self._for_schema('maximum')
        return schema
