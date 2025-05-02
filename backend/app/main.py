from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
from datetime import datetime
from typing import Optional

from streaming_stats import calculate_stats

app = FastAPI(title="Stream Stats API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

data_dir = Path("data")
data_dir.mkdir(exist_ok=True)


@app.get("/")
async def root():
    return {"message": "Welcome to Stream Stats API"}


@app.post("/upload-tsv/")
async def upload_tsv(file: UploadFile = File(...)):
    if not file.filename or Path(file.filename).suffix != ".tsv":
        raise HTTPException(status_code=400, detail="File must be a TSV")

    file_path = data_dir / f"upload_{datetime.now().strftime('%Y%m%d_%H%M%S')}.tsv"
    with open(file_path, "wb") as f:
        f.write(await file.read())

    return {"filename": file_path.name, "status": "File uploaded successfully"}


@app.get("/streaming-stats/")
async def streaming_stats(
    filename: str,
    store: Optional[str] = None,
    year: Optional[str] = None,
    month: Optional[str] = None,
    country: Optional[str] = None,
):
    file_path = data_dir / filename
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="File not found")

    try:
        stats = calculate_stats(file_path, store, year, month, country)
        return stats
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing file: {str(e)}")


@app.get("/available-files/")
async def list_available_files():
    files = [f.name for f in data_dir.glob("*.tsv")]
    return {"files": files}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
