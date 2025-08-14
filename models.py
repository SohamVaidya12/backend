from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, JSON, Float
from sqlalchemy.orm import relationship
from datetime import datetime
from .database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(64), unique=True, nullable=False, index=True)
    api_key_hash = Column(String(128), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    runs = relationship("Run", back_populates="user")

class Run(Base):
    __tablename__ = "runs"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    symbol = Column(String(32), nullable=False)
    interval = Column(String(16), nullable=False)
    capital = Column(Float, nullable=False)
    lot_size = Column(Float, nullable=False)
    params = Column(JSON, nullable=False)  # all indicators + thresholds + dates
    summary = Column(Text, nullable=True)
    table_json = Column(JSON, nullable=True)  # monthly table (list of dicts)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="runs")
    trades = relationship("Trade", back_populates="run", cascade="all, delete-orphan")

class Trade(Base):
    __tablename__ = "trades"
    id = Column(Integer, primary_key=True, index=True)
    run_id = Column(Integer, ForeignKey("runs.id"), nullable=False, index=True)
    entry_time = Column(DateTime, nullable=True)
    exit_time = Column(DateTime, nullable=True)
    entry_price = Column(Float, nullable=True)
    exit_price = Column(Float, nullable=True)
    units = Column(Float, nullable=True)
    pnl = Column(Float, nullable=True)
    indicators_triggered = Column(String(128), nullable=True)
    exit_reason = Column(String(64), nullable=True)

    run = relationship("Run", back_populates="trades")
