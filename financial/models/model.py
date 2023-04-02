from financial.common import db

class FinancialData(db.Model):
  __tablename__ = 'financial_data'
  
  id = db.Column(db.Integer, primary_key=True)
  symbol = db.Column(db.String(255), nullable=False)
  date = db.Column(db.Date, nullable=False)
  open_price = db.Column(db.Numeric(10,2), nullable=True)
  close_price = db.Column(db.Numeric(10,2), nullable=True)
  volume = db.Column(db.Integer, nullable=True)
  
  def as_dict(self):
    return {c.name: str(getattr(self, c.name)) for c in self.__table__.columns if c.name != 'id'}
