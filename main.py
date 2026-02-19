from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
import logging
from routes.users import router as users_router
from routes.users import get_users, get_user, get_loans
from routes.loans import router as loans_router
from routes.customers import router as customers_router
from routes.login import router as login_router


logging.basicConfig(level=logging.INFO)

# from database import engine, Base, get_db
from src.database import engine, Base, get_db


app = FastAPI(title="fastapi")

@app.get("/")
def root():
    return {"status": "ok"}
    logging.info("Application started successfully.")


# @app.on_event("startup")
# async def startup():
#     async with engine.begin() as conn:
#         await conn.run_sync(Base.metadata.create_all)

@app.get("/")
async def health_check(db: AsyncSession = Depends(get_db)):
    result = await db.execute(text("SELECT 1"))
    return {"db_status": "connected", "result": result.scalar()}
    logging.info("Health check executed successfully.")



app.include_router(users_router)
app.add_api_route("/users", get_users, methods=["GET"])
app.add_api_route("/users/{user_id}", get_user, methods=["GET"])
app.add_api_route("/loans", get_loans, methods=["GET"])
app.include_router(users_router)
app.include_router(loans_router)
app.include_router(login_router)
app.include_router(customers_router)

