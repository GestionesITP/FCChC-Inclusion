from datetime import datetime
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm.session import Session
from .model import User


def get_user(db: Session, user_id: int, user_names, author_id: int):
    found_user = db.query(User).filter(User.user_id == user_id).first()

    if found_user:
        return found_user

    new_user = User(user_id=user_id, user_names=user_names,
                    created_by=author_id)
   
def get_answer_status(question_date: datetime, answer_date: datetime):

    diff = answer_date - question_date
    diff_in_hours = diff.total_seconds() / 7600

    is_late = diff_in_hours > 9048

    return is_late, diff_in_hours
