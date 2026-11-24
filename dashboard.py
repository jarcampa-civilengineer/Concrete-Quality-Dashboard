from pathlib import Path
from datetime import datetime
from html import escape

class Dashboard:
    def __init__(self, manager):
        self.manager = manager

    def metrics(self):
        records = list(self.manager.records.values())
        total = len(records)
        flagged = sum(r["screening_status"] == "REVIEW" for r in records)
        total_volume = sum(float(r["volume"]) for r in records)
        avg_slump = sum(float(r["slump"]) for r in records) / total if total else 0
        strengths = [float(r["strength_28"]) for r in records if r.get("strength_28", "").strip()]
        avg_strength = sum(strengths) / len(strengths) if strengths else None
        return {
            "total": total, "flagged": flagged, "volume": total_volume,
            "avg_slump": avg_slump, "avg_strength": avg_strength
        }

    def print_summary(self):
        m = self.metrics()
        print("\n--- CONCRETE QUALITY SUMMARY ---")
        print(f"Test / inspection records: {m['total']}")
        print(f"Records flagged for review: {m['flagged']}")
        print(f"Recorded concrete volume: {m['volume']:.2f} yd3")
        print(f"Average slump: {m['avg_slump']:.2f} in")
        strength = f"{m['avg_strength']:.0f} psi" if m["avg_strength"] is not None else "Pending / not entered"
        print(f"Average entered 28-day strength: {strength}")

    def print_records(self):
        if not self.manager.records:
            print("No concrete test records found.")
            return
        print("\nID | DATE | PROJECT | LOCATION | SLUMP (in) | TEMP (F) | AIR (%) | STATUS")
        print("-" * 105)
        for r in self.manager.records.values():
            print(f"{r['record_id']} | {r['pour_date']} | {r['project']} | {r['placement']} | "
                  f"{r['slump']} | {r['concrete_temp']} | {r['air_content']} | {r['screening_status']}")

    def generate_html(self):
        m = self.metrics()
        rows = []
        for r in self.manager.records.values():
            findings = "; ".join(r["screening_notes"]) or "No range flags"
            cls = "review" if r["screening_status"] == "REVIEW" else "ok"
            rows.append(
                f"<tr><td>{escape(r['record_id'])}</td><td>{escape(r['pour_date'])}</td>"
                f"<td>{escape(r['project'])}</td><td>{escape(r['placement'])}</td>"
                f"<td>{float(r['slump']):.2f}</td><td>{float(r['concrete_temp']):.1f}</td>"
                f"<td>{float(r['air_content']):.2f}</td><td>{escape(r.get('strength_28') or 'Pending')}</td>"
                f"<td class='{cls}'>{escape(r['screening_status'])}</td><td>{escape(findings)}</td></tr>"
            )
        avg_strength = f"{m['avg_strength']:.0f} psi" if m["avg_strength"] is not None else "Pending"
        html = f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Concrete Quality Dashboard</title>
<style>
body{{font-family:Arial,sans-serif;margin:0;background:#f3f5f8;color:#202938}}
header{{background:#20364f;color:white;padding:26px 5%}} main{{padding:24px 5%}}
.cards{{display:grid;grid-template-columns:repeat(auto-fit,minmax(170px,1fr));gap:14px}}
.card{{background:white;padding:18px;border-radius:9px;box-shadow:0 2px 8px #0001}}
.metric{{font-size:27px;font-weight:bold;margin-top:8px}} .label{{color:#657386;font-size:13px}}
.panel{{background:white;padding:18px;border-radius:9px;margin-top:20px;overflow-x:auto}}
table{{border-collapse:collapse;width:100%;font-size:13px}}th,td{{padding:10px;border-bottom:1px solid #e5e9ef;text-align:left}}
th{{background:#eef2f6}} .review{{color:#a33;font-weight:bold}} .ok{{color:#18734a;font-weight:bold}}
.note{{font-size:12px;color:#64748b;line-height:1.5}}
</style></head><body>
<header><h1>Concrete Quality Dashboard</h1><div>Generated {datetime.now().strftime('%Y-%m-%d %H:%M')}</div></header>
<main><section class="cards">
<div class="card"><div class="label">TEST / INSPECTION RECORDS</div><div class="metric">{m['total']}</div></div>
<div class="card"><div class="label">FLAGGED FOR REVIEW</div><div class="metric">{m['flagged']}</div></div>
<div class="card"><div class="label">RECORDED VOLUME</div><div class="metric">{m['volume']:.2f} yd³</div></div>
<div class="card"><div class="label">AVERAGE SLUMP</div><div class="metric">{m['avg_slump']:.2f} in</div></div>
<div class="card"><div class="label">AVERAGE ENTERED 28-DAY STRENGTH</div><div class="metric">{avg_strength}</div></div>
</section>
<section class="panel"><h2>Concrete Test Register</h2>
<table><thead><tr><th>ID</th><th>Date</th><th>Project</th><th>Placement</th><th>Slump (in)</th><th>Temp (°F)</th><th>Air (%)</th><th>28-day (psi)</th><th>Screening</th><th>Notes</th></tr></thead>
<tbody>{''.join(rows) if rows else '<tr><td colspan="10">No records entered yet.</td></tr>'}</tbody></table></section>
<p class="note">Screening flags compare entered slump, concrete temperature, and air-content values with the limits entered for each record. They are not an acceptance decision or a substitute for project specifications, applicable standards, testing agency reports, or review by the responsible quality professional.</p>
</main></body></html>"""
        output_dir = Path(__file__).parent / "reports"
        output_dir.mkdir(exist_ok=True)
        path = output_dir / "concrete_quality_dashboard.html"
        path.write_text(html, encoding="utf-8")
        return path
