from datetime import datetime, timedelta

from celery import shared_task
from sqlalchemy import delete

from ..config import appConfig
from ..database.postgre import db
from ..database.postgre.models import Session


tasks_config: dict[str, int | bool] = {
    "bind": True,
    "default_retry_delay": 60,
    "max_retries": 3,
    "task_time_limit": 15,
    "priority": 3
}


@shared_task(name="delete_expired_sessions", options=tasks_config)
def delete_expired_sessions():
    expire: datetime = datetime.now() \
        - timedelta(seconds=appConfig.REFRESH_TOKEN_LIFETIME) \
        - timedelta(hours=3)  # because of utc((

    db.session.execute(
        delete(Session).filter(Session.last_activity < expire)
    )
    db.session.commit()
