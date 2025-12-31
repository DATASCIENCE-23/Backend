from sqlalchemy.orm import Session
from datetime import datetime

from models.goods_receipt import GRN


class GRNService:
    """GRN number generator"""

    @staticmethod
    def genGRN(db: Session) -> str:
        """Generate sequential GRN: GRN-YYYY-MM-XXXXX"""
        now = datetime.now()
        year = now.strftime("%Y")
        month = now.strftime("%m")
        count = db.query(GRN).filter(
            GRN.grnNum.like(f"GRN-{year}-{month}-%")
        ).count()
        seq = str(count + 1).zfill(5)
        return f"GRN-{year}-{month}-{seq}"

    @staticmethod
    def createGRN(db: Session, purchaseId: int, recvBy: int, notes: str = None) -> GRN:
        """Create GRN"""
        grnNum = GRNService.genGRN(db)
        grn = GRN(
            purchaseId=purchaseId,
            grnNum=grnNum,
            recvDate=datetime.now().date(),
            recvBy=recvBy,
            notes=notes
        )
        db.add(grn)
        db.commit()
        db.refresh(grn)
        return grn
