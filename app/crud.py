from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from models import Rate
from typing import List
from datetime import date
BATCH_SIZE = 1000


async def add_rates(db: AsyncSession, rates: List[Rate]):
    for i in range(0, len(rates), BATCH_SIZE):
        batch = rates[i:i + BATCH_SIZE]
        for rate in batch:
            result = await db.execute(
                select(Rate).filter(Rate.cargo_type == rate.cargo_type, Rate.date == rate.date)
            )
            existing_rate = result.scalars().first()
            if existing_rate:
                existing_rate.rate = rate.rate
            else:
                db.add(rate)
    await db.commit()


async def get_current_rate(db: AsyncSession, cargo_type: str, target_date: date = None):
    if target_date:
        result = await db.execute(
            select(Rate)
            .filter(Rate.cargo_type == cargo_type)
            .filter(Rate.date <= target_date)
            .order_by(Rate.date.desc())
            .limit(1)
        )
    else:
        result = await db.execute(
            select(Rate)
            .filter(Rate.cargo_type == cargo_type)
            .order_by(Rate.date.desc())
            .limit(1)
        )
    rate = result.scalars().first()
    return rate




