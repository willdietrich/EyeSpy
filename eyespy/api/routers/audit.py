from datetime import datetime, timedelta

from fastapi import APIRouter

from eyespy.api.models.audit_search_repository import AuditSearchResponse
from eyespy.api.models.audit_search_request import AuditSearchRequest
from eyespy.dal.mongo_connection import get_mongo_connection
from eyespy.enumerations.audit_type import AuditType
from eyespy.dal.audit_dal import AuditDal

connection = get_mongo_connection()
audit_dal = AuditDal(**connection)

router = APIRouter(
    prefix="/audit"
)


@router.post(
    "/search"
)
async def audit_search(query: AuditSearchRequest) -> AuditSearchResponse:
    results = []
    cursor = None

    dateTimeRange = datetime.now() - timedelta(days=query.timeframe_days)

    if query.type == AuditType.Collection:
        cursor = audit_dal.search_audit_channels(query.target, dateTimeRange)
    elif query.type == AuditType.User:
        cursor = []

    if cursor is not None:
        for result in cursor:
            results.append(result)

    return AuditSearchResponse(results=results)
