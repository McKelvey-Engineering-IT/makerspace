import os
import pymysql
import pyodbc
from dotenv import load_dotenv

class MySQLToMSSQLMigrator:
    def __init__(self):
        load_dotenv()

        self.mysql_conn = pymysql.connect(
            host=os.getenv("MYSQL_DB_SERVER"),
            user=os.getenv("MYSQL_DB_USER"),
            password=os.getenv("MYSQL_DB_PASSWORD"),
            database=os.getenv("MYSQL_DB"),
            port=3306,
            cursorclass=pymysql.cursors.Cursor
        )

        mssql_driver = "ODBC Driver 18 for SQL Server"
        mssql_server = os.getenv("MSSQL_DB_SERVER")
        mssql_db = os.getenv("MSSQL_DB").replace('"', '')
        mssql_user = os.getenv("MSSQL_DB_USER")
        mssql_pass = os.getenv("MSSQL_DB_PASSWORD")

        self.mssql_conn = pyodbc.connect(
            f"DRIVER={{{mssql_driver}}};SERVER={mssql_server};DATABASE={mssql_db};UID={mssql_user};PWD={mssql_pass};Encrypt=no",
            autocommit=True
        )

    def escape(self, val):
        if val is None:
            return 'NULL'
        elif isinstance(val, bytes):
            return f"0x{val.hex()}"
        elif isinstance(val, str):
            return f"'{val.replace(chr(39), chr(39)+chr(39))}'"
        return f"'{str(val)}'"

    def transfer_selected_tables(self):
        with self.mysql_conn.cursor() as mysql_cursor, self.mssql_conn.cursor() as mssql_cursor:
            # USERS
            print("🚚 Migrating: users")
            mysql_cursor.execute("SELECT * FROM `users`")
            rows = mysql_cursor.fetchall()
            columns = [desc[0] for desc in mysql_cursor.description]

            for row in rows:
                values = ", ".join(self.escape(val) for val in row)
                col_clause = ", ".join(f"[{col}]" for col in columns)
                sql = f"INSERT INTO [dbo].[users] ({col_clause}) VALUES ({values})"
                try:
                    mssql_cursor.execute(sql)
                except Exception as e:
                    print(f"❌ Failed inserting into users: {e}")

            # ACCESS_LOG with ID mapping
            print("🚚 Migrating: access_log (tracking ID map)")
            mysql_cursor.execute("SELECT * FROM `access_log`")
            rows = mysql_cursor.fetchall()
            columns = [desc[0] for desc in mysql_cursor.description]
            id_index = columns.index("ID")
            access_id_map = {}

            for row in rows:
                original_id = row[id_index]
                insert_cols = [col for col in columns if col != "ID"]
                insert_vals = [self.escape(row[columns.index(col)]) for col in insert_cols]
                col_clause = ", ".join(f"[{col}]" for col in insert_cols)
                val_clause = ", ".join(insert_vals)

                sql = f"INSERT INTO [dbo].[access_log] ({col_clause}) OUTPUT INSERTED.ID VALUES ({val_clause})"
                try:
                    mssql_cursor.execute(sql)
                    new_id = mssql_cursor.fetchone()[0]
                    access_id_map[original_id] = new_id
                except Exception as e:
                    print(f"❌ Failed inserting into access_log: {e}")

            # BADGE_SNAPSHOT using remapped AccessLogID
            print("🚚 Migrating: badge_snapshot (remapping AccessLogID)")
            mysql_cursor.execute("SELECT * FROM `badge_snapshot`")
            rows = mysql_cursor.fetchall()
            columns = [desc[0] for desc in mysql_cursor.description]
            id_index = columns.index("ID")
            fk_index = columns.index("AccessLogID")

            insert_cols = [col for col in columns if col != "ID"]
            for row in rows:
                old_fk = row[fk_index]
                new_fk = access_id_map.get(old_fk)

                if new_fk is None:
                    print(f"⚠️ Skipping badge_snapshot with missing AccessLogID: {old_fk}")
                    continue

                # Prepare row for insert (skipping ID and replacing FK)
                insert_vals = []
                for col in insert_cols:
                    val = row[columns.index(col)]
                    if col == "AccessLogID":
                        val = new_fk
                    insert_vals.append(self.escape(val))

                col_clause = ", ".join(f"[{col}]" for col in insert_cols)
                val_clause = ", ".join(insert_vals)
                sql = f"INSERT INTO [dbo].[badge_snapshot] ({col_clause}) VALUES ({val_clause})"
                try:
                    mssql_cursor.execute(sql)
                except Exception as e:
                    print(f"❌ Failed inserting into badge_snapshot: {e}")

            print("Migration complete for users, access_log, and badge_snapshot.")

    def close(self):
        self.mysql_conn.close()
        self.mssql_conn.close()

if __name__ == "__main__":
    migrator = MySQLToMSSQLMigrator()
    try:
        migrator.transfer_selected_tables()
    finally:
        migrator.close()
