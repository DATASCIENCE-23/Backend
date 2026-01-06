from sqlalchemy.orm import Session
from sqlalchemy import and_
from datetime import date, datetime
from typing import List, Optional

from Waiting_List.Waiting_List_model import WaitingList, WaitingListStatusEnum


class WaitingListRepository:
    """Repository layer for Waiting List (DB operations only)"""

    # ================= GET METHODS =================

    @staticmethod
    def get_by_id(db: Session, waiting_id: int) -> Optional[WaitingList]:
        return (
            db.query(WaitingList)
            .filter(WaitingList.waiting_id == waiting_id)
            .first()
        )

    @staticmethod
    def get_all(db: Session, skip: int = 0, limit: int = 100) -> List[WaitingList]:
        return (
            db.query(WaitingList)
            .offset(skip)
            .limit(limit)
            .all()
        )

    @staticmethod
    def get_by_patient_id(db: Session, patient_id: int) -> List[WaitingList]:
        return (
            db.query(WaitingList)
            .filter(WaitingList.patient_id == patient_id)
            .order_by(WaitingList.added_at.desc())
            .all()
        )

    @staticmethod
    def get_by_doctor_id(db: Session, doctor_id: int) -> List[WaitingList]:
        return (
            db.query(WaitingList)
            .filter(WaitingList.doctor_id == doctor_id)
            .order_by(WaitingList.added_at)
            .all()
        )

    @staticmethod
    def get_by_status(db: Session, status: WaitingListStatusEnum) -> List[WaitingList]:
        return (
            db.query(WaitingList)
            .filter(WaitingList.status == status)
            .all()
        )

    @staticmethod
    def get_active_entries(db: Session, doctor_id: Optional[int] = None) -> List[WaitingList]:
        query = db.query(WaitingList).filter(
            WaitingList.status == WaitingListStatusEnum.ACTIVE
        )

        if doctor_id is not None:
            query = query.filter(WaitingList.doctor_id == doctor_id)

        return query.order_by(WaitingList.added_at).all()

    @staticmethod
    def get_by_patient_and_doctor(
        db: Session,
        patient_id: int,
        doctor_id: int
    ) -> List[WaitingList]:
        return (
            db.query(WaitingList)
            .filter(
                and_(
                    WaitingList.patient_id == patient_id,
                    WaitingList.doctor_id == doctor_id
                )
            )
            .all()
        )

    @staticmethod
    def get_by_preferred_date(
        db: Session,
        doctor_id: int,
        preferred_date: date
    ) -> List[WaitingList]:
        return (
            db.query(WaitingList)
            .filter(
                and_(
                    WaitingList.doctor_id == doctor_id,
                    WaitingList.preferred_date == preferred_date,
                    WaitingList.status == WaitingListStatusEnum.ACTIVE
                )
            )
            .order_by(WaitingList.added_at)
            .all()
        )

    @staticmethod
    def get_by_date_range(
        db: Session,
        doctor_id: int,
        start_date: date,
        end_date: date
    ) -> List[WaitingList]:
        return (
            db.query(WaitingList)
            .filter(
                and_(
                    WaitingList.doctor_id == doctor_id,
                    WaitingList.preferred_date >= start_date,
                    WaitingList.preferred_date <= end_date,
                    WaitingList.status.in_(
                        [
                            WaitingListStatusEnum.ACTIVE,
                            WaitingListStatusEnum.NOTIFIED
                        ]
                    )
                )
            )
            .order_by(WaitingList.preferred_date, WaitingList.added_at)
            .all()
        )

    @staticmethod
    def get_expired_entries(db: Session, current_time: datetime) -> List[WaitingList]:
        return (
            db.query(WaitingList)
            .filter(
                and_(
                    WaitingList.status == WaitingListStatusEnum.ACTIVE,
                    WaitingList.expires_at <= current_time
                )
            )
            .all()
        )

    @staticmethod
    def get_entries_to_notify(
        db: Session,
        notification_window: datetime
    ) -> List[WaitingList]:
        return (
            db.query(WaitingList)
            .filter(
                and_(
                    WaitingList.status == WaitingListStatusEnum.ACTIVE,
                    WaitingList.expires_at <= notification_window,
                    WaitingList.notified_at.is_(None)
                )
            )
            .all()
        )

    # ================= COUNT METHODS =================

    @staticmethod
    def count_active_by_patient(db: Session, patient_id: int) -> int:
        return (
            db.query(WaitingList)
            .filter(
                and_(
                    WaitingList.patient_id == patient_id,
                    WaitingList.status == WaitingListStatusEnum.ACTIVE
                )
            )
            .count()
        )

    @staticmethod
    def count_by_doctor_and_date(
        db: Session,
        doctor_id: int,
        preferred_date: date
    ) -> int:
        return (
            db.query(WaitingList)
            .filter(
                and_(
                    WaitingList.doctor_id == doctor_id,
                    WaitingList.preferred_date == preferred_date,
                    WaitingList.status.in_(
                        [
                            WaitingListStatusEnum.ACTIVE,
                            WaitingListStatusEnum.NOTIFIED
                        ]
                    )
                )
            )
            .count()
        )

    # ================= VALIDATION HELPERS =================

    @staticmethod
    def check_duplicate_entry(
        db: Session,
        patient_id: int,
        doctor_id: int,
        preferred_date: date
    ) -> bool:
        existing = (
            db.query(WaitingList)
            .filter(
                and_(
                    WaitingList.patient_id == patient_id,
                    WaitingList.doctor_id == doctor_id,
                    WaitingList.preferred_date == preferred_date,
                    WaitingList.status.in_(
                        [
                            WaitingListStatusEnum.ACTIVE,
                            WaitingListStatusEnum.NOTIFIED
                        ]
                    )
                )
            )
            .first()
        )
        return existing is not None

    # ================= WRITE METHODS =================

    @staticmethod
    def create(db: Session, waiting_entry: WaitingList) -> WaitingList:
        db.add(waiting_entry)
        db.commit()
        db.refresh(waiting_entry)
        return waiting_entry

    @staticmethod
    def update(db: Session, waiting_entry: WaitingList) -> WaitingList:
        db.commit()
        db.refresh(waiting_entry)
        return waiting_entry

    @staticmethod
    def delete(db: Session, waiting_entry: WaitingList) -> None:
        db.delete(waiting_entry)
        db.commit()

    @staticmethod
    def bulk_update_status(
        db: Session,
        waiting_ids: List[int],
        new_status: WaitingListStatusEnum
    ) -> int:
        count = (
            db.query(WaitingList)
            .filter(WaitingList.waiting_id.in_(waiting_ids))
            .update(
                {WaitingList.status: new_status},
                synchronize_session=False
            )
        )
        db.commit()
        return count

    # ================= STATISTICS =================

    @staticmethod
    def get_statistics_by_doctor(db: Session, doctor_id: int) -> dict:
        total = (
            db.query(WaitingList)
            .filter(WaitingList.doctor_id == doctor_id)
            .count()
        )

        active = (
            db.query(WaitingList)
            .filter(
                and_(
                    WaitingList.doctor_id == doctor_id,
                    WaitingList.status == WaitingListStatusEnum.ACTIVE
                )
            )
            .count()
        )

        notified = (
            db.query(WaitingList)
            .filter(
                and_(
                    WaitingList.doctor_id == doctor_id,
                    WaitingList.status == WaitingListStatusEnum.NOTIFIED
                )
            )
            .count()
        )

        return {
            "total": total,
            "active": active,
            "notified": notified
        }
