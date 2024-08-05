from flask import current_app

from src.depot.user import UserDepot


def is_user_admin(organization_xid, user_xid):
    if current_app.config["DEVELOPMENT"] or current_app.config["TESTING"]:
        return True

    user_model = UserDepot.fetch_user(organization_xid, user_xid)
    admin = user_model['email'] in ['prashant.khanduri@gmail.com', ]
    return admin
