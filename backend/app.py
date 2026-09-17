from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
import shutil
import os
from backend.analyzer import analyze_dcgm
from backend.report_gen import generate_pdf_report

app = FastAPI(title="ThermaCompute AI Diagnostic Engine")

# Setup for reports directory
REPORTS_DIR = "reports"
os.makedirs(REPORTS_DIR, exist_ok=True)

# Serve frontend
app.mount("/frontend", StaticFiles(directory="frontend"), name="frontend")

@app.post("/api/upload-audit")
async def upload_audit(file: UploadFile = File(...)):
    if not file.filename.endswith('.csv'):
        raise HTTPException(status_code=400, detail="Only CSV files are supported.")

    # Save uploaded file
    temp_path = f"temp_{file.filename}"
    with open(temp_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    try:
        # 1. Analyze logs
        metrics = analyze_dcgm(temp_path)

        # 2. Generate PDF report
        report_filename = "thermal_waste_audit.pdf"
        report_path = os.path.join(REPORTS_DIR, report_filename)
        generate_pdf_report(metrics, report_path)

        return {
            "metrics": metrics,
            "report_url": f"/api/download-report/{report_filename}"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")
    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)

@app.get("/api/download-report/{filename}")
async def download_report(filename: str):
    file_path = os.path.join(REPORTS_DIR, filename)
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Report not found.")
    return FileResponse(path=file_path, filename=filename, media_type='application/pdf')

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
