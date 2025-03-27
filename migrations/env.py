from app.database.database import engine
from app.models.transaction import Base

# Убедитесь, что SQLAlchemy подключен к нужной базе данных
target_metadata = Base.metadata