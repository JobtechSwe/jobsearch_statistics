from fastapi import FastAPI

from .routers import ads

app = FastAPI(
    title="Jobsearch Statistics",
    description="Statistics for usage of the Jobsearch api",
    version="0.1.0",)
app.include_router(ads.router)
