from datetime import datetime, timedelta

from celery import shared_task
from sqlalchemy import delete

from app.config import appConfig
from app.database.postgre import db
from app.database.postgre.models import Session


class _TaskConfig():
    max_retries: int = 0
    task_time_limit: int = 10
    priority: int = 3


taskConfig: _TaskConfig = _TaskConfig()


@shared_task(
    name="delete_expired_sessions",
    bind=True,
    max_retries=taskConfig.max_retries,
    task_time_limit=taskConfig.task_time_limit,
    priority=taskConfig.priority
)
def delete_expired_sessions() -> None:
    expire: datetime = datetime.now() \
        - timedelta(seconds=appConfig.REFRESH_TOKEN_LIFETIME) \
        - timedelta(hours=3)  # because of utc((

    db.session.execute(
        delete(Session).filter(Session.last_activity < expire)
    )
    db.session.commit()
