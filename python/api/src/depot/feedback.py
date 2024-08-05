from .mongo.feedback import Feedback


class FeedbackDepot(object):

    @classmethod
    def create_feedback(cls, meta, data):
        fxid = Feedback.create_feedback(meta, data)
        return fxid

    @classmethod
    def fetch_feedbacks(cls):
        data = Feedback.select_feedbacks()
        return data
