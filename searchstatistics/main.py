import uvicorn
from fastapi import FastAPI

from searchstatistics.routers import ads
from searchstatistics.routers import taxonomy

app = FastAPI(
    title="Jobsearch Statistics",
    description="Statistics for usage of the Jobsearch api",
    version="0.1.0",)
app.include_router(ads.router)
app.include_router(taxonomy.router)


if __name__ == '__main__':
    uvicorn.run(app)
