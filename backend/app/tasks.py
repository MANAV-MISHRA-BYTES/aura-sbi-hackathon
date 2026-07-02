import random
from datetime import datetime, timedelta
from celery import shared_task

from . import db
from .models import User, Transaction, ActionableNudge


# Nudge message templates (one chosen at random per trigger)
NUDGE_TEMPLATES = [
    {
        "action": "invest_liquid_fund",
        "template": (
            "🎯 Smart Move! I noticed ₹{surplus:,.0f} sitting idle after all your "
            "monthly expenses. Inflation is quietly eroding its value!\n\n"
            "Want me to instantly park ₹{amount:,.0f} in an SBI Liquid Fund earning "
            "~7% p.a.? You can withdraw it anytime — as flexible as your savings account."
        ),
    },
    {
        "action": "create_fd",
        "template": (
            "💡 Opportunity Spotted! Your June salary credited ₹75,000 and after all "
            "expenses, ₹{surplus:,.0f} is sitting unused.\n\n"
            "An SBI 90-Day FD at 6.8% p.a. on ₹{amount:,.0f} would earn you "
            "₹{interest:,.0f} risk-free by September — guaranteed by the Government of India."
        ),
    },
    {
        "action": "invest_liquid_fund",
        "template": (
            "📈 Aura Insight: ₹{surplus:,.0f} has been idle since your salary credit.\n\n"
            "Shall I move ₹{amount:,.0f} to SBI Liquid Fund? It earns 2× more than a "
            "savings account while staying instantly accessible — zero lock-in."
        ),
    },
]


def _run_analysis(user_id: int) -> dict:
    user = User.query.get(user_id)
    if not user:
        return {"status": "error", "message": "User not found"}

    # Skip if a pending nudge already exists
    if ActionableNudge.query.filter_by(user_id=user_id, status="pending").first():
        return {"status": "skipped", "message": "Pending nudge already exists"}

    # Analyse last 30 days of transactions
    since = datetime.utcnow() - timedelta(days=30)
    txns = Transaction.query.filter(
        Transaction.user_id == user_id,
        Transaction.timestamp >= since,
    ).all()

    total_debits    = sum(t.amount for t in txns if t.type == "debit")
    has_salary      = any(t.category == "Salary" and t.amount >= 30_000 for t in txns)
    surplus         = user.checking_balance - total_debits

    # Trigger condition: high balance + salary detected + meaningful surplus
    if user.checking_balance > 50_000 and has_salary and surplus > 10_000:
        invest_amount = round(min(surplus * 0.65, 15_000) / 1_000) * 1_000
        interest_90d  = invest_amount * 0.068 * (90 / 365)

        template = random.choice(NUDGE_TEMPLATES)
        message  = template["template"].format(
            surplus=surplus, amount=invest_amount, interest=interest_90d
        )

        nudge = ActionableNudge(
            user_id=user_id,
            message=message,
            proposed_action=template["action"],
            amount=invest_amount,
            status="pending",
        )
        db.session.add(nudge)
        db.session.commit()
        return {"status": "nudge_created", "nudge_id": nudge.id, "amount": invest_amount}

    return {"status": "no_action", "message": "Conditions not met"}


@shared_task(name="aura.analyze_financial_health")
def analyze_financial_health(user_id: int = 1) -> dict:
    return _run_analysis(user_id)
