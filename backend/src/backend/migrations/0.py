
async def migrate(connection):
    await connection.execute("""
        CREATE TABLE IF NOT EXISTS vendors (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            publiic_username VARCHAR(40) NOT NULL UNIQUE,
            private_username VARCHAR(40) NOT NULL UNIQUE,
            secret_phrase VARCHAR(250) NOT NULL UNIQUE,
            password_hash VARCHAR(60),
            public_key TEXT
        );
    """)

    await connection.execute("""
        CREATE TABLE IF NOT EXISTS categories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            category VARCHAR(100) NOT NULL UNIQUE,
            info VARCHAR(250)
        );
    """)

    await connection.execute("""
        CREATE TABLE IF NOT EXISTS subcategories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            category_id INTEGER,
            sub_category VARCHAR(100) NOT NULL UNIQUE,
            info TEXT,
            FOREIGN KEY (category_id) REFERENCES categories(id)
        );
    """)


async def valid_migration(connection):
    return True