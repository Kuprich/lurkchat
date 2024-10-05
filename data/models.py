from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy import Integer, Boolean


class Base(DeclarativeBase):
    pass


class Room(Base):
    __tablename__ = 'room'
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    chat_id_1: Mapped[int] = mapped_column(Integer, nullable=True)
    chat_id_2: Mapped[int] = mapped_column(Integer, nullable=True)
    is_busy: Mapped[bool] = mapped_column(Boolean, default=False)

    def __repr__(self) -> str:
        return f'Room(id={self.id}, chat_id_1={self.chat_id_1}, chat_id_2={self.chat_id_2}, is_busy-{self.is_busy})'

