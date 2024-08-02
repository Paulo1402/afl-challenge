import dotenv
from fastapi import FastAPI, Depends

from routes.companies import router as companies_router
from routes.auth import router as auth_router, get_current_user
from database import init_db

dotenv.load_dotenv()

app = FastAPI(root_path="/api", title="AFL Challenge")

app.include_router(auth_router, prefix="/auth", tags=["auth"])
app.include_router(
    companies_router,
    prefix="/companies",
    tags=["companies"],
    dependencies=[Depends(get_current_user)],
)

init_db()
