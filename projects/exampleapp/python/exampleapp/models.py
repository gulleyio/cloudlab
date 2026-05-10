import uuid
from app.database import Base


class user_info(Base):
    __tablename__ = "users"

    user_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_name = Column(String, unique=True, index=True, nullable=False)
