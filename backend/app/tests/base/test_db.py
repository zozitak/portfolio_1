# from sqlmodel import Session, create_engine, select, SQLModel# type: ignore

# from app import crud
# from app.base.config import settings
# from app.models import User, UserCreate

# engine = create_engine(settings.get_url())

# # make sure all SQLModel models are imported (app.models) before initializing DB
# # otherwise, SQLModel might fail to initialize relationships properly
# # for more details: https://github.com/tiangolo/full-stack-fastapi-template/issues/28


# def test_init_db() -> None:
#     with Session(engine) as session:
#         user = session.exec(
#             select(User).where(User.email == settings.EMAIL_TEST_SUPER_USER)
#         ).first()
#         if not user:
#             user_in = UserCreate(
#                 email=settings.EMAIL_TEST_SUPER_USER,
#                 password=settings.FIRST_SUPERUSER_PASSWORD,
#                 is_superuser=True,
#             )
#             user = crud.create_user(session=session, user_create=user_in)
#         get_user = crud.get_user_by_email(session=session, email=settings.EMAIL_TEST_SUPER_USER)
#         assert get_user
#         if get_user is not None:
#             assert user.email == get_user.email
#         else:
#             assert False