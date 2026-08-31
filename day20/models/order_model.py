from models.user_model import db
from datetime import datetime, timezone

class Order(db.Model):
    __tablename__ = "orders"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False, index=True)
    item_name = db.Column(db.String(200), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(50), nullable=False, default="pending")
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    def to_dict(self):
        return {
            "id": self.id,
            "item_name": self.item_name,
            "amount": self.amount,
            "status": self.status,
            "created_at": self.created_at.isoformat(),
        }