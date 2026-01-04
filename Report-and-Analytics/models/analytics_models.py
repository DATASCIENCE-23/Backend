from sqlalchemy import Column, Integer, String, DateTime, Text, Numeric, ForeignKey
from sqlalchemy.orm import relationship
from database import Base
import datetime

class AnalyticalSnapshot(Base):
    __tablename__ = "analytical_snapshot"

    snapshot_id = Column(Integer, primary_key=True)
    captured_at = Column(DateTime, default=datetime.datetime.utcnow)
    metric_type = Column(String, nullable=False)
    value = Column(Numeric(15, 2), nullable=False)
    dimensions = Column(String)

class ReportTemplate(Base):
    __tablename__ = "report_template"

    template_id = Column(Integer, primary_key=True)
    template_name = Column(String, nullable=False)
    layout_json = Column(Text)
    category = Column(String)

class GeneratedReport(Base):
    __tablename__ = "generated_report"

    report_id = Column(Integer, primary_key=True)
    template_id = Column(Integer, ForeignKey("report_template.template_id"))
    patient_id = Column(Integer)     # do NOT FK (owned by core team)
    generated_by_user_id = Column(Integer)
    generated_at = Column(DateTime, default=datetime.datetime.utcnow)
    file_path_url = Column(String)
