import csv
from pathlib import Path
from models import ConcreteTest
from validators import validate_record
import storage

class QualityManager:
    def __init__(self):
        self.records = storage.load_records()
        self.counter = len(self.records)

    def _screen(self, data):
        findings = []
        slump = float(data["slump"])
        if not float(data["target_slump_min"]) <= slump <= float(data["target_slump_max"]):
            findings.append("Slump is outside the entered project range.")
        if float(data["concrete_temp"]) > float(data["target_temp_max"]):
            findings.append("Concrete temperature exceeds the entered maximum.")
        if not float(data["target_air_min"]) <= float(data["air_content"]) <= float(data["target_air_max"]):
            findings.append("Air content is outside the entered project range.")
        return ("REVIEW" if findings else "WITHIN ENTERED RANGES"), findings

    def add_record(self, data):
        validate_record(data)
        self.counter += 1
        record_id = f"CQ-{self.counter:04d}"
        status, findings = self._screen(data)
        record = ConcreteTest.from_data(record_id, data, status, findings).to_dict()
        self.records[record_id] = record
        storage.save_records(self.records)
        return record_id

    def export_csv(self):
        output_dir = Path(__file__).parent / "reports"
        output_dir.mkdir(exist_ok=True)
        path = output_dir / "concrete_quality_register.csv"
        fields = [
            "record_id", "project", "placement", "pour_date", "mix_id", "supplier",
            "ticket", "volume", "slump", "concrete_temp", "air_content", "strength_7",
            "strength_28", "inspector", "sample_id", "screening_status", "screening_notes", "notes"
        ]
        with path.open("w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fields)
            writer.writeheader()
            for record in self.records.values():
                row = dict(record)
                row["screening_notes"] = "; ".join(row["screening_notes"])
                writer.writerow({key: row.get(key, "") for key in fields})
        return path
