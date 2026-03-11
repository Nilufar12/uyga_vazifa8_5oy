from typing import Optional

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, ForeignKey

from database import Base


class Category(Base):
    __tablename__ = 'categories'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50))

    news: Mapped[list['News']] = relationship('News', back_populates='category')


class News(Base):
    __tablename__ = 'news'

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(100))
    description: Mapped[str] = mapped_column(String(150))
    views: Mapped[int] = mapped_column()

    image: Mapped[Optional[str]] = mapped_column(nullable=True)
    video: Mapped[Optional[str]] = mapped_column(nullable=True)
    document: Mapped[Optional[str]] = mapped_column(nullable=True)

    category_id: Mapped[int] = mapped_column(ForeignKey('categories.id'))

    category: Mapped["Category"] = relationship("Category", back_populates='news')