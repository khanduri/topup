from src import create_app, db
import src.micro_services


def init():
    # org = Organization(xid="test_org_xid", name="PRODUCT - demo", domain="domain.com")
    # db.session.add(org)
    # db.session.commit()
    pass


if __name__ == '__main__':
    # INSTRUCTIONS:
    # export PYTHONPATH=/Users/pkrypto/projects/projectskeleton/api
    # python scripts/oneoff/init_db.py
    app = create_app()
    with app.app_context():
        init()
