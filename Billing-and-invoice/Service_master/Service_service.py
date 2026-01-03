from sqlalchemy.orm import Session
from .Service_model import ServiceMaster
from .Service_repository import ServiceRepository

class ServiceService:

    @staticmethod
    def create_service(db: Session, data: dict):
        # Check uniqueness on service_code
        if ServiceRepository.get_by_code(db, data["service_code"]):
            raise ValueError("Service with this code already exists")

        service = ServiceMaster(**data)
        return ServiceRepository.create(db, service)

    @staticmethod
    def get_service(db: Session, service_id: int):
        service = ServiceRepository.get_by_id(db, service_id)
        if not service:
            raise ValueError("Service not found")
        if not service.is_active:
            raise ValueError("Service is inactive")
        return service

    @staticmethod
    def list_services(db: Session, include_inactive: bool = False):
        return ServiceRepository.get_all(db, include_inactive)

    @staticmethod
    def update_service(db: Session, service_id: int, data: dict):
        service = ServiceRepository.get_by_id(db, service_id)
        if not service:
            raise ValueError("Service not found")

        # Prevent changing service_code if it's already set (to preserve UK integrity)
        if "service_code" in data and data["service_code"] != service.service_code:
            if ServiceRepository.get_by_code(db, data["service_code"]):
                raise ValueError("Another service already uses this code")

        for key, value in data.items():
            if hasattr(service, key):
                setattr(service, key, value)

        return ServiceRepository.update(db, service)

    @staticmethod
    def delete_service(db: Session, service_id: int):
        service = ServiceRepository.get_by_id(db, service_id)
        if not service:
            raise ValueError("Service not found")
        ServiceRepository.delete(db, service)