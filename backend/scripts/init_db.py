import asyncio
from pathlib import Path
import sys

# Add parent directory to path to import dependencies
sys.path.append(str(Path(__file__).parent.parent))

from routes.dependencies import get_db, engine
from sqlalchemy import text


async def execute_schema():
    print("Reading schema file...")
    schema_path = Path(__file__).parent.parent.parent / 'mysql.sql'
    
    with open(schema_path, 'r') as f:
        schema = f.read()

    print("Executing schema...")
    async with engine.begin() as conn:
        # Split on semicolon to execute multiple statements
        statements = [s.strip() for s in schema.split(';') if s.strip()]
        for statement in statements:
            try:
                await conn.execute(text(statement))
                print(f"Executed: {statement[:50]}...")
            except Exception as e:
                print(f"Error executing statement: {statement[:50]}...")
                print(f"Error: {str(e)}")
                raise

    print("Schema execution completed successfully!")


if __name__ == "__main__":
    asyncio.run(execute_schema())