from datetime import datetime, timedelta
from logging import Logger, getLogger

from celery import shared_task
from sqlalchemy import delete

from app.config import appConfig
from app.database.postgre import db
from app.database.postgre.models import Session
from app.tasks import TaskConfig


taskConfig: TaskConfig = TaskConfig()
logger: Logger = getLogger("celery")


@shared_task(
    name="delete_expired_sessions",
    bind=True,
    max_retries=taskConfig.max_retries,
    task_time_limit=taskConfig.task_time_limit,
    priority=taskConfig.priority
)
def delete_expired_sessions(self) -> None:
    expire: datetime = datetime.now() \
        - timedelta(seconds=appConfig.REFRESH_TOKEN_LIFETIME) \
        - timedelta(hours=3)  # because of utc((

    db.session.execute(
        delete(Session).filter(Session.last_activity < expire)
    )
    db.session.commit()
    logger.info(msg="expired sessions in postgre deleted")
