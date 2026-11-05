from fastapi import APIRouter, HTTPException, status
from scalar_fastapi import get_scalar_api_reference

from app.services.log_analysis_chain import analyze_logs
from app.schemas.incident import LogAnalysisRequest

router = APIRouter()


@router.post("/post")
def result(body: LogAnalysisRequest):

    answer = analyze_logs(body.log_text)

    return answer


@router.get("/scalar", include_in_schema=False)
def scalar():
    return get_scalar_api_reference(
        openapi_url="/openapi.json",
        title="scalar API",
    )
