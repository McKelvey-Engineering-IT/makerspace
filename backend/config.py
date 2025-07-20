import os, urllib.parse
from pydantic import BaseModel, Field


BADGE_LEVELS = {
        "Red Level": {
            "expanded": True,
            "color": "#FF6B6B",  # Softer red
            "terms": [
                'Mini-Mill (CNC)',
                'Laser Cutting',
                'Power Tools - Band Saw',
                'Power Tools - Drill Press',
                '3D Scanner'
            ]
        },
        "Yellow Level": {
            "expanded": True,
            "color": "#FFD93D",  # Warmer yellow
            "terms": [
                'Handheld Power Tool - Cordless Drill',
                'Handheld Power Tool - Dremel',
                'Handheld Power Tool - Jigsaw',
                'Sewing',
                'Soldering',
                'Vinyl Cutting'
            ]
        },
        "Green Level": {
            "expanded": False,
            "color": "#4CAF50",  # Softer green
            "terms": [
                '3D Printing - Know the Basics',
                '3D Slicing with Prusa Slicer',
                '3D Slicing with PreForm (Form 3)',
                'Button Maker',
                'Laser Cutting with Inkscape',
                'Laser Cutting with Illustrator',
                'Heat Press',
                'Heat Press - Mini',
                'Mug Press'
            ]
        }
    }


class Settings(BaseModel):
    MESSAGE_STREAM_DELAY: int = 10
    MESSAGE_STREAM_RETRY_TIMEOUT: int = 15000
    IS_LOCAL: bool = Field(default_factory=lambda: bool(os.getenv("LOCALDEV")))
    DB_TYPE: str = Field(default_factory=lambda: os.getenv("DB_TYPE", "MYSQL"))
    BADGR_MAKERSPACE_EMAIL: str = Field(default_factory=lambda: os.getenv('MAKERSPACE_EMAIL'))
    BADGR_MAKERSPACE_PASSWORD: str = Field(default_factory=lambda: os.getenv('MAKERSPACE_PASSWORD'))

    FRONTEND_BUILD_DIR: str = Field(default_factory=lambda: os.path.join("..", "frontend", "build"))
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

