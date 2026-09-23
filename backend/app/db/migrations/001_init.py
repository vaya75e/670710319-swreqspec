from app.db.models import Base


# รองรับ: CON-TECH-01, DOM-PDPA-01, IF-HIS-01

def upgrade(engine):
    Base.metadata.create_all(bind=engine)


def downgrade(engine):
    Base.metadata.drop_all(bind=engine)
