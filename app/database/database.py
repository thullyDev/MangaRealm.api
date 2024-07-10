from typing import Any, Dict, List, Optional, Tuple, Union

from fastapi import responses
from app.database.models import AddList, Base, SetUser, User, SetList
from app.resources.config import SQL_URL
from .sequel.postgresDatabase import PostgresDB 

psqlDB: PostgresDB = PostgresDB(SQL_URL)  

def update_user(*, key: str, entity: str, data: List[tuple[str, Any]]) -> Union[bool, str]:
	update_data = [f"SET {column} = {repr(value)}" for column, value in data ]
	update_string = " , ".join(update_data)
	query = f"""
				UPDATE "user" 
				{update_string}
				WHERE {key} = '{entity}';
			""".strip()

	return psqlDB.execute(query)
	
def get_list_items(*, key: str, entity: str, filterWords: str = "") -> List[AddList]:
	searchQuery = "" if filterWords == "" else  f" AND title ILIKE '%{filter}%'"
	query = f"SELECT * FROM \"list\" WHERE {key} = '{entity}' {searchQuery};"
	response = psqlDB.fetch(query=query)

	if not response:
		return []

	return [AddList(item) for item in response]

def get_user(*, key: str, entity: str) -> Optional[User]:
	query = f"SELECT * FROM \"user\" WHERE {key} = '{entity}';"
	response = psqlDB.fetch(query=query)

	if not response:
		return None

	return User(response[0])

def set_user(user: SetUser) -> Union[bool, str]: return set_model(model=user, table="user") 

def add_to_list(list: SetList) -> Union[bool, str]: return set_model(model=list, table="list")

def remove_from_list(conditions: List[Tuple[str, Any]]) -> Union[bool, str]:
	conditions_query = " AND ".join([
		f"{key} = '{entity}'" 
		for key, entity in conditions
	])
	query = f"""
				DELETE FROM "list"
				WHERE {conditions_query}; 
			"""
	return psqlDB.execute(query=query)

def set_model(*, model: Base, table: str) -> Union[bool, str]:
	keys = model.string_tuple("keys").replace("'", '')
	entities = model.string_tuple("entities").replace("None", "NULL").replace('"', "'")
	query = f"""
				INSERT INTO "{table}" {keys}
				VALUES {entities};
			""".strip()
	return psqlDB.execute(query)

