from fastapi import FastAPI

app = FastAPI(title="TruCon NDTS API",
              description="Nigerian Data Trust System backend - Citizen-First Consent Platform",
              version="0.1.0")

@app.get("/health", tags=["Infra"])
def health():
    return {"status": "ok", "message": "TruCon Backend API running"}
