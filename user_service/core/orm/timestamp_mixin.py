from datetime import datetime

from sqlalchemy import Column
from sqlalchemy.orm import declarative_mixin
from sqlalchemy.sql.sqltypes import DateTime


@declarative_mixin
class TimestampMixin:
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
