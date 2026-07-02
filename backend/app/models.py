from datetime import datetime
from . import db


class User(db.Model):
    __tablename__ = "users"

    id                = db.Column(db.Integer, primary_key=True)
    name              = db.Column(db.String(100), nullable=False)
    checking_balance  = db.Column(db.Float, default=0.0, nullable=False)
    savings_balance   = db.Column(db.Float, default=0.0, nullable=False)

    transactions = db.relationship("Transaction", backref="user", lazy="dynamic")
    nudges       = db.relationship("ActionableNudge", backref="user", lazy="dynamic")

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "checking_balance": self.checking_balance,
            "savings_balance": self.savings_balance,
        }


class Transaction(db.Model):
    __tablename__ = "transactions"

    id          = db.Column(db.Integer, primary_key=True)
    user_id     = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    amount      = db.Column(db.Float, nullable=False)
    type        = db.Column(db.String(10), nullable=False)   # credit | debit
    category    = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(200))
    timestamp   = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "amount": self.amount,
            "type": self.type,
            "category": self.category,
            "description": self.description,
            "timestamp": self.timestamp.isoformat() + "Z",
        }


class ActionableNudge(db.Model):
    __tablename__ = "actionable_nudges"

    id              = db.Column(db.Integer, primary_key=True)
    user_id         = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    message         = db.Column(db.Text, nullable=False)
    proposed_action = db.Column(db.String(50), nullable=False)  # create_fd | invest_liquid_fund
    amount          = db.Column(db.Float, nullable=False)
    status          = db.Column(db.String(20), default="pending")  # pending | accepted | dismissed
    created_at      = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "message": self.message,
            "proposed_action": self.proposed_action,
            "amount": self.amount,
            "status": self.status,
            "created_at": self.created_at.isoformat() + "Z",
        }
