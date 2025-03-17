import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models.base import Base


class User(Base):
    """Modelo representando um usuário."""

    __tablename__ = "user"
    id: Mapped[int] = mapped_column(sa.Integer, primary_key=True)
    username: Mapped[str] = mapped_column(sa.String, unique=True, nullable=False)
    password: Mapped[str] = mapped_column(sa.String, nullable=False)
    role_id: Mapped[int] = mapped_column(sa.ForeignKey("role.id"))
    role: Mapped["Role"] = relationship(back_populates="user")  # noqa: F821

    def __repr__(self) -> str:
        """Retorna uma representação em string do User."""
        return f"User(id={self.id!r}, username={self.username!r})"
