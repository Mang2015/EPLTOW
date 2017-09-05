from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Players(db.Model):
	pid = db.Column(db.Integer, primary_key=True)
	playername = db.Column(db.Unicode(32), unique=True, nullable=False)

	def __init__(self,pid,playername):
		self.pid = pid
		self.playername = playername
