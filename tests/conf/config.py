from app.conf.config import Settings

settings_to_test = Settings(
    title="",
    description="",
    version="",
    database_url="sqlite:///:memory:",
    secret_key="test",
    algorithm="HS256",
    version_prefix="v1",
)
