import os, urllib.parse
from pydantic import BaseModel, Field

class Settings(BaseModel):
    MESSAGE_STREAM_DELAY: int = 10
    MESSAGE_STREAM_RETRY_TIMEOUT: int = 15000
    IS_LOCAL: bool = Field(default_factory=lambda: bool(os.getenv("LOCALDEV")))
    DB_TYPE: str = Field(default_factory=lambda: os.getenv("DB_TYPE", "MYSQL"))
    BADGR_MAKERSPACE_EMAIL: str = Field(default_factory=lambda: os.getenv('MAKERSPACE_EMAIL'))
    BADGR_MAKERSPACE_PASSWORD: str = Field(default_factory=lambda: os.getenv('MAKERSPACE_PASSWORD'))
    
    FRONTEND_BUILD_DIR: str = Field(default_factory=lambda: os.path.join(os.getenv("APP_HOME", "/app"), "frontend", "build"))
    PORT: int = Field(default=32776)
    
    DB: dict = Field(default_factory=dict)
    DB_CONNECTION_STRING: str = Field(default_factory=str)

    def __init__(self, **data):
        super().__init__(**data)
        self.check_required_env_vars()
        self.build_settings()
        self.build_sql_connection_string()

    def build_settings(self):
        def db_field(field):
            return os.getenv(f"{self.DB_TYPE}_{field}")

        if self.IS_LOCAL:
            self.FRONTEND_BUILD_DIR = os.path.join("..", "frontend", "build")
            print(self.FRONTEND_BUILD_DIR)
            self.PORT = 8001

        self.DB = {
            "DB": db_field("DB"),
            "USER": db_field("DB_USER"),
            "PASS": db_field("DB_PASSWORD"),
            "HOST": db_field("DB_SERVER"),
        }

    def build_sql_connection_string(self):
        encoded_password = urllib.parse.quote_plus(self.DB['PASS'])
        core_string = f"{self.DB['USER']}:{encoded_password}@{self.DB['HOST']}/{self.DB['DB']}"
        
        if self.DB_TYPE.lower() == "mysql":
            self.DB_CONNECTION_STRING = f"mysql+aiomysql://{core_string}"
        elif self.DB_TYPE.lower() == "mssql":
            self.DB_CONNECTION_STRING = f"mssql+aioodbc://{core_string}?driver=ODBC+Driver+18+for+SQL+Server&TrustServerCertificate=yes&Encrypt=yes&Authentication=SQLPassword"
        else:
            raise RuntimeError("No SQL db specified")

    def check_required_env_vars(self):
        required_vars = [
            "MAKERSPACE_EMAIL", "MAKERSPACE_PASSWORD",
            f"{self.DB_TYPE}_DB", f"{self.DB_TYPE}_DB_USER", f"{self.DB_TYPE}_DB_PASSWORD", f"{self.DB_TYPE}_DB_SERVER"
        ]
        
        missing_vars = [var for var in required_vars if not os.getenv(var)]
        if missing_vars:
            raise RuntimeError(f"Missing required environment variables: {', '.join(missing_vars)}")

