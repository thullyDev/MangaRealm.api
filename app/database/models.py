from datetime import datetime
from typing import Any, Optional, Tuple, Union

#! please use this is order when initializing using a tuple, or else the attributes wont match


class Base:
	def entities_to_tuple(self) -> Tuple:
		return tuple(vars(self).values())

	def keys_to_tuple(self, as_strings=False) -> Tuple[str, ...]:
		return tuple(self.__dict__.keys()) 

	def string_tuple(self, type) -> str:
		if type == "keys":
			return str(self.keys_to_tuple())

		if type == "entities":
			return str(self.entities_to_tuple())

		raise Exception(f"no such type: {type}, try keys or entities")

class User(Base):
	def __init__(self, user: Tuple[
			int,
			str,
			str,
			str,
			bool,
			datetime,
			Optional[str],
			str]
		):
		self.id: int = user[0] 
		self.username: str = user[1]
		self.email: str = user[2]
		self.password: str = user[3]
		self.deleted: bool = user[4]
		self.profile_image_url: Optional[str] = user[6]
		self.token: Optional[str] = user[7]

class SetUser(Base):
	def __init__(self, user: Tuple[str, ...]):
		self.username: str = user[0]
		self.email: str = user[1]
		self.password: str = user[2]
		self.token: str = user[3]

class AddList(Base):
	def __init__(self, data: Tuple[str, ...]):
		self.id: str = data[0]
		self.useremail: str = data[1]
		self.slug: str = data[2]
		self.title: str = data[3]
		self.created_at: str = data[4]
		self.image_url: str = data[5]


class SetList(Base):
	def __init__(self, data: Tuple[str, ...]):
		self.useremail: str = data[0]
		self.slug: str = data[1]
		self.title: str = data[2]
		self.image_url: str = data[3]


