import sqlalchemy as _sql
import sqlalchemy.ext.declarative as _declarative
import sqlalchemy.orm as _orm


DATABASE_URL = "postgresql://cgsukvjjfzlgrd:e980af14f1b9a825d213103d365bb33daeee148528d94274a2f3c8181ca81bec@ec2-52-30-67-143.eu-west-1.compute.amazonaws.com:5432/demsi71c8nc1no"


engine = _sql.create_engine(DATABASE_URL)

SessionLocal = _orm.sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = _declarative.declarative_base()
