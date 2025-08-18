from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import select
from database import Base, engine, get_db
from models import User, Run, Trade
from schemas import SignupIn, SignupOut, RunIn, RunOut, TradesIn, TradeOut
from security import generate_api_key, hash_api_key, require_api_key

app = FastAPI(title="BullRun Backend", version="1.0.0")

# Create tables at startup
@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)

@app.get("/health")
def health():
    return {"ok": True}

@app.post("/auth/signup", response_model=SignupOut)
def signup(data: SignupIn, db: Session = Depends(get_db)):
    exists = db.execute(select(User).where(User.username == data.username)).scalar_one_or_none()
    if exists:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Username already exists")
    api_key = generate_api_key(data.username)
    user = User(username=data.username, api_key_hash=hash_api_key(api_key))
    db.add(user)
    db.commit()
    db.refresh(user)
    return {"api_key": api_key}

@app.post("/runs", response_model=RunOut)
def create_run(payload: RunIn, current_user: User = Depends(require_api_key), db: Session = Depends(get_db)):
    run = Run(
        user_id=current_user.id,
        symbol=payload.symbol,
        interval=payload.interval,
        capital=payload.capital,
        lot_size=payload.lot_size,
        params=payload.params,
        summary=payload.summary,
        table_json=payload.table_json
    )
    db.add(run)
    db.commit()
    db.refresh(run)
    return run

@app.get("/runs", response_model=list[RunOut])
def list_runs(current_user: User = Depends(require_api_key), db: Session = Depends(get_db)):
    runs = db.query(Run).filter(Run.user_id == current_user.id).order_by(Run.created_at.desc()).all()
    return runs

@app.get("/runs/{run_id}", response_model=RunOut)
def get_run(run_id: int, current_user: User = Depends(require_api_key), db: Session = Depends(get_db)):
    run = db.query(Run).filter(Run.id == run_id, Run.user_id == current_user.id).first()
    if not run:
        raise HTTPException(status_code=404, detail="Run not found")
    return run

@app.post("/runs/{run_id}/trades", response_model=list[TradeOut])
def add_trades(run_id: int, payload: TradesIn, current_user: User = Depends(require_api_key), db: Session = Depends(get_db)):
    run = db.query(Run).filter(Run.id == run_id, Run.user_id == current_user.id).first()
    if not run:
        raise HTTPException(status_code=404, detail="Run not found")
    created = []
    for t in payload.trades:
        tr = Trade(
            run_id=run.id,
            entry_time=t.entry_time,
            exit_time=t.exit_time,
            entry_price=t.entry_price,
            exit_price=t.exit_price,
            units=t.units,
            pnl=t.pnl,
            indicators_triggered=t.indicators_triggered,
            exit_reason=t.exit_reason
        )
        db.add(tr)
        created.append(tr)
    db.commit()
    for tr in created:
        db.refresh(tr)
    return created

@app.get("/runs/{run_id}/trades", response_model=list[TradeOut])
def get_trades(run_id: int, current_user: User = Depends(require_api_key), db: Session = Depends(get_db)):
    run = db.query(Run).filter(Run.id == run_id, Run.user_id == current_user.id).first()
    if not run:
        raise HTTPException(status_code=404, detail="Run not found")
    trades = db.query(Trade).filter(Trade.run_id == run_id).order_by(Trade.id.asc()).all()
    return trades
