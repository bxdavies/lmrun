#############
# Libraries #
#############
import sqlalchemy.ext.asyncio
import sqlalchemy.orm

###########
# Modules #
###########
from ..config import database_url

############
# Database #
############

# Create a async engine
engine = sqlalchemy.ext.asyncio.create_async_engine(database_url)

# Create a async session
async_session = sqlalchemy.orm.sessionmaker(
    engine, expire_on_commit=False, class_=sqlalchemy.ext.asyncio.AsyncSession)
