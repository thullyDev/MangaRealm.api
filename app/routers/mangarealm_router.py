from typing import Any, Dict, Optional
from fastapi import APIRouter
from fastapi.responses import JSONResponse
from app.database import database
from app.database.models import SetList
from app.handlers import response_handler as response
from app.database.cache import cache 
import requests
import pprint

from app.resources.config import MANGANATO_API_URL
from app.resources.errors import SUCCESSFUL

router: APIRouter = APIRouter(prefix="/api")

# @router.post("/profile_details/")
# def profile_details(email: str) -> JSONResponse:
# 	return response.successful_response(data={ "message": "" })

@router.post("/add_list")
def add_to_list(email: str, slug: str) -> JSONResponse:
	user = database.get_user(key="email", entity=email)

	if not user:
		return response.forbidden_response(data={ "message": "invalid user"}) 

	manga = get_manga(slug)

	print(manga)

	if not manga:
		return response.bad_request_response(data={ "message": "invalid manga" })

	title = manga["title"]
	image_url = manga["image_url"]
	list_manga = SetList((
		email,
		slug,
		title,
		image_url
	))
	res = database.add_to_list(list=list_manga)

	if not res:
		return response.crash_response(data={ "message": "failed to add to list, may already be in the list" })

	return response.successful_response(data={ "message": "added to list" })

def get_manga(slug: str) -> Optional[Dict[str, Any]]:
	url = f"{MANGANATO_API_URL}/{slug}"
	response = requests.get(url)

	if response.status_code != SUCCESSFUL:
		return None

	return response.json()["data"]["manga"]