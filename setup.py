from app.database.sequel.postgresDatabase import PostgresDB 
from app.resources.config import SQL_URL

# this script sets up the database requirements for the project.
# please make sure the user has create table privileges (schema public), or just use the root user

psqlDB: PostgresDB = PostgresDB(SQL_URL)  

def setup():
	setup_query = f"""
		CREATE TABLE "user" (
		    id SERIAL PRIMARY KEY, 
		    username VARCHAR(100) NOT NULL, 
		    email VARCHAR(100) UNIQUE NOT NULL, 
		    password VARCHAR(100) NOT NULL CHECK (LENGTH(password) >= 10), 
		    deleted BOOLEAN DEFAULT FALSE, 
		    created_at TIMESTAMP DEFAULT NOW(), 
		    profile_image_url VARCHAR(300), 
		    token VARCHAR(300)
		);

		CREATE TABLE "list" (
			    id SERIAL PRIMARY KEY,
			    useremail VARCHAR(100) NOT NULL,
			    slug VARCHAR(300) UNIQUE NOT NULL,
			    title VARCHAR(300) NOT NULL,
			    image_url VARCHAR(400) NOT NULL,
			    created_at TIMESTAMP DEFAULT NOW()
			);
			""".strip()
	psqlDB.execute(setup_query)


if __name__ == "__main__":
	setup()



