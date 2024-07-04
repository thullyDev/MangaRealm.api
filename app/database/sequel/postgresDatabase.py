from typing import List, Optional, Tuple, Union
import psycopg2


class PostgresDB: 	
	def __init__(self, DB_URL: str) -> None:
		self.conn = psycopg2.connect(DB_URL)
		self.cursor = self.conn.cursor()

	def execute(self, query: str, params=None) -> Union[bool, Tuple]:
		try:
			print(params)
			self.cursor.execute(query=query, vars=params)
			self.conn.commit()
			return True
		except psycopg2.Error as e:
			self.conn.rollback()

			print("Postgres Error: ", e)
			if "duplicate" in str(e):
				return False, "duplicate"



			return False

	def fetch(self, query: str, params=None) -> Optional[List[Tuple]]:
		try:
			self.cursor.execute(query=query, vars=params)
			return self.cursor.fetchall()
		except psycopg2.Error as e:
			self.conn.rollback()

			print("Postgres Error: ", e)

			return None

	def close_connection(self):
		self.cursor.close()
		self.conn.close()
