engine = create_async_engine(
    url=get_db_settings().async_connection_string,
    echo=True,
)

async_session_global = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_global.begin() as session:
        try:
            yield session
        except:
            await session.rollback()
            raise
        finally:
            await session.close()

# defind fastapi application
app = FastAPI()

router = APIRouter()
@router.get('/api/async-examples/{id}')
def get_example(id: int, db = Depends(get_async_session)):
    return await db.execute(select(Example)).all()

@router.put('/api/async-examples/{id}')
def put_example(id: int, db = Depends(get_async_session)):
    await db.execute(update(Example).where(id=id).values(name='testtest', age=123))
    await db.commit()
    await db.refresh(Example)
    return await db.execute(select(Example).filter_by(id=id)).scalar_one()

app.include_router(router)