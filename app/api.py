from fastapi import FastAPI

app = FastAPI(
    title="Wolt delivery fee calculator API",
    summary="Wolt Summer 2024 Internship backend assignment project, python HTTP API for calculating delivery fees",
    version="0.0.1",
    contact={
        "name": "jj-stigell",
        "url": "https://github.com/jj-stigell",
    },
    license_info={
        "name": "MIT",
        "url": "https://github.com/jj-stigell/wolt-api/blob/main/LICENSE",
    },
)
