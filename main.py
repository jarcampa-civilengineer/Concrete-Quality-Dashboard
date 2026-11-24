from quality_manager import QualityManager
from dashboard import Dashboard

def ask(prompt, default=""):
    value = input(f"{prompt}" + (f" [{default}]" if default else "") + ": ").strip()
    return value or default

def main():
    manager = QualityManager()
    dashboard = Dashboard(manager)

    while True:
        print("\n=== CONCRETE QUALITY DASHBOARD ===")
        print("1. Record concrete test / inspection")
        print("2. View dashboard summary")
        print("3. List test records")
        print("4. Generate HTML dashboard")
        print("5. Export test register to CSV")
        print("6. Exit")
        choice = input("Select an option: ").strip()

        try:
            if choice == "1":
                data = {
                    "project": ask("Project name"),
                    "placement": ask("Placement / pour location"),
                    "pour_date": ask("Pour date (YYYY-MM-DD)"),
                    "mix_id": ask("Mix design ID"),
                    "supplier": ask("Concrete supplier", "N/A"),
                    "ticket": ask("Delivery ticket number", "N/A"),
                    "volume": ask("Delivered volume (yd3)", "0"),
                    "slump": ask("Measured slump (inches)", "0"),
                    "concrete_temp": ask("Concrete temperature (F)", "0"),
                    "air_content": ask("Air content (%)", "0"),
                    "strength_7": ask("7-day compressive strength (psi; blank if pending)", ""),
                    "strength_28": ask("28-day compressive strength (psi; blank if pending)", ""),
                    "target_slump_min": ask("Specified minimum slump (inches)", "0"),
                    "target_slump_max": ask("Specified maximum slump (inches)", "10"),
                    "target_temp_max": ask("Maximum concrete temperature (F)", "90"),
                    "target_air_min": ask("Minimum air content (%)", "0"),
                    "target_air_max": ask("Maximum air content (%)", "10"),
                    "inspector": ask("Inspector / technician"),
                    "sample_id": ask("Sample / cylinder ID", "N/A"),
                    "notes": ask("Observations / notes", ""),
                }
                record_id = manager.add_record(data)
                print(f"Record saved: {record_id}")
                print(f"Screening result: {manager.records[record_id]['screening_status']}")
            elif choice == "2":
                dashboard.print_summary()
            elif choice == "3":
                dashboard.print_records()
            elif choice == "4":
                path = dashboard.generate_html()
                print(f"HTML dashboard generated: {path}")
            elif choice == "5":
                path = manager.export_csv()
                print(f"CSV register exported: {path}")
            elif choice == "6":
                print("Goodbye.")
                break
            else:
                print("Please select a valid option.")
        except (ValueError, KeyError) as exc:
            print(f"Error: {exc}")

if __name__ == "__main__":
    main()
