import os
import traceback

from celery import Celery
from app.database import SessionLocal
from app.models import AnalysisResult
from app.crew_runner import run_crew


celery = Celery(
    "financial_worker",
    broker=os.getenv("CELERY_BROKER_URL", "redis://redis:6379/0"),
    backend=os.getenv("CELERY_RESULT_BACKEND", "redis://redis:6379/0"),
)


@celery.task(bind=True)
def analyze_document_task(self, analysis_id, query, file_path, file_name):

    db = SessionLocal()

    try:

        print(f"\n--- WORKER STARTED: {analysis_id} ---")

        result = run_crew(
            query=query,
            file_path=file_path
        )

        record = db.query(AnalysisResult).filter(
            AnalysisResult.id == analysis_id
        ).first()

        if record:
            record.status = "completed"
            record.result = result
            db.commit()

        print(f"--- WORKER COMPLETED: {analysis_id} ---\n")

        return result

    except Exception as e:

        traceback.print_exc()

        record = db.query(AnalysisResult).filter(
            AnalysisResult.id == analysis_id
        ).first()

        if record:
            record.status = "failed"
            record.result = str(e)
            db.commit()

        raise e

    finally:

        db.close()

        # ✅ DELETE FILE HERE (correct place)
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
                print(f"Deleted file: {file_path}")
        except Exception as cleanup_error:
            print(f"Cleanup error: {cleanup_error}")