from sqlalchemy.orm import Session
from sqlalchemy import and_, or_
from datetime import date, time, datetime
from typing import List, Optional
from Waiting_List.Waiting_List_model import WaitingList, WaitingListStatusEnum

class WaitingListRepository:

    @staticmethod
    def get_by_id(db: Session, waiting_id: int) -> Optional[WaitingList]:
        """Get waiting list entry by ID"""
        return db.query(WaitingList).filter(WaitingList.waiting_id == waiting_id).first()

    @staticmethod
    def get_all(db: Session, skip: int = 0, limit: int = 100) -> List[WaitingList]:
        """Get all waiting list entries with pagination"""
        return db.query(WaitingList).offset(skip).limit(limit).all()

    @staticmethod
    def get_by_patient_id(db: Session, patient_id: int) -> List[WaitingList]:
        """Get all waiting list entries for a specific patient"""
        return db.query(WaitingList).filter(WaitingList.patient_id == patient_id).order_by(WaitingList.added_at.desc()).all()

    @staticmethod
    def get_by_doctor_id(db: Session, doctor_id: int) -> List[WaitingList]:
        """Get all waiting list entries for a specific doctor"""
        return db.query(WaitingList).filter(WaitingList.doctor_id == doctor_id).order_by(WaitingList.added_at).all()

    @staticmethod
    def get_by_status(db: Session, status: WaitingListStatusEnum) -> List[WaitingList]:
        """Get all waiting list entries with a specific status"""
        return db.query(WaitingList).filter(WaitingList.status == status).all()

    @staticmethod
    def get_active_entries(db: Session, doctor_id: int = None) -> List[WaitingList]:
        """Get all active waiting list entries"""
        query = db.query(WaitingList).filter(WaitingList.status == WaitingListStatusEnum.ACTIVE)
        if doctor_id:
            query = query.filter(WaitingList.doctor_id == doctor_id)
        return query.order_by(WaitingList.added_at).all()

    @staticmethod
    def get_by_patient_and_doctor(db: Session, patient_id: int, doctor_id: int) -> List[WaitingList]:
        """Get waiting list entries for a specific patient-doctor combination"""
        return db.query(WaitingList).filter(
            and_(
                WaitingList.patient_id == patient_id,
                WaitingList.doctor_id == doctor_id
            )
        ).all()

    @staticmethod
    def get_by_preferred_date(db: Session, doctor_id: int, preferred_date: date) -> List[WaitingList]:
        """Get waiting list entries for a doctor on a specific preferred date"""
        return db.query(WaitingList).filter(
            and_(
                WaitingList.doctor_id == doctor_id,
                WaitingList.preferred_date == preferred_date,
                WaitingList.status == WaitingListStatusEnum.ACTIVE
            )
        ).order_by(WaitingList.added_at).all()

    @staticmethod
    def get_by_date_range(
        db: Session,
        doctor_id: int,
        start_date: date,
        end_date: date
    ) -> List[WaitingList]:
        """Get waiting list entries within a date range"""
        return db.query(WaitingList).filter(
            and_(
                WaitingList.doctor_id == doctor_id,
                WaitingList.preferred_date >= start_date,
                WaitingList.preferred_date <= end_date,
                WaitingList.status.in_([
                    WaitingListStatusEnum.ACTIVE,
                    WaitingListStatusEnum.NOTIFIED
                ])
            )
        ).order_by(WaitingList.preferred_date, WaitingList.added_at).all()

    @staticmethod
    def get_expired_entries(db: Session, current_time: datetime) -> List[WaitingList]:
        """Get all expired waiting list entries"""
        return db.query(WaitingList).filter(
            and_(
                WaitingList.status == WaitingListStatusEnum.ACTIVE,
                WaitingList.expires_at <= current_time
            )
        ).all()

    @staticmethod
    def get_entries_to_notify(db: Session, notification_window: datetime) -> List[WaitingList]:
        """Get waiting list entries that need notification"""
        return db.query(WaitingList).filter(
            and_(
                WaitingList.status == WaitingListStatusEnum.ACTIVE,
                WaitingList.expires_at <= notification_window,
                WaitingList.notified_at == None
            )
        ).all()

    @staticmethod
    def count_active_by_patient(db: Session, patient_id: int) -> int:
        """Count active waiting list entries for a patient"""
        return db.query(WaitingList).filter(
            and_(
                WaitingList.patient_id == patient_id,
                WaitingList.status == WaitingListStatusEnum.ACTIVE
            )
        ).count()

    @staticmethod
    def count_by_doctor_and_date(db: Session, doctor_id: int, preferred_date: date) -> int:
        """Count waiting list entries for a doctor on a specific date"""
        return db.query(WaitingList).filter(
            and_(
                WaitingList.doctor_id == doctor_id,
                WaitingList.preferred_date == preferred_date,
                WaitingList.status.in_([
                    WaitingListStatusEnum.ACTIVE,
                    WaitingListStatusEnum.NOTIFIED
                ])
            )
        ).count()

    @staticmethod
    def check_duplicate_entry(
        db: Session,
        patient_id: int,
        doctor_id: int,
        preferred_date: date
    ) -> bool:
        """Check if patient already has an active entry for this doctor on this date"""
        existing = db.query(WaitingList).filter(
            and_(
                WaitingList.patient_id == patient_id,
                WaitingList.doctor_id == doctor_id,
                WaitingList.preferred_date == preferred_date,
                WaitingList.status.in_([
                    WaitingListStatusEnum.ACTIVE,
                    WaitingListStatusEnum.NOTIFIED
                ])
            )
        ).first()
        return existing is not None

    @staticmethod
    def get_notified_entries(db: Session, doctor_id: int = None) -> List[WaitingList]:
        """Get waiting list entries that have been notified"""
        query = db.query(WaitingList).filter(WaitingList.status == WaitingListStatusEnum.NOTIFIED)
        if doctor_id:
            query = query.filter(WaitingList.doctor_id == doctor_id)
        return query.order_by(WaitingList.notified_at.desc()).all()

    @staticmethod
    def get_priority_sorted_entries(
        db: Session,
        doctor_id: int,
        preferred_date: date
    ) -> List[WaitingList]:
        """Get waiting list entries sorted by priority (added_at)"""
        return db.query(WaitingList).filter(
            and_(
                WaitingList.doctor_id == doctor_id,
                WaitingList.preferred_date == preferred_date,
                WaitingList.status == WaitingListStatusEnum.ACTIVE
            )
        ).order_by(WaitingList.added_at).all()

    @staticmethod
    def create(db: Session, waiting_entry: WaitingList) -> WaitingList:
        """Create a new waiting list entry"""
        db.add(waiting_entry)
        db.commit()
        db.refresh(waiting_entry)
        return waiting_entry

    @staticmethod
    def update(db: Session, waiting_entry: WaitingList) -> WaitingList:
        """Update an existing waiting list entry"""
        db.commit()
        db.refresh(waiting_entry)
        return waiting_entry

    @staticmethod
    def delete(db: Session, waiting_entry: WaitingList) -> None:
        """Delete a waiting list entry"""
        db.delete(waiting_entry)
        db.commit()

    @staticmethod
    def bulk_update_status(
        db: Session,
        waiting_ids: List[int],
        new_status: WaitingListStatusEnum
    ) -> int:
        """Bulk update status for multiple waiting list entries"""
        count = db.query(WaitingList).filter(
            WaitingList.waiting_id.in_(waiting_ids)
        ).update(
            {WaitingList.status: new_status},
            synchronize_session=False
        )
        db.commit()
        return count

    @staticmethod
    def get_statistics_by_doctor(db: Session, doctor_id: int) -> dict:
        """Get waiting list statistics for a doctor"""
        total = db.query(WaitingList).filter(WaitingList.doctor_id == doctor_id).count()
        active = db.query(WaitingList).filter(
            and_(
                WaitingList.doctor_id == doctor_id,
                WaitingList.status == WaitingListStatusEnum.ACTIVE
            )
        ).count()
        notified = db.query(WaitingList).filter(
            and_(
                WaitingList.doctor_id == doctor_id,
                WaitingList.status == WaitingListStatusEnum.NOTIFIED
            )
        ).count()
        
        return {
            "total": total,
            "active": active,
            "notified": notified
        }