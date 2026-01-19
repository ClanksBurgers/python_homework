import sqlite3

try:
    connection = sqlite3.connect('../db/magazines.db')
    cursor = connection.cursor()
    
    cursor.execute("PRAGMA foreign_keys = 1")

    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='publishers'")
    if not cursor.fetchone():
        cursor.execute('''
            CREATE TABLE publishers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL
            )
        ''')

        cursor.execute('''
            CREATE TABLE magazines (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL,
                publisher_id INTEGER NOT NULL,
                FOREIGN KEY (publisher_id) REFERENCES publishers(id)
            )
        ''')

        cursor.execute('''
            CREATE TABLE subscribers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                address TEXT NOT NULL
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE subscriptions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                magazine_id INTEGER NOT NULL,
                subscriber_id INTEGER NOT NULL,
                expiration_date TEXT NOT NULL,
                FOREIGN KEY (magazine_id) REFERENCES magazines(id),
                FOREIGN KEY (subscriber_id) REFERENCES subscribers(id)
            )
        ''')
        
        connection.commit()
        print("Tables created successfully!")
    else:
        print("Tables already exist.")

    def add_publisher(name):
        try:
            cursor.execute("INSERT INTO publishers (name) VALUES (?)", (name,))
            connection.commit()
            print(f"Added publisher: {name}")
        except sqlite3.IntegrityError:
            print(f"Publisher '{name}' already exists.")
        except Exception as e:
            print(f"Error adding publisher: {e}")

    def add_magazine(name, publisher_id):
        try:
            cursor.execute("INSERT INTO magazines (name, publisher_id) VALUES (?, ?)", (name, publisher_id))
            connection.commit()
            print(f"Added magazine: {name}")
        except sqlite3.IntegrityError:
            print(f"Magazine '{name}' already exists or publisher_id is invalid.")
        except Exception as e:
            print(f"Error adding magazine: {e}")

    def add_subscriber(name, address):
        try:
            cursor.execute("SELECT id FROM subscribers WHERE name = ? AND address = ?", (name, address))
            if cursor.fetchone():
                print(f"Subscriber '{name}' at '{address}' already exists.")
                return
            cursor.execute("INSERT INTO subscribers (name, address) VALUES (?, ?)", (name, address))
            connection.commit()
            print(f"Added subscriber: {name}, {address}")
        except Exception as e:
            print(f"Error adding subscriber: {e}")

    def add_subscription(magazine_id, subscriber_id, expiration_date):
        try:
            cursor.execute("INSERT INTO subscriptions (magazine_id, subscriber_id, expiration_date) VALUES (?, ?, ?)", 
                         (magazine_id, subscriber_id, expiration_date))
            connection.commit()
            print(f"Added subscription for magazine_id {magazine_id}, subscriber_id {subscriber_id}")
        except sqlite3.IntegrityError:
            print(f"Subscription already exists or foreign key is invalid.")
        except Exception as e:
            print(f"Error adding subscription: {e}")

    print("\n--- Populating tables ---")

    add_publisher("Condé Nast")
    add_publisher("Hearst Media")
    add_publisher("Penguin Random House")

    add_magazine("Vogue", 1)
    add_magazine("Wired", 1)
    add_magazine("Good Housekeeping", 2)

    add_subscriber("John Smith", "123 Main St, NYC")
    add_subscriber("Jane Doe", "456 Oak Ave, LA")
    add_subscriber("Bob Johnson", "789 Elm St, Chicago")

    add_subscription(1, 1, "2025-12-31")
    add_subscription(1, 2, "2026-06-30")
    add_subscription(2, 2, "2025-09-15")
    add_subscription(3, 3, "2026-03-20")
    
    #Query 1
    print("\n--- Query 1: All Subscribers ---")
    cursor.execute("SELECT * FROM subscribers")
    subscribers = cursor.fetchall()
    for row in subscribers:
        print(row)
    
    #Query 2
    print("\n--- Query 2: All Magazines (sorted by name) ---")
    cursor.execute("SELECT * FROM magazines ORDER BY name")
    magazines = cursor.fetchall()
    for row in magazines:
        print(row)
    
    #Query 3
    print("\n--- Query 3: Magazines by Publisher (Condé Nast) ---")
    cursor.execute('''
        SELECT m.id, m.name, p.name as publisher_name
        FROM magazines m
        JOIN publishers p ON m.publisher_id = p.id
        WHERE p.name = ?
    ''', ("Condé Nast",))
    magazines_by_publisher = cursor.fetchall()
    for row in magazines_by_publisher:
        print(row)
    
    connection.close()
except Exception as e:
    print(f"An error occurred: {e}")

