from .logging import logger
from sqlalchemy.exc import IntegrityError, OperationalError, SQLAlchemyError
from .models import User
from . import db


class DatabaseServices:
    def get_all_users():
        try:
            users = User.query.all()
            logger.info(f"Success: all users queried, {len(users)} user(s) in database")

        except OperationalError as e:
            logger.error(f"DatabaseOperationalError: {e}")
            users = []
        except SQLAlchemyError as e:
            logger.error(f"SQLAlchemyError: {e}")
            users = []

        return users

    def add_user(user):
        try:
            db.session.add(user)
            db.session.commit()
            logger.info(f"Success: {user} has been added to the database.")
            posted = True

        except IntegrityError as e:
            logger.error(f"IntegrityError: {e}")
            db.session.rollback()
        except OperationalError as e:
            logger.error(f"OperationalError: {e}")
            db.session.rollback()
        except SQLAlchemyError as e:
            logger.error(f"SQLAlchemyError: {e}")
            db.session.rollback()

        return posted

    def delete_user_by_id(user_id):
        try:
            user = User.query.get(user_id)

        except OperationalError as e:
            logger.error(f"OperationalError: {e}")
        except SQLAlchemyError as e:
            logger.error(f"SQLAlchemyError: {e}")

        if user:
            try:
                db.session.delete(user)
                db.session.commit()
                logger.info(f"Success: {user} has been removed from the database.")

            except IntegrityError as e:
                logger.error(f"IntegrityError: {e}")
                db.session.rollback()
            except OperationalError as e:
                logger.error(f"OperationalError: {e}")
                db.session.rollback()
            except SQLAlchemyError as e:
                logger.error(f"SQLAlchemyError: {e}")
                db.session.rollback()
