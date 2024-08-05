from .mongo.subscription import Subscription


class SubscriptionDepot(object):

    @classmethod
    def create_subscription(cls, email, meta, data):
        sub_xid = Subscription.create_subscription(email, meta, data)
        return sub_xid

    @classmethod
    def fetch_subscription(cls):
        data = Subscription.select_subscriptions()
        return data
