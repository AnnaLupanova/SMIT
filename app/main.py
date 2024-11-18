from fastapi import FastAPI, Depends, HTTPException
from database import AsyncSession, SessionLocal, engine
import schemas
from typing import List, Dict
from models import Rate
import crud
import traceback
from database import Base
from datetime import date


app = FastAPI()

@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


@app.on_event("shutdown")
async def shutdown():
    await engine.dispose()


async def get_db() -> AsyncSession:
    async with SessionLocal() as session:
        yield session


@app.post('/upload_rates/')
async def upload_rates(request_rates: Dict[date, List[schemas.Rate]], db: AsyncSession = Depends(get_db)):

    """
        Upload tariff by JSON format

        - JSON format:
            {
                "2020-07-01": [
                    {cargo_type: "test", "rate": "0.01"},
                ]
            }
    """
    try:
        rate_objects = []
        for date, rate_list in request_rates.items():
            for rate in rate_list:
                rate_objects.append(Rate(cargo_type=rate.cargo_type, rate=float(rate.rate), date=date))

        await crud.add_rates(db, rate_objects)

        return {"message": "Rates successfully uploaded to the database."}
    except Exception as e:
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/calculate_insurance/")
async def calculate_insurance(cargo_type: str, declared_value: float, target_date: date = None,
                              db: AsyncSession = Depends(get_db)):
    """
        Calculate the cost of insurance for a request based on the corresponding tariff

        - Args:
            cargo_type (str): Сargo type (example 'Glass')
            declared_value (float): Declared value of the cargo
            target_date (date or None): Date (example 2024-07-01)
    """

    rate = await crud.get_current_rate(db=db, cargo_type=cargo_type, target_date=target_date)
    if rate is None:
        raise HTTPException(status_code=404, detail="Rate not found for cargo type and date")

    return declared_value * rate.rate

