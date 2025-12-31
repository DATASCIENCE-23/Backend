from sqlalchemy.orm import Session
from Service.Service_model import ServiceMaster

class ServiceRepository:

    @staticmethod
    def get_by_id(db: Session, service_id: int):
        return db.query(ServiceMaster).filter(ServiceMaster.service_id == service_id).first()

    @staticmethod
    def get_by_code(db: Session, service_code: str):
        return db.query(ServiceMaster).filter(ServiceMaster.service_code == service_code).first()

    @staticmethod
    def get_all(db: Session, include_inactive: bool = False):
        query = db.query(ServiceMaster)
        if not include_inactive:
            query = query.filter(ServiceMaster.is_active == True)
        return query.all()

    @staticmethod
    def create(db: Session, service: ServiceMaster):
        db.add(service)
        db.commit()
        db.refresh(service)
        return service

    @staticmethod
    def update(db: Session, service: ServiceMaster):
        db.commit()
        db.refresh(service)
        return service

    @staticmethod
    def delete(db: Session, service: ServiceMaster):
        db.delete(service)
        db.commit()