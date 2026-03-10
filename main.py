from fastapi import FastAPI, Depends, UploadFile, Form
from fastapi.staticfiles import StaticFiles
import uvicorn
from sqlalchemy.ext.asyncio import AsyncSession

from database import *
from schemas import *
from crud import *


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


app = FastAPI()
app.mount(f'/{MEDIA_DIR}', StaticFiles(directory=MEDIA_DIR), name='media')


@app.on_event('startup')
async def startup_event():
    await init_db()


@app.post('/categories', response_model=CategoryResponse)
async def create_category_endpoint(category: CategoryCreate, db: AsyncSession = Depends(get_db)):
    return await create_category(category, db)


@app.get('/categories/', response_model=list[CategoryResponse])
async def read_categories_endpoint(db: AsyncSession = Depends(get_db)):
    return await read_categories(db)


@app.get('/categories/{category_id}/', response_model=CategoryResponse)
async def read_category_endpoint(category_id, db: AsyncSession = Depends(get_db)):
    return await read_category(category_id, db)


@app.put('/categories/{category_id}/', response_model=CategoryResponse)
async def update_category_endpoint(category_id: int, category: CategoryCreate, db: AsyncSession = Depends(get_db)):
    return await update_category(category_id, category, db)


@app.delete('/categories/{category_id}/', response_model=dict)
async def delete_category_endpoint(category_id: int, db: AsyncSession = Depends(get_db)):
    return await delete_category(category_id, db)

#------------news


@app.post('/news/', response_model=NewsResponse)
async def news_create_endpoint(
        title: str = Form(...),
        description: str = Form(...),
        views: int = Form(0),
        category_id: int = Form(...),
        db: AsyncSession = Depends(get_db),
        image: UploadFile = None,
        video: UploadFile = None
):
    news = NewsCreate(title=title, description=description,views=views, category_id=category_id)
    return await create_news(news, db, image, video)


@app.get('/news/', response_model=list[NewsResponse])
async def read_all_news_endpoint(db: AsyncSession = Depends(get_db)):
    return await read_all_news(db)


@app.get('/news/{news_id}', response_model=NewsResponse)
async def read_news_endpoint(news_id, db: AsyncSession = Depends(get_db)):
    return await read_news(news_id, db)


@app.put('/news/{news_id}/', response_model=NewsResponse)
async def update_news_endpoint(news_id, news: NewsCreate, db: AsyncSession = Depends(get_db)):
    return await update_news(news_id, news, db)


@app.delete('/news/{news_id}/', response_model=dict)
async def delete_news_endpoint(news_id: int, db: AsyncSession = Depends(get_db)):
    return await delete_news(news_id, db)


if __name__ == '__main__':
    uvicorn.run(app)