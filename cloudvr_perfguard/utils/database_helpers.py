"""
Database helper utilities
Removes duplicate code patterns and provides reusable database operations
"""

from typing import Any, Dict, List, Optional
import aiosqlite


async def rows_to_dicts(cursor: aiosqlite.Cursor) -> List[Dict[str, Any]]:
    """
    Convert database cursor rows to list of dictionaries

    Args:
        cursor: Database cursor after executing a query

    Returns:
        List of dictionaries with column names as keys

    Example:
        cursor = await db.execute("SELECT * FROM users")
        users = await rows_to_dicts(cursor)
        # [{"id": 1, "name": "Alice"}, {"id": 2, "name": "Bob"}]
    """
    # Extract column names from cursor description
    columns = [description[0] for description in cursor.description]

    # Fetch all rows
    rows = await cursor.fetchall()

    # Convert each row to dictionary
    return [dict(zip(columns, row)) for row in rows]


async def row_to_dict(cursor: aiosqlite.Cursor) -> Optional[Dict[str, Any]]:
    """
    Convert single database cursor row to dictionary

    Args:
        cursor: Database cursor after executing a query

    Returns:
        Dictionary with column names as keys, or None if no row found

    Example:
        cursor = await db.execute("SELECT * FROM users WHERE id = ?", (1,))
        user = await row_to_dict(cursor)
        # {"id": 1, "name": "Alice"}
    """
    # Extract column names from cursor description
    columns = [description[0] for description in cursor.description]

    # Fetch one row
    row = await cursor.fetchone()

    if not row:
        return None

    # Convert row to dictionary
    return dict(zip(columns, row))


async def execute_and_fetch_one(
    connection: aiosqlite.Connection,
    query: str,
    params: tuple = ()
) -> Optional[Dict[str, Any]]:
    """
    Execute query and return single result as dictionary

    Args:
        connection: Database connection
        query: SQL query to execute
        params: Query parameters

    Returns:
        Dictionary with query result, or None if no result

    Example:
        user = await execute_and_fetch_one(
            conn,
            "SELECT * FROM users WHERE id = ?",
            (1,)
        )
    """
    cursor = await connection.execute(query, params)
    return await row_to_dict(cursor)


async def execute_and_fetch_all(
    connection: aiosqlite.Connection,
    query: str,
    params: tuple = ()
) -> List[Dict[str, Any]]:
    """
    Execute query and return all results as list of dictionaries

    Args:
        connection: Database connection
        query: SQL query to execute
        params: Query parameters

    Returns:
        List of dictionaries with query results

    Example:
        users = await execute_and_fetch_all(
            conn,
            "SELECT * FROM users WHERE age > ?",
            (18,)
        )
    """
    cursor = await connection.execute(query, params)
    return await rows_to_dicts(cursor)
