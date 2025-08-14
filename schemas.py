from pydantic import BaseModel, Field
from typing import List, Optional, Any
from datetime import datetime

class SignupIn(BaseModel):
    username: str = Field(min_length=3, max_length=64)

class SignupOut(BaseModel):
    api_key: str

class RunIn(BaseModel):
    symbol: str
    interval: str
    capital: float
    lot_size: float
    params: dict
    summary: Optional[str] = None
    table_json: Optional[list] = None

class RunOut(BaseModel):
    id: int
    created_at: datetime
    symbol: str
    interval: str
    capital: float
    lot_size: float
    params: Any
    summary: Optional[str] = None
    table_json: Optional[list] = None

    class Config:
        from_attributes = True

class TradeIn(BaseModel):
    entry_time: Optional[datetime] = None
    exit_time: Optional[datetime] = None
    entry_price: Optional[float] = None
    exit_price: Optional[float] = None
    units: Optional[float] = None
    pnl: Optional[float] = None
    indicators_triggered: Optional[str] = None
    exit_reason: Optional[str] = None

class TradesIn(BaseModel):
    trades: List[TradeIn]

class TradeOut(TradeIn):
    id: int
    class Config:
        from_attributes = True
