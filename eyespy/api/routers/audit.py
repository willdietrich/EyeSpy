import base64
from datetime import datetime, timedelta

import bson
from fastapi import APIRouter

from api.models.audit_search_repository import AuditSearchResponse
from api.models.audit_search_request import AuditSearchRequest
from dal import AuditDal
from dal.mongo_connection import get_mongo_connection
from enumerations.audit_type import AuditType

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
