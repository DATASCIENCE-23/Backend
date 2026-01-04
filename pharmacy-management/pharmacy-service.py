"""
Pharmacy Module - Service Layer
Contains business logic and orchestrates repository operations
"""
from sqlalchemy.orm import Session
from typing import List, Optional, Tuple
from datetime import datetime
import json
from decimal import Decimal

from repository import (
    MedicineRepository, MedicineBatchRepository, PrescriptionRepository,
    DispenseRepository, PharmacyAuditRepository
)
from schemas import (
    MedicineCreate, MedicineUpdate, MedicineResponse,
    MedicineBatchCreate, MedicineBatchResponse,
    PrescriptionCreate, PrescriptionResponse,
    DispenseCreate, DispenseResponse,
    LowStockMedicine, StockValidationResponse,
    PrescriptionStatus, DispenseStatus
)
from exceptions import (
    DuplicateRecordException, NotFoundException,
    InsufficientStockException, ValidationException
)


class MedicineService:
    """Business logic for Medicine management"""

    @staticmethod
    def create_medicine(db: Session, medicine_data: MedicineCreate, user_id: int) -> MedicineResponse:
        # Check for duplicate
        if MedicineRepository.check_duplicate(
                db, medicine_data.medicine_name,
                medicine_data.strength, medicine_data.form
        ):
            raise DuplicateRecordException(
                f"Medicine {medicine_data.medicine_name} with strength {medicine_data.strength} "
                f"and form {medicine_data.form} already exists"
            )

        medicine = MedicineRepository.create(db, medicine_data.dict(), user_id)

        # Audit log
        PharmacyAuditRepository.log_action(
            db, user_id, "Medicine", medicine.medicine_id, "CREATE",
            json.dumps(medicine_data.dict(), default=str)
        )

        return MedicineResponse.from_orm(medicine)

    @staticmethod
    def get_medicine(db: Session, medicine_id: int) -> MedicineResponse:
        medicine = MedicineRepository.get_by_id(db, medicine_id)
        if not medicine:
            raise NotFoundException(f"Medicine with ID {medicine_id} not found")

        response = MedicineResponse.from_orm(medicine)
        response.total_stock = MedicineRepository.get_total_stock(db, medicine_id)
        return response

    @staticmethod
    def update_medicine(db: Session, medicine_id: int,
                        medicine_data: MedicineUpdate, user_id: int) -> MedicineResponse:
        medicine = MedicineRepository.get_by_id(db, medicine_id)
        if not medicine:
            raise NotFoundException(f"Medicine with ID {medicine_id} not found")

        # Check duplicate if name/strength/form changed
        update_dict = medicine_data.dict(exclude_unset=True)
        if any(k in update_dict for k in ['medicine_name', 'strength', 'form']):
            name = update_dict.get('medicine_name', medicine.medicine_name)
            strength = update_dict.get('strength', medicine.strength)
            form = update_dict.get('form', medicine.form)

            if MedicineRepository.check_duplicate(db, name, strength, form, medicine_id):
                raise DuplicateRecordException(
                    f"Medicine {name} with strength {strength} and form {form} already exists"
                )

        updated = MedicineRepository.update(db, medicine_id, update_dict, user_id)

        # Audit log
        PharmacyAuditRepository.log_action(
            db, user_id, "Medicine", medicine_id, "UPDATE",
            json.dumps(update_dict, default=str)
        )

        return MedicineResponse.from_orm(updated)

    @staticmethod
    def search_medicines(db: Session, search_term: str) -> List[MedicineResponse]:
        medicines = MedicineRepository.search(db, search_term)
        return [MedicineResponse.from_orm(med) for med in medicines]

    @staticmethod
    def get_low_stock_medicines(db: Session) -> List[LowStockMedicine]:
        """Get medicines below reorder level for inventory integration"""
        low_stock_data = MedicineRepository.get_low_stock_medicines(db)

        result = []
        for medicine, available_qty in low_stock_data:
            result.append(LowStockMedicine(
                medicine_id=medicine.medicine_id,
                medicine_name=medicine.medicine_name,
                generic_name=medicine.generic_name,
                strength=medicine.strength,
                form=medicine.form,
                available_quantity=available_qty,
                min_quantity=medicine.min_quantity,
                reorder_level=medicine.reorder_level,
                deficit=medicine.reorder_level - available_qty
            ))

        return result


class MedicineBatchService:
    """Business logic for Medicine Batch management"""

    @staticmethod
    def create_batch(db: Session, batch_data: MedicineBatchCreate, user_id: int) -> MedicineBatchResponse:
        # Validate medicine exists
        medicine = MedicineRepository.get_by_id(db, batch_data.medicine_id)
        if not medicine:
            raise NotFoundException(f"Medicine with ID {batch_data.medicine_id} not found")

        # Check duplicate batch number
        if MedicineBatchRepository.check_batch_number_exists(db, batch_data.batch_number):
            raise DuplicateRecordException(f"Batch number {batch_data.batch_number} already exists")

        batch = MedicineBatchRepository.create(db, batch_data.dict())

        # Audit log
        PharmacyAuditRepository.log_action(
            db, user_id, "MedicineBatch", batch.batch_id, "CREATE",
            json.dumps(batch_data.dict(), default=str)
        )

        return MedicineBatchResponse.from_orm(batch)

    @staticmethod
    def get_batches_by_medicine(db: Session, medicine_id: int) -> List[MedicineBatchResponse]:
        batches = MedicineBatchRepository.get_by_medicine(db, medicine_id)
        return [MedicineBatchResponse.from_orm(batch) for batch in batches]


class PrescriptionService:
    """Business logic for Prescription management"""

    @staticmethod
    def create_prescription(db: Session, prescription_data: PrescriptionCreate) -> PrescriptionResponse:
        """Create prescription from doctor module (via API)"""

        # Validate all medicines exist
        for item in prescription_data.items:
            medicine = MedicineRepository.get_by_id(db, item.medicine_id)
            if not medicine:
                raise NotFoundException(f"Medicine with ID {item.medicine_id} not found")
            if not medicine.is_active:
                raise ValidationException(f"Medicine {medicine.medicine_name} is not active")

        # Create prescription
        prescription_dict = prescription_data.dict(exclude={'items'})
        items_data = [item.dict() for item in prescription_data.items]

        prescription = PrescriptionRepository.create(db, prescription_dict, items_data)

        return PrescriptionService._build_prescription_response(db, prescription)

    @staticmethod
    def get_prescription(db: Session, prescription_id: int) -> PrescriptionResponse:
        prescription = PrescriptionRepository.get_by_id(db, prescription_id)
        if not prescription:
            raise NotFoundException(f"Prescription with ID {prescription_id} not found")

        return PrescriptionService._build_prescription_response(db, prescription)

    @staticmethod
    def get_pending_prescriptions(db: Session, skip: int = 0, limit: int = 100) -> List[PrescriptionResponse]:
        prescriptions = PrescriptionRepository.get_pending(db, skip, limit)
        return [PrescriptionService._build_prescription_response(db, p) for p in prescriptions]

    @staticmethod
    def validate_stock_availability(db: Session, prescription_id: int) -> StockValidationResponse:
        """Check if prescription can be dispensed based on stock"""
        availability = PrescriptionRepository.check_stock_availability(db, prescription_id)

        if "error" in availability:
            raise NotFoundException(availability["error"])

        return StockValidationResponse(
            prescription_id=availability["prescription_id"],
            can_dispense_fully=availability["can_dispense_fully"],
            validation_items=availability["items"]
        )

    @staticmethod
    def _build_prescription_response(db: Session, prescription) -> PrescriptionResponse:
        """Helper to build prescription response with calculated fields"""
        from models import Patient, Doctor

        # Get patient and doctor info (simplified - would use proper joins)
        patient = db.query(Patient).filter(Patient.patient_id == prescription.patient_id).first()
        doctor = db.query(Doctor).filter(Doctor.doctor_id == prescription.doctor_id).first()

        items_response = []
        for item in prescription.prescription_items:
            available_qty = MedicineRepository.get_total_stock(db, item.medicine_id)
            items_response.append({
                "prescription_item_id": item.prescription_item_id,
                "medicine_id": item.medicine_id,
                "medicine_name": item.medicine.medicine_name,
                "generic_name": item.medicine.generic_name,
                "strength": item.medicine.strength,
                "form": item.medicine.form,
                "prescribed_quantity": item.prescribed_quantity,
                "dosage": item.dosage,
                "frequency": item.frequency,
                "duration_days": item.duration_days,
                "instructions": item.instructions,
                "available_quantity": available_qty,
                "unit_price": item.medicine.unit_price
            })

        return PrescriptionResponse(
            prescription_id=prescription.prescription_id,
            patient_id=prescription.patient_id,
            patient_name=f"{patient.first_name} {patient.last_name}" if patient else "Unknown",
            doctor_id=prescription.doctor_id,
            doctor_name=f"Dr. {doctor.first_name} {doctor.last_name}" if doctor else "Unknown",
            created_at=prescription.created_at,
            status=prescription.status,
            notes=prescription.notes,
            items=items_response
        )


class DispenseService:
    """Business logic for Dispensing medicines"""

    @staticmethod
    def dispense_medicines(db: Session, dispense_data: DispenseCreate, user_id: int) -> DispenseResponse:
        """Process medicine dispensing"""

        # Validate prescription exists and is pending
        prescription = PrescriptionRepository.get_by_id(db, dispense_data.prescription_id)
        if not prescription:
            raise NotFoundException(f"Prescription {dispense_data.prescription_id} not found")

        if prescription.status not in [PrescriptionStatus.PENDING, PrescriptionStatus.IN_PROGRESS]:
            raise ValidationException(f"Prescription status is {prescription.status}, cannot dispense")

        # Validate stock and prepare dispense items
        dispense_items_data = []
        total_prescribed = 0
        total_dispensed = 0

        for item in dispense_data.items:
            # Find prescription item
            presc_item = next(
                (pi for pi in prescription.prescription_items
                 if pi.prescription_item_id == item.prescription_item_id),
                None
            )
            if not presc_item:
                raise NotFoundException(f"Prescription item {item.prescription_item_id} not found")

            # Validate batch
            batch = MedicineBatchRepository.get_by_id(db, item.batch_id)
            if not batch:
                raise NotFoundException(f"Batch {item.batch_id} not found")

            if batch.medicine_id != presc_item.medicine_id:
                raise ValidationException(
                    f"Batch {item.batch_id} does not belong to medicine {presc_item.medicine_id}"
                )

            # Check stock availability
            if batch.quantity_in_stock < item.dispensed_quantity:
                raise InsufficientStockException(
                    f"Insufficient stock in batch {batch.batch_number}. "
                    f"Available: {batch.quantity_in_stock}, Requested: {item.dispensed_quantity}"
                )

            # Prepare dispense item
            dispense_items_data.append({
                "prescription_item_id": item.prescription_item_id,
                "batch_id": item.batch_id,
                "dispensed_quantity": item.dispensed_quantity,
                "unit_price": presc_item.medicine.unit_price
            })

            total_prescribed += presc_item.prescribed_quantity
            total_dispensed += item.dispensed_quantity

        # Create dispense record
        dispense_dict = {
            "prescription_id": dispense_data.prescription_id,
            "pharmacist_id": dispense_data.pharmacist_id,
            "notes": dispense_data.notes,
            "status": DispenseStatus.COMPLETED
        }

        dispense = DispenseRepository.create(db, dispense_dict, dispense_items_data)

        # Update prescription status
        new_status = PrescriptionStatus.COMPLETED if total_dispensed >= total_prescribed \
            else PrescriptionStatus.PARTIALLY_COMPLETED
        PrescriptionRepository.update_status(db, dispense_data.prescription_id, new_status)

        # Audit log
        PharmacyAuditRepository.log_action(
            db, user_id, "Dispense", dispense.dispense_id, "DISPENSE",
            json.dumps({
                "prescription_id": dispense_data.prescription_id,
                "items_count": len(dispense_items_data),
                "total_amount": str(dispense.total_amount)
            })
        )

        return DispenseService._build_dispense_response(db, dispense)

    @staticmethod
    def get_dispense(db: Session, dispense_id: int) -> DispenseResponse:
        dispense = DispenseRepository.get_by_id(db, dispense_id)
        if not dispense:
            raise NotFoundException(f"Dispense with ID {dispense_id} not found")

        return DispenseService._build_dispense_response(db, dispense)

    @staticmethod
    def get_unbilled_dispenses(db: Session) -> List[dict]:
        """Get dispenses ready for billing - for billing module integration"""
        dispenses = DispenseRepository.get_unbilled_dispenses(db)

        result = []
        for dispense in dispenses:
            items = []
            for item in dispense.dispense_items:
                items.append({
                    "medicine_name": item.prescription_item.medicine.medicine_name,
                    "quantity": item.dispensed_quantity,
                    "unit_price": float(item.unit_price),
                    "line_total": float(item.line_total)
                })

            result.append({
                "dispense_id": dispense.dispense_id,
                "prescription_id": dispense.prescription_id,
                "patient_id": dispense.prescription.patient_id,
                "dispensed_at": dispense.dispensed_at,
                "total_amount": float(dispense.total_amount),
                "items": items
            })

        return result

    @staticmethod
    def mark_as_billed(db: Session, dispense_id: int, invoice_id: int) -> DispenseResponse:
        """Mark dispense as billed - called by billing module"""
        dispense = DispenseRepository.update_billing_status(db, dispense_id, invoice_id)
        if not dispense:
            raise NotFoundException(f"Dispense with ID {dispense_id} not found")

        return DispenseService._build_dispense_response(db, dispense)

    @staticmethod
    def _build_dispense_response(db: Session, dispense) -> DispenseResponse:
        """Helper to build dispense response"""
        from models import Pharmacist

        pharmacist = db.query(Pharmacist).filter(
            Pharmacist.pharmacist_id == dispense.pharmacist_id
        ).first()

        items_response = []
        for item in dispense.dispense_items:
            items_response.append({
                "dispense_item_id": item.dispense_item_id,
                "prescription_item_id": item.prescription_item_id,
                "medicine_name": item.prescription_item.medicine.medicine_name,
                "batch_number": item.batch.batch_number,
                "dispensed_quantity": item.dispensed_quantity,
                "unit_price": item.unit_price,
                "line_total": item.line_total
            })

        return DispenseResponse(
            dispense_id=dispense.dispense_id,
            prescription_id=dispense.prescription_id,
            pharmacist_id=dispense.pharmacist_id,
            pharmacist_name=f"{pharmacist.first_name} {pharmacist.last_name}" if pharmacist else "Unknown",
            dispensed_at=dispense.dispensed_at,
            total_amount=dispense.total_amount,
            status=dispense.status,
            notes=dispense.notes,
            items=items_response
        )