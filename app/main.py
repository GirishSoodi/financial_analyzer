import os
import uuid
import traceback

from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import JSONResponse

from app.database import SessionLocal, engine
from app.models import Base, AnalysisResult

from app.celery_worker import analyze_document_task


# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Financial Document Analyzer API")


# Health check
@app.get("/")
async def root():
    return {
        "status": "success",
        "message": "Financial Document Analyzer API running"
    }


# Submit analysis job (ASYNC)
@app.post("/analyze")
async def analyze_financial_document_api(
    file: UploadFile = File(...),
    query: str = Form(default="Analyze this financial document for investment insights")
):

    file_id = str(uuid.uuid4())

    os.makedirs("data", exist_ok=True)

    file_path = f"data/financial_document_{file_id}.pdf"

    try:

        # Save file
        with open(file_path, "wb") as f:
            f.write(await file.read())

        print("\n--- JOB SUBMITTED ---")
        print("File:", file.filename)
        print("ID:", file_id)
        print("---------------------\n")

        # Save job to database
        db = SessionLocal()

        record = AnalysisResult(
            id=file_id,
            file_name=file.filename,
            query=query,
            status="processing",
            result=""
        )

        db.add(record)
        db.commit()
        db.close()

        # Send to Celery worker
        analyze_document_task.delay(
            analysis_id=file_id,
            query=query.strip(),
            file_path=file_path,
            file_name=file.filename
        )

        # Return immediately (non-blocking)
        return JSONResponse(
            status_code=202,
            content={
                "status": "processing",
                "analysis_id": file_id,
                "message": "Analysis started. Use /result/{analysis_id}"
            }
        )

    except Exception as e:

        traceback.print_exc()

        return JSONResponse(
            status_code=500,
            content={
                "status": "error",
                "message": str(e)
            }
        )


# Get analysis result
@app.get("/result/{analysis_id}")
def get_analysis_result(analysis_id: str):

    db = SessionLocal()

    try:

        record = db.query(AnalysisResult).filter(
            AnalysisResult.id == analysis_id
        ).first()

        if not record:

            return JSONResponse(
                status_code=404,
                content={
                    "status": "error",
                    "message": "Analysis ID not found"
                }
            )

        return {

            "analysis_id": record.id,
            "file_name": record.file_name,
            "query": record.query,
            "status": record.status,
            "result": record.result,
            "created_at": record.created_at

        }

    finally:

        db.close()


# Run locally
if __name__ == "__main__":

    import uvicorn

    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )