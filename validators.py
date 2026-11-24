from datetime import datetime

REQUIRED_FIELDS = [
    "project", "placement", "pour_date", "mix_id", "inspector",
    "volume", "slump", "concrete_temp", "air_content",
    "target_slump_min", "target_slump_max", "target_temp_max",
    "target_air_min", "target_air_max"
]

def validate_record(data):
    for field in REQUIRED_FIELDS:
        if not str(data.get(field, "")).strip():
            raise ValueError(f"{field.replace('_', ' ').title()} is required.")
    try:
        datetime.strptime(data["pour_date"], "%Y-%m-%d")
    except ValueError:
        raise ValueError("Pour date must use YYYY-MM-DD.")
    numeric_fields = [
        "volume", "slump", "concrete_temp", "air_content",
        "target_slump_min", "target_slump_max", "target_temp_max",
        "target_air_min", "target_air_max"
    ]
    for field in numeric_fields:
        try:
            value = float(data[field])
        except (TypeError, ValueError):
            raise ValueError(f"{field.replace('_', ' ').title()} must be numeric.")
        if value < 0:
            raise ValueError(f"{field.replace('_', ' ').title()} cannot be negative.")
    if float(data["target_slump_min"]) > float(data["target_slump_max"]):
        raise ValueError("Specified minimum slump cannot exceed maximum slump.")
    if float(data["target_air_min"]) > float(data["target_air_max"]):
        raise ValueError("Specified minimum air content cannot exceed maximum air content.")
    for field in ("strength_7", "strength_28"):
        if str(data.get(field, "")).strip():
            try:
                if float(data[field]) < 0:
                    raise ValueError
            except ValueError:
                raise ValueError(f"{field.replace('_', ' ').title()} must be a non-negative number or blank.")
