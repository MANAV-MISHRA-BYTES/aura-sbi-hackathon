from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

db = SQLAlchemy()


def create_app() -> Flask:
    app = Flask(__name__)
    app.config.from_object("app.config.Config")

    CORS(app, resources={r"/api/*": {"origins": "*"}})
    db.init_app(app)

    from .celery_factory import celery_init_app
    celery_init_app(app)

    from .routes import api
    app.register_blueprint(api, url_prefix="/api")

    with app.app_context():
        db.create_all()
        _seed_data()

    return app


def _seed_data() -> None:
    from .models import User, Transaction
    from datetime import datetime, timedelta

    if User.query.first():
        return

    user = User(name="Rajesh Kumar", checking_balance=65_000.0, savings_balance=12_500.0)
    db.session.add(user)
    db.session.flush()

    now = datetime.utcnow()
    transactions = [
        Transaction(user_id=user.id, amount=75_000, type="credit", category="Salary",
                    description="SBI Payroll — June 2025",      timestamp=now - timedelta(days=5)),
        Transaction(user_id=user.id, amount=12_500, type="debit",  category="Rent",
                    description="Housing rent transfer",          timestamp=now - timedelta(days=4)),
        Transaction(user_id=user.id, amount=3_200,  type="debit",  category="Groceries",
                    description="BigBasket Monthly Order",        timestamp=now - timedelta(days=3)),
        Transaction(user_id=user.id, amount=1_800,  type="debit",  category="Utilities",
                    description="BESCOM Electricity Bill",        timestamp=now - timedelta(days=3)),
        Transaction(user_id=user.id, amount=5_000,  type="debit",  category="Dining",
                    description="Zomato & Swiggy",               timestamp=now - timedelta(days=2)),
        Transaction(user_id=user.id, amount=2_500,  type="debit",  category="Transport",
                    description="Uber rides — June",             timestamp=now - timedelta(days=2)),
        Transaction(user_id=user.id, amount=800,    type="debit",  category="Entertainment",
                    description="Netflix + Spotify",             timestamp=now - timedelta(days=1)),
        Transaction(user_id=user.id, amount=4_200,  type="debit",  category="Shopping",
                    description="Myntra flash sale",             timestamp=now - timedelta(days=1)),
        Transaction(user_id=user.id, amount=500,    type="credit", category="Cashback",
                    description="YONO Cashback Reward",          timestamp=now - timedelta(hours=12)),
        Transaction(user_id=user.id, amount=1_500,  type="debit",  category="Healthcare",
                    description="Apollo Pharmacy",               timestamp=now - timedelta(hours=6)),
    ]
    db.session.bulk_save_objects(transactions)
    db.session.commit()
