from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from services import fetch_hts_codes, compare_excel
import uvicorn
import io

app = FastAPI(title="Customs Tracker API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Customs Tracker API is running"}

@app.get("/api/search")
def search_hts(q: str = ""):
    """
    Search for HTS codes by product name or description.
    """
    results = fetch_hts_codes(q)
    return results

@app.get("/api/usitc-search")
def search_usitc_proxy(q: str = ""):
    """
    Proxy to USITC API
    """
    from services import search_usitc
    return search_usitc(q)

@app.get("/api/tree")
def get_tree():
    """
    Get hierarchy tree of HTS codes.
    """
    from services import get_hts_tree
    return get_hts_tree()

@app.post("/api/sync")
async def sync_excel(file: UploadFile = File(...)):
    """
    Upload an Excel file to sync/compare data.
    """
    if not file.filename.endswith('.xlsx'):
        raise HTTPException(status_code=400, detail="Invalid file format. Please upload .xlsx")
    
    content = await file.read()
    result = compare_excel(io.BytesIO(content), [])
    return result

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
