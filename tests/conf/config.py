from app.conf.config import Settings

settings_to_test = Settings(
    title="Test",
    description="Test",
    version="1.0",
    database_url="sqlite:///:memory:",
    secret_key="test",
    algorithm="HS256",
    version_prefix="/v1",
)
