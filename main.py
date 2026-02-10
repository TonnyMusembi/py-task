from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
import logging
from routes.users import router as users_router
from routes.users import get_users

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

# @app.get("/users")
# async def get_user(db: AsyncSession = Depends(get_db)):
#     if not db:
#         logging.error("Database connection failed in get_users endpoint.")
#         raise HTTPException(status_code=500, detail="Database connection failed")

#     result = await db.execute(
#         text("""
#             SELECT id, full_name, email, role, created_at
#             FROM users
#         """)
#     )

#     users = result.fetchall()
#     logging.info("Fetched users successfully.")

#     return {
#         "users": [dict(row._mapping) for row in users]
#     }

app.include_router(users_router)
app.add_api_route("/users", get_users, methods=["GET"])

