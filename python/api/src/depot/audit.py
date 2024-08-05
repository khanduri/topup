from .mongo.audit import Audit


class AuditDepot(object):

    @classmethod
    def insert_log(cls, bucket, topic, text, meta_dict):
        return Audit.insert_log(bucket, topic, text, meta_dict)

    @classmethod
    def fetch_logs(cls):
        return Audit.fetch_logs()
