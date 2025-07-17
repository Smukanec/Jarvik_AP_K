from pathlib import Path
from typing import List, Dict

from sqlalchemy import create_engine, Column, String, Boolean
from sqlalchemy.orm import declarative_base, sessionmaker

BASE_DIR = Path(__file__).resolve().parent.parent
MEMORY_DIR = BASE_DIR / 'memory'

Base = declarative_base()

class ActionPlan(Base):
    __tablename__ = 'action_plan'

    id = Column(String, primary_key=True)
    traceability = Column(String)
    problem = Column(String)
    cause = Column(String)
    action = Column(String)
    responsible = Column(String)
    date = Column(String)
    effectiveness = Column(String)
    closed = Column(Boolean, default=False)

    def to_dict(self) -> Dict:
        return {
            'id': self.id,
            'traceability': self.traceability,
            'problem': self.problem,
            'cause': self.cause,
            'action': self.action,
            'responsible': self.responsible,
            'date': self.date,
            'effectiveness': self.effectiveness,
            'closed': self.closed,
        }

_engines = {}
_sessionmakers = {}

def _get_session(user: str):
    user_dir = MEMORY_DIR / user
    user_dir.mkdir(parents=True, exist_ok=True)
    db_path = user_dir / 'action_plan.db'
    if user not in _sessionmakers:
        engine = create_engine(
            f'sqlite:///{db_path}',
            connect_args={'check_same_thread': False},
        )
        Base.metadata.create_all(engine)
        _engines[user] = engine
        _sessionmakers[user] = sessionmaker(bind=engine, expire_on_commit=False)
    SessionLocal = _sessionmakers[user]
    return SessionLocal()

def load_memory(user: str) -> List[Dict]:
    """Return all records for a user."""
    with _get_session(user) as session:
        records = session.query(ActionPlan).all()
        return [r.to_dict() for r in records]

def save_record(user: str, record: Dict):
    """Insert a new record."""
    with _get_session(user) as session:
        session.add(ActionPlan(**record))
        session.commit()

def update_record(user: str, record_id: str, updates: Dict):
    """Update an existing record by id."""
    with _get_session(user) as session:
        ap = session.get(ActionPlan, record_id)
        if ap:
            for key, value in updates.items():
                if hasattr(ap, key):
                    setattr(ap, key, value)
            session.commit()

def delete_record(user: str, record_id: str):
    """Delete a record by id."""
    with _get_session(user) as session:
        ap = session.get(ActionPlan, record_id)
        if ap:
            session.delete(ap)
            session.commit()

def save_memory(user: str, records: List[Dict]):
    """Rewrite user's memory with the given list of records."""
    with _get_session(user) as session:
        session.query(ActionPlan).delete()
        session.add_all(ActionPlan(**r) for r in records)
        session.commit()
