import ast
from urllib.parse import parse_qs, urlparse
import uuid
import hashlib
import datetime
from typing import Any, Dict, List, Optional, Tuple, Union

from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
import requests

from app.database import database
from app.database.models import SetList, User
from app.handlers import response_handler as response, storage
from app.resources.config import MANGANATO_API_URL
from app.resources.errors import SUCCESSFUL
from app.resources.misc import paginate_items


router: APIRouter = APIRouter(prefix="/api")

async def validator(*, request: Request, callnext) -> JSONResponse:
	headers = request.headers
	auth_token = headers.get("auth_token")

	# if not auth_token:
	# 	return response.forbidden_response(data={ "message": "bad auth_token" })

	parsed_url = urlparse(request.url._url)
	query_params = parse_qs(parsed_url.query)
	email = query_params.get('email', [None])[0]

	if not email:
		return response.bad_request_response()

	user = database.get_user(key="email", entity=email)
	
	if not user:
		return response.forbidden_response(data={ "message": "invalid user"})
	
	# if user.token != auth_token:
	# 	return response.forbidden_response(data={ "message": "user not up to date with the auth_token, so they should authenticate first"})
	
	user.token = generate_unique_token()
	res = database.update_user(data=[ ( "token", user.token) ], key="email", entity=email)
	
	if not res:
		return response.crash_response(data={ "message": "the token updating failed" }) 
	
	request.state.auth_token = user.token 

	return await callnext(request)

@router.post("/profile_details/")
def profile_details(request: Request, email: str, list_page: str = "1", keywords: str = "") -> JSONResponse:
	page = 1

	try:
		page = int(list_page) 
	except Exception as e:
		print(e)
	
	user = database.get_user(key="email", entity=email)

	if not user:
		return response.forbidden_response(data={ "message": "invalid email" })

	profile_data = get_profile_data(user, page=page, keywords=keywords)
	token = request.state.auth_token 
	return response.successful_response(data={ 
		"message": "successfully got the user data", 
		"data": profile_data, 
		"auth_token": token
	})

def get_profile_data(user: User, page: int, keywords: str):
	items = database.get_list_items(key="useremail", entity=user.email, filterWords=keywords)
	data, pagination = paginate_items(data=items, page=page, limit=20)
	items = []
	user_data = user.__dict__

	del user_data["password"]
	del user_data["token"]

	user_data["created_at"] = user_data["created_at"].strftime('%Y-%m-%d %H:%M:%S.%f')
	
	for item in data:
		item.created_at = str(item.created_at)
		items.append(item.__dict__)
		
	return {
		"profile": user_data,
		"list": items,
		"pagination": pagination,
	}

@router.post("/add_to_list")
def add_to_list(request: Request, email: str, slug: str) -> JSONResponse:
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

	if type(res) is str:
		conditions = [("useremail", email), ("slug", slug)]
		database.remove_from_list(conditions=conditions)
		return response.successful_response(data={ "message": "added to list", "auth_token": request.headers.get("auth_token"), "data": { "isAdded": False } })

	if not res:
		return response.crash_response(data={ "message": "failed to add to list, may already be in the list" })
	
	return response.successful_response(data={ "message": "added to list", "auth_token": request.headers.get("auth_token"), "data": { "isAdded": True } })

@router.post("/remove_from_list")
def remove_from_list(request: Request, email: str, slug: str) -> JSONResponse:
	conditions = [("useremail", email), ("slug", slug)]
	res = database.remove_from_list(conditions=conditions)

	if not res:
		return response.crash_response(data={ "message": "failed to  remove from list, may not be in the list" })

	return response.successful_response(data={ "message": "removed from list", "auth_token": request.headers.get("auth_token") })

@router.post("/change_user_info")
def change_user_info(request: Request, email: str, data: str) -> JSONResponse:
	attributes: List[Dict[str, Union[str, bool]]] = ast.literal_eval(data.strip("'"))
	isvalid, isvalid_msg = valid_keys(attributes)

	if not isvalid:
		return response.forbidden_response(data={ "message": isvalid_msg })

	res = update_data(attributes, key="email", entity=email)

	if not res:
		return response.crash_response(data={ "message": "failed" })

	return response.successful_response(data={ "message": "updated", "auth_token": request.headers.get("auth_token") })

@router.post("/upload_user_profile_image")
def upload_user_profile_image(request: Request, user, email: str, image: str) -> JSONResponse:
	#! image should be a base64 image
	name, base64 = process_image(image, user.username)
	profile_image_url = storage.upload_base64_image(name=name, base64Str=base64)

	if not profile_image_url:
		return response.crash_response(data={ "message": "failed to upload image", "auth_token": request.headers.get("auth_token") })

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

import pprint
def get_manga(slug: str) -> Optional[Dict[str, Any]]:
	url = f"{MANGANATO_API_URL}/{slug}"
	response = requests.get(url)

	if response.status_code != SUCCESSFUL:
		return None

	data = response.json()["data"]["manga"]
	pprint.pprint(data)
	return data

def update_data(attributes: List[Dict[str, Any]], **kwargs) -> Union[bool, str]:
	data: List[tuple[str, Any]] = []
	for item in attributes:
		data.append((item["key"], item["value"]))
	return database.update_user(data=data, **kwargs)

def process_image(image: str, username: str):
	current_time = datetime.datetime.now().strftime("%d-%m-%Y-%w-%d-%H-%M-%S-%f")
	name = f"{username}-{current_time}"
	return name, image.replace("data:image/jpeg;base64,", "").replace("data:image/png;base64,", "")

def generate_unique_token(length: int = 250) -> str:
	random_uuid = uuid.uuid4()
	uuid_bytes = random_uuid.bytes
	hashed_token = hashlib.sha256(uuid_bytes).hexdigest()
	while len(hashed_token) < length:
		hashed_token += hashlib.sha256(hashed_token.encode()).hexdigest()
	
	hashed_token = hashed_token[:length]
	
	return hashed_token

