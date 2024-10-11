from http import HTTPStatus
from flask import Blueprint
from database import Session
from utils.response import error_response, success_response
from .service import TaskService
from utils.data_validator import DataValidator
from logger import logger
from .validator import TaskCreateModel, TaskUpdateModel
from functools import wraps
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from psycopg2.errors import ForeignKeyViolation

blueprint = Blueprint("tasks", __name__, url_prefix="/tasks")

# Centralized session and exception handling decorator
def handle_exceptions_and_session(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            with Session() as session:
                return func(session, *args, **kwargs)
        except ForeignKeyViolation as fk_error:
            logger.error(f"Foreign key violation: {fk_error}", exc_info=True)
            return error_response(
                "The product ID or note type ID provided does not exist. Please ensure they are valid.",
                HTTPStatus.BAD_REQUEST
            )
        except IntegrityError as integrity_error:
            logger.error(f"Integrity error: {integrity_error}", exc_info=True)
            return error_response(
                "Data integrity error occurred. Please check the input values.",
                HTTPStatus.BAD_REQUEST
            )
        except SQLAlchemyError as db_error:
            logger.error(f"Database error in {func.__name__}: {db_error}", exc_info=True)
            return error_response(
                "A database error occurred. Please try again later.",
                HTTPStatus.INTERNAL_SERVER_ERROR
            )
        except ValueError as ve:
            logger.error(f"Value error: {ve}", exc_info=True)
            return error_response(str(ve), HTTPStatus.BAD_REQUEST)
        except Exception as e:
            logger.error(f"Error in {func.__name__}: {e}", exc_info=True)
            return error_response(
                "An unexpected error occurred. Please try again later.",
                HTTPStatus.INTERNAL_SERVER_ERROR
            )
    return wrapper

# Route definitions
@blueprint.route("", methods=["GET"])
@handle_exceptions_and_session
def get_products(session):
    response = TaskService.get_all(session)
    return success_response(data=response), HTTPStatus.OK

@blueprint.route("", methods=["POST"])
@DataValidator(TaskCreateModel)
@handle_exceptions_and_session
def create_product(session, data: TaskCreateModel):
    response =  TaskService.create(session, data)
    return success_response(message=response), HTTPStatus.CREATED

@blueprint.route("/<string:id>", methods=["PATCH"])
@DataValidator(TaskUpdateModel)
@handle_exceptions_and_session
def update_product(session, data: TaskUpdateModel, id: str):
    response = TaskService.update(session, data, id)
    return success_response(message=response), HTTPStatus.OK

@blueprint.route("/<string:id>", methods=["DELETE"])
@handle_exceptions_and_session
def delete_product(session, id: str):
    response = TaskService.delete(session, id)
    return success_response(message=response), HTTPStatus.OK
