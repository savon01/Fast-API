import uvicorn

from fastapi import FastAPI
from core.db import engine, Base
from views import menus, submenus, dishes


Base.metadata.create_all(bind=engine)

app = FastAPI(title="My Fast API", description="My first API", docs_url="/")

app.include_router(menus.router)
app.include_router(submenus.router)
app.include_router(dishes.router)


if __name__ == "__main__":
    uvicorn.run(app)
