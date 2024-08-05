import uuid

from sqlalchemy import func
from sqlalchemy import UniqueConstraint, Index

from app import db
from app import hashids


def _gen_xid(context):
    return hashids.encode_hex(uuid.uuid4().hex)


class _Model(object):
    def __init__(self, column_list):
        self.column_list = column_list

    def to_dict(self):
        return_dict = {}
        for column in self.column_list:
            return_dict[column] = getattr(self, column)
        return return_dict


class BaseDBMixin(object):

    id = db.Column('id', db.Integer, primary_key=True)
    xid = db.Column(db.String(255), default=_gen_xid, nullable=False)

    created = db.Column(db.TIMESTAMP, server_default=func.now())
    removed_at = db.Column(db.TIMESTAMP)
    updated = db.Column(db.TIMESTAMP, server_default=func.now(), onupdate=func.current_timestamp())

    __json_cols__ = None
    __json_full_cols__ = None

    def to_json(self, full=False):
        pack = {}

        basic_cols = self.__json_cols__
        full_cols = self.__json_full_cols__
        if not basic_cols and not full_cols:
            raise ValueError("Cannot call `to_json()` without defining basic or full json columns")

        cols = full_cols if full and full_cols else basic_cols

        for col in cols:
            pack[col] = getattr(self, col)
        return pack

    def to_model(self):
        column_list = self.__json_full_cols__
        model = _Model(column_list)
        for col in column_list:
            setattr(model, col, getattr(self, col))
        return model

    @classmethod
    def gen_indexes(cls, table_name):
        args = []
        args.extend([UniqueConstraint('xid')])
        return tuple(args)


class OrganizationMembershipBaseMixin(BaseDBMixin):

    organization_xid = db.Column(db.String(255))

    @classmethod
    def gen_indexes(cls, table_name):
        args = list(super(OrganizationMembershipBaseMixin, cls).gen_indexes(table_name))
        args.extend([Index('idx_organization_xid_{}'.format(table_name), 'organization_xid')])
        return tuple(args)
