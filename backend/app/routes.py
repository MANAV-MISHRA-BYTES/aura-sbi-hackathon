from flask import Blueprint, jsonify, request
from .models import User, Transaction, ActionableNudge
from . import db

api = Blueprint("api", __name__)
DEMO_USER_ID = 1


@api.route("/dashboard", methods=["GET"])
def dashboard():
    user = User.query.get_or_404(DEMO_USER_ID)
    txns = (
        Transaction.query
        .filter_by(user_id=DEMO_USER_ID)
        .order_by(Transaction.timestamp.desc())
        .limit(10)
        .all()
    )
    return jsonify({"user": user.to_dict(), "transactions": [t.to_dict() for t in txns]})


@api.route("/nudges", methods=["GET"])
def get_nudges():
    nudges = (
        ActionableNudge.query
        .filter_by(user_id=DEMO_USER_ID, status="pending")
        .order_by(ActionableNudge.created_at.desc())
        .all()
    )
    return jsonify({"nudges": [n.to_dict() for n in nudges]})


@api.route("/execute-nudge", methods=["POST"])
def execute_nudge():
    data    = request.get_json(silent=True) or {}
    nudge_id = data.get("nudge_id")
    if not nudge_id:
        return jsonify({"error": "nudge_id is required"}), 400

    nudge = ActionableNudge.query.get_or_404(nudge_id)
    if nudge.status != "pending":
        return jsonify({"error": "Nudge already processed"}), 400

    user = User.query.get_or_404(nudge.user_id)
    if user.checking_balance < nudge.amount:
        return jsonify({"error": "Insufficient checking balance"}), 400

    # Move funds: deduct checking, credit savings
    user.checking_balance -= nudge.amount
    user.savings_balance  += nudge.amount
    nudge.status = "accepted"
    db.session.commit()

    return jsonify({
        "success": True,
        "message": f"₹{nudge.amount:,.0f} successfully moved!",
        "action": nudge.proposed_action,
        "new_checking_balance": user.checking_balance,
        "new_savings_balance": user.savings_balance,
    })


@api.route("/dismiss-nudge", methods=["POST"])
def dismiss_nudge():
    data    = request.get_json(silent=True) or {}
    nudge_id = data.get("nudge_id")
    if not nudge_id:
        return jsonify({"error": "nudge_id is required"}), 400

    nudge = ActionableNudge.query.get_or_404(nudge_id)
    nudge.status = "dismissed"
    db.session.commit()
    return jsonify({"success": True})


@api.route("/trigger-agent", methods=["POST"])
def trigger_agent():
    from .tasks import analyze_financial_health, _run_analysis
    try:
        # Attempt async Celery dispatch; falls back to sync if Redis is unavailable
        task = analyze_financial_health.apply_async(args=[DEMO_USER_ID])
        return jsonify({
            "success": True,
            "message": "🤖 Aura is analysing your finances… Check back in 3 seconds!",
            "task_id": str(task.id),
            "mode": "async",
        })
    except Exception:
        result = _run_analysis(DEMO_USER_ID)
        return jsonify({
            "success": True,
            "message": "✅ Aura has analysed your finances!" if result.get("status") == "nudge_created" else "ℹ️ " + result.get("message", ""),
            "result": result,
            "mode": "sync",
        })


@api.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok", "service": "Aura API v1.0"})
