import argparse
import sqlite3

from mcp.server.fastmcp import FastMCP

mcp = FastMCP('sqlite-demo')

def init_db():
    conn = sqlite3.connect('demo.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS people (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            age INTEGER NOT NULL,
            profession TEXT NOT NULL
        )
    ''')
    conn.commit()
    return conn, cursor

@mcp.tool()
def add_data(name: str, age: int, profession: str) -> bool:
    """Add new data to the people table.

    Args:
        name (str): Name of the person.
        age (int): Age of the person.
        profession (str): Profession of the person.
    Returns:
        bool: True if data was added successfully, False otherwise.
    Example:
        >>> add_data('Roger Federer', 45, 'Professional Tennis Player')
        True
    """
    conn, cursor = init_db()
    try:
        cursor.execute(
            "INSERT INTO people (name, age, profession) VALUES (?, ?, ?)",
            (name, age, profession)
        )
        conn.commit()
        return True
    except sqlite3.Error as e:
        print(f"Error adding data: {e}")
        return False
    finally:
        conn.close()

@mcp.tool()
def read_data(query: str = "SELECT * FROM people") -> list[dict]:
    """Read data from the people table using a SQL SELECT query and return as a list of dicts.

    Args:
        query (str, optional): SQL SELECT query. Defaults to "SELECT * FROM people".
            Examples:
            - "SELECT * FROM people"
            - "SELECT name, age FROM people WHERE age > 25"
            - "SELECT * FROM people ORDER BY age DESC"
    
    Returns:
        list: List of dictionaries containing the query results.
              For default query, dict format is {"id": ..., "name": ..., "age": ..., "profession": ...}
    
    Example:
        >>> # Read all records
        >>> read_data()
        [
            {"id": 1, "name": "John Doe", "age": 30, "profession": "Engineer"},
            {"id": 2, "name": "Alice Smith", "age": 25, "profession": "Developer"}
        ]
        
        >>> # Read with custom query
        >>> read_data("SELECT name, profession FROM people WHERE age < 30")
        [
            {"name": "Alice Smith", "profession": "Developer"}
        ]
    """
    if not query or not query.strip():
        query = "SELECT * FROM people"
    conn, cursor = init_db()
    try:
        cursor.execute(query)
        columns = [desc[0] for desc in cursor.description]
        rows = cursor.fetchall()
        result = [dict(zip(columns, row)) for row in rows]
        return result
    except sqlite3.Error as e:
        print(f"Error reading data: {e}")
        return []
    finally:
        conn.close()

@mcp.tool()
def delete_person_by_name(name: str) -> bool:
    """Delete a record from the people table by name if it exists.

    Args:
        name (str): The name of the person to delete.
    Returns:
        bool: True if a record was deleted, False otherwise.
    Example:
        >>> delete_person_by_name('John Doe')
        True
    """
    conn, cursor = init_db()
    try:
        cursor.execute("DELETE FROM people WHERE name = ?", (name,))
        conn.commit()
        return cursor.rowcount > 0
    except sqlite3.Error as e:
        print(f"Error deleting data: {e}")
        return False
    finally:
        conn.close()

@mcp.tool()
def update_person(id: int, name: str = None, age: int = None, profession: str = None) -> bool:
    """Update a person's record in the people table by id. You can update name, age, and/or profession.

    Args:
        id (int): The id of the person to update.
        name (str, optional): The new name. Defaults to None (no change).
        age (int, optional): The new age. Defaults to None (no change).
        profession (str, optional): The new profession. Defaults to None (no change).
    Returns:
        bool: True if a record was updated, False otherwise.
    Example:
        >>> update_person(1, name='Rafael Nadal', age=41)
        True
    """
    conn, cursor = init_db()
    try:
        fields = []
        values = []
        if name is not None:
            fields.append("name = ?")
            values.append(name)
        if age is not None:
            fields.append("age = ?")
            values.append(age)
        if profession is not None:
            fields.append("profession = ?")
            values.append(profession)
        if not fields:
            return False  # Nothing to update
        values.append(id)
        query = f"UPDATE people SET {', '.join(fields)} WHERE id = ?"
        cursor.execute(query, tuple(values))
        conn.commit()
        return cursor.rowcount > 0
    except sqlite3.Error as e:
        print(f"Error updating data: {e}")
        return False
    finally:
        conn.close()

if __name__ == "__main__":
    # Start the server
    print("🚀Starting server... ")

    # Debug Mode
    #  uv run mcp dev server.py

    # Production Mode
    # uv run server.py --server_type=sse

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--server_type", type=str, default="sse", choices=["sse", "stdio"]
    )

    args = parser.parse_args()
    mcp.run(args.server_type)



# # Example usage
# if __name__ == "__main__":
#     # Example INSERT query
#     insert_query = """
#     INSERT INTO people (name, age, profession)
#     VALUES ('John Doe', 30, 'Engineer')
#     """
    
#     # Add data
#     if add_data(insert_query):
#         print("Data added successfully")
    
#     # Read all data
#     results = read_data()
#     print("\nAll records:")
#     for record in results:
#         print(record)
#         print(record)
