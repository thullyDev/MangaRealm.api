from typing import Any, Dict, List, Optional
from app.database.models import Base, SetUser, User, SetList
from app.resources.config import SQL_URL
from .sequel.postgresDatabase import PostgresDB 

psqlDB: PostgresDB = PostgresDB(SQL_URL)  

def get_user(*, key: str, entity: str) -> Optional[User]:
	query = f"select * from \"user\" where {key} = '{entity}';"
	response = psqlDB.fetch(query=query)

	if not response:
		return None

	return User(response[0])

def set_user(user: SetUser) -> bool:

	return set_model(model=user, table="user") 

def update_user(*, key: str, entity: str, data: List[tuple[str, Any]]) -> bool:
	update_data = [f"set {column} = {repr(value)}" for column, value in data ]
	update_string = " , ".join(update_data)
	query = f"""
				update "user" 
				{update_string}
				where {key} = '{entity}';
			""".strip()
	return psqlDB.execute(query)

def add_to_list(list: SetList) -> bool:
	return set_model(model=list, table="list")

def set_model(*, model: Base, table: str) -> bool:
	keys = model.string_tuple("keys").replace("'", '')
	entities = model.string_tuple("entities").replace("None", "NULL").replace('"', "'")
	query = f"""
				insert into "{table}" {keys}
				values {entities};
			""".strip()
	return psqlDB.execute(query)

