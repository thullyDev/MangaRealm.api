from typing import Any, Optional, Dict
from fastapi import APIRouter, Request
from fastapi.datastructures import URL
from fastapi.responses import JSONResponse
from app.database.models import SetUser
from app.handlers import response_handler as response
from app.database import database
from app.database.cache import cache 

router: APIRouter = APIRouter(prefix="/api")

# @router.post("/signup/")
# def signup(request: Request, username: str, email: str, password: str, confirm: str) -> JSONResponse:
#      return response.successful_response(data={ "message": "sent verify link to your email, please verify" })