from pathlib import Path

from app.core.data_storage import get_reports_dir


def _signature_path_for(pdf_path: Path) -> Path:
    return pdf_path.with_name(pdf_path.name + ".sig")

def get_signed_reports(username: str) -> list[dict]:
    reports_dir = get_reports_dir(username)
    if not reports_dir.exists():
        return []

    signed_reports = []

    for pdf_path in reports_dir.glob("report_year_*.pdf"):
        sig_path = _signature_path_for(pdf_path)

        if sig_path.exists():
            year = int(pdf_path.stem.replace("report_year_", ""))
            signed_reports.append({
                "filename": pdf_path.name,
                "path": str(pdf_path),
                "year": year,
                "sig": str(sig_path),
            })

    return sorted(signed_reports, key=lambda x: x["year"], reverse=True)

def get_unsigned_reports(username: str) -> list[dict]:
    reports_dir = get_reports_dir(username)
    if not reports_dir.exists():
        return []

    unsigned_reports = []

    for pdf_path in reports_dir.glob("report_year_*.pdf"):
        sig_path = _signature_path_for(pdf_path)

        if not sig_path.exists():
            year = int(pdf_path.stem.replace("report_year_", ""))
            unsigned_reports.append({
                "filename": pdf_path.name,
                "path": str(pdf_path),
                "year": year,
            })

    return sorted(unsigned_reports, key=lambda x: x["year"], reverse=True)
