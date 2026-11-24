from dataclasses import dataclass, asdict
from datetime import datetime

@dataclass
class ConcreteTest:
    record_id: str
    project: str
    placement: str
    pour_date: str
    mix_id: str
    supplier: str
    ticket: str
    volume: float
    slump: float
    concrete_temp: float
    air_content: float
    strength_7: str
    strength_28: str
    target_slump_min: float
    target_slump_max: float
    target_temp_max: float
    target_air_min: float
    target_air_max: float
    inspector: str
    sample_id: str
    notes: str
    screening_status: str
    screening_notes: list
    created_at: str

    def to_dict(self):
        return asdict(self)

    @classmethod
    def from_data(cls, record_id, data, status, findings):
        return cls(
            record_id=record_id,
            project=data["project"],
            placement=data["placement"],
            pour_date=data["pour_date"],
            mix_id=data["mix_id"],
            supplier=data["supplier"],
            ticket=data["ticket"],
            volume=float(data["volume"]),
            slump=float(data["slump"]),
            concrete_temp=float(data["concrete_temp"]),
            air_content=float(data["air_content"]),
            strength_7=data.get("strength_7", ""),
            strength_28=data.get("strength_28", ""),
            target_slump_min=float(data["target_slump_min"]),
            target_slump_max=float(data["target_slump_max"]),
            target_temp_max=float(data["target_temp_max"]),
            target_air_min=float(data["target_air_min"]),
            target_air_max=float(data["target_air_max"]),
            inspector=data["inspector"],
            sample_id=data["sample_id"],
            notes=data.get("notes", ""),
            screening_status=status,
            screening_notes=findings,
            created_at=datetime.now().isoformat(timespec="seconds"),
        )
