from collector.api.app import db


class ActionLogs(db.Model):
    __table_args__ = (
        db.UniqueConstraint('node_aid', 'external_id'),
    )

    id = db.Column(db.Integer, primary_key=True)
    node_aid = db.Column(db.String, nullable=False)
    external_id = db.Column(db.Integer, nullable=False)
