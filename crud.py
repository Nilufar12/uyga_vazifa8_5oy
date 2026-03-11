from pathlib import Path
import shutil
from fastapi import HTTPException, UploadFile

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from models import *
from schemas import *
from database import MEDIA_DIR

async def create_category(category: CategoryCreate, db: AsyncSession) -> CategoryResponse:
    db_category = Category(**category.model_dump())
    db.add(db_category)
    await db.commit()
    await db.refresh(db_category)
    return CategoryResponse.model_validate(db_category)


async def read_categories(db: AsyncSession) -> list[CategoryResponse]:
    stmt = await db.execute(select(Category))
    db_categories = stmt.scalars().all()
    return [CategoryResponse.model_validate(db_category) for db_category in db_categories]


async def read_category(category_id: int, db: AsyncSession) -> CategoryResponse:
    db_category = await db.get(Category, category_id)
    if db_category is None:
        raise HTTPException(status_code=404, detail='Category Not Found')
    return CategoryResponse.model_validate(db_category)


async def update_category(category_id: int, category: CategoryCreate, db: AsyncSession) -> CategoryResponse:
    db_category = await db.get(Category, category_id)
    if db_category is None:
        raise HTTPException(status_code=404, detail="Category Not Found")

    for attr, value in category.model_dump().items():
        setattr(db_category, attr, value)
    await db.commit()
    await db.refresh(db_category)

    return CategoryResponse.model_validate(db_category)


async def delete_category(category_id: int, db: AsyncSession) -> dict:
    db_category = await db.get(Category, category_id)
    if db_category is None:
        raise HTTPException(status_code=404, detail="Category Not Found")
    await db.delete(db_category)
    await db.commit()
    return {'message': 'Category Deleted Successful!!!'}


#-----news
async def create_news(news: NewsCreate, db: AsyncSession, image: UploadFile = None, video: UploadFile = None, document: UploadFile = None) -> NewsResponse:
    if image:
        image_extension = image.filename.lower().split('.')[-1]
        if image_extension not in ['jpg', 'png', 'bmp']:
            raise HTTPException(status_code=400, detail="Only 'jpg' and 'png' files are allowed")

    if video:
        video_extension = video.filename.lower().split('.')[-1]
        if video_extension not in ["mp4", "avi"]:
            raise HTTPException(status_code=400, detail="Only 'mp3' and 'avi' files are allowed")

    if document:
        document_extension = document.filename.lower().split('.')[-1]
    if document_extension not in ["pdf"]:
        raise HTTPException(status_code=400, detail="Only 'pdf' files are allowed")

    db_news = News(**news.model_dump())
    db.add(db_news)
    await db.commit()
    await db.refresh(db_news)

    if image:
        image_path = Path(MEDIA_DIR) / f'news_{db_news.id}_image.{image_extension}'
        with image_path.open('wb') as buffer:
            shutil.copyfileobj(image.file, buffer)
        db_news.image = str(image_path)

    if video:
        video_path = Path(MEDIA_DIR) / f'news_{db_news.id}_video.{video_extension}'
        with video_path.open('wb') as buffer:
            shutil.copyfileobj(video.file, buffer)
        db_news.video = str(video_path)

    if document:
        document_path = Path(MEDIA_DIR) / f'news_{db_news.id}_file.{document_extension}'
        with document_path.open('wb') as buffer:
            shutil.copyfileobj(document.file, buffer)
        db_news.document = str(document_path)

    await db.commit()
    await db.refresh(db_news)

    return NewsResponse.model_validate(db_news)


async def read_all_news(db: AsyncSession) -> list[NewsResponse]:
    stmt = await db.execute(select(News))
    db_all_news = stmt.scalars().all()
    return [NewsResponse.model_validate(db_news) for db_news in db_all_news]


async def read_news(news_id: int, db: AsyncSession) -> NewsResponse:
    db_news = await db.get(News, news_id)
    if db_news is None:
        raise HTTPException(status_code=404, detail='News Not Found')
    return NewsResponse.model_validate(db_news)


async def update_news(news_id: int, news: NewsCreate, db: AsyncSession) -> NewsResponse:
    db_news = await db.get(News, news_id)
    if db_news is None:
        raise HTTPException(status_code=404, detail='News Not Found')
    for attr, value in news.model_dump().items():
        setattr(news, attr, value)
    await db.commit()
    await db.refresh(db_news)
    return NewsResponse.model_validate(db_news)


async def delete_news(news_id, db: AsyncSession) -> dict:
    db_news = await db.get(News, news_id)
    if db_news is None:
        raise HTTPException(status_code=404, detail='News Not Found')
    await db.delete(db_news)
    await db.commit()
    return {'message': 'News Deleted Successful!!!'}