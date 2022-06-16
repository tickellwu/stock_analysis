from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import sessionmaker

Base = declarative_base()


class stock_code_status(Base):
    __tablename__ = 'code_status'
    stock_code = Column(String(64), nullable=False, primary_key=True)
    status = Column(Integer, nullable=False, index=True)

    def __repr__(self):
        return '%s(%r)' % (self.__class__.__name__, self.stock_code)


class sqldao:
    def __init__(self, _engine):
        self.engine = _engine
        self.session = sessionmaker(bind=_engine)()

    def set_status(self, _code, _status):
        result = self.session.query(stock_code_status).filter_by(stock_code=_code).all()
        if len(result) == 0:
            self.session.add(stock_code_status(stock_code=_code, status=_status))
        else:
            self.session.query(stock_code_status).filter_by(stock_code=_code).update({"status": _status})
        self.session.commit()

#if __name__ == "__main__":
#    engine = create_engine('mysql://grafana:1ikedb^R@127.0.0.1:3333/stock_db')
#    dao = sqldao(engine)
#    dao.set_status("000972.SZ", 2)
