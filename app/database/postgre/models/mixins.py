from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column


class BaseIDMixin:
    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} ID={self.ID}>"


class DefaultIDMixin(BaseIDMixin):
    ID: Mapped[str] = mapped_column(String(16), primary_key=True)


class UUIDMixin(BaseIDMixin):
    ID: Mapped[str] = mapped_column(String(36), primary_key=True)


class UserRelMixin:
    user_id: Mapped[str] = mapped_column(
        ForeignKey("User.uuid", ondelete="CASCADE")
    )
