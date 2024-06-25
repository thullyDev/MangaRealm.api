from typing import Any, Dict, List, Optional, Union
from fastapi import APIRouter
from fastapi.responses import JSONResponse
from app.database import database
from app.database.models import SetList
from app.handlers import response_handler as response
from app.database.cache import cache 
import requests
import pprint
import ast

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

@router.post("/change_user_data")
def change_user_data(email: str, data: str) -> JSONResponse:
	attributes: List[Dict[str, Union[str, bool]]] = ast.literal_eval(data.strip("'"))
	isvalid, isvalid_msg = valid_keys(attributes)

	if not isvalid:
		return response.forbidden_response(data={ "message": isvalid_msg })

	user = database.get_user(key="email", entity=email)

	if not user:
		return response.forbidden_response(data={ "message": "invalid user"}) 

	res = update_data(attributes, key="email", entity=email)

	if not res:
		return response.crash_response(data={ "message": "failed" })

	return response.successful_response(data={ "message": "updated" })

def valid_keys(attributes):
	keys = [ "email", "profile_image_url", "username", "password" "deleted" ]

	for item in attributes:
		key = item["key"]
		value = item["value"]

		if key not in keys:
			return False, "forbidden"

		if key == "password":
			if len(password) < 10:
				return False, "password should have atleast 10 characters" 

	return True, ""

def get_manga(slug: str) -> Optional[Dict[str, Any]]:
	url = f"{MANGANATO_API_URL}/{slug}"
	response = requests.get(url)

	if response.status_code != SUCCESSFUL:
		return None

	return response.json()["data"]["manga"]

def update_data(attributes: List[ Dict[str, Union[str, bool]]], **kwargs) -> bool:
	data: List[tuple[str, Any]] = [(item["key"], item["value"]) for item in attributes]
	return database.update_user(data=data, **kwargs)