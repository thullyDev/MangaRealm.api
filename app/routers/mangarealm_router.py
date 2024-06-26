from typing import Any, Dict, List, Optional, Tuple, Union
from fastapi import APIRouter
from fastapi.responses import JSONResponse
from app.database import database
from app.database.models import SetList
from app.handlers import response_handler as response, storage
from app.database.cache import cache 
import requests
import pprint
import ast
import datetime

from app.resources.config import MANGANATO_API_URL
from app.resources.errors import SUCCESSFUL

router: APIRouter = APIRouter(prefix="/api")

# @router.post("/profile_details/")
# def profile_details(email: str) -> JSONResponse:
# 	return response.successful_response(data={ "message": "" })

@router.post("/add_to_list")
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

@router.post("/remove_from_list")
def remove_from_list(email: str, slug: str) -> JSONResponse:
	user = database.get_user(key="email", entity=email)

	if not user:
		return response.forbidden_response(data={ "message": "invalid user"}) 

	conditions = [("useremail", email), ("slug", slug)]
	res = database.remove_from_list(conditions=conditions)

	if not res:
		return response.crash_response(data={ "message": "failed to  remove from list, may already be in the list" })

	return response.successful_response(data={ "message": "removed from list" })

@router.post("/change_user_info")
def change_user_info(email: str, data: str) -> JSONResponse:
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

@router.post("/upload_user_profile_image")
def upload_user_profile_image(email: str, image: str) -> JSONResponse:
	user = database.get_user(key="email", entity=email)

	if not user:
		return response.forbidden_response(data={ "message": "invalid user"})

	name, base64 = process_image(image, user.username)
	profile_image_url = storage.upload_base64_image(name=name, base64Str=base64)

	if not profile_image_url:
		return response.crash_response(data={ "message": "failed to upload image" })

	data = { "key": "profile_image_url", "value": profile_image_url }
	res = update_data([ data ], key="email", entity=email)

	if not res:
		return response.crash_response(data={ "message": "failed" })

	return response.successful_response(data={ "message": "updated" })

def valid_keys(attributes: List[Dict[str, Any]]) -> Tuple[bool, str]:
	keys = [ "email", "profile_image_url", "username", "password" "deleted" ]

	for item in attributes:
		key = item["key"]
		value = item["value"]

		if key not in keys:
			return False, "forbidden"

		if key == "password":
			if len(value) < 10:
				return False, "password should have atleast 10 characters" 

	return True, ""

def get_manga(slug: str) -> Optional[Dict[str, Any]]:
	url = f"{MANGANATO_API_URL}/{slug}"
	response = requests.get(url)

	if response.status_code != SUCCESSFUL:
		return None

	return response.json()["data"]["manga"]

def update_data(attributes: List[Dict[str, Any]], **kwargs) -> bool:
	data: List[tuple[str, Any]] = []
	for item in attributes:
		data.append((item["key"], item["value"]))
	return database.update_user(data=data, **kwargs)

def process_image(image: str, username: str):
	current_time = datetime.datetime.now().strftime("%d-%m-%Y-%w-%d-%H-%M-%S-%f")
	name = f"{username}-{current_time}"
	return name, image.replace("data:image/jpeg;base64,", "").replace("data:image/png;base64,", "")

