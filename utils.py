from typing import List, Dict, Optional


def parse_experience(exp_str: str) -> Dict[str, str]:
    # Format: yrs_[bucket]::title_[title]::company_[company]::start_[year]::end_[year]
    parts = exp_str.split("::")
    out = {}
    for p in parts:
        if '_' not in p:
            continue
        k, v = p.split('_', 1)
        out[k] = v
    return out


def parse_education(edu_str: str) -> Dict[str, str]:
    # Format: yrs_[bucket]::school_[school]::degree_[degree]::fos_[field_of_study]::start_[year]::end_[year]
    parts = edu_str.split("::")
    out = {}
    for p in parts:
        if '_' not in p:
            continue
        k, v = p.split('_', 1)
        out[k] = v
    return out


def total_experience_years(exp_list: List[str]) -> int:
    # Simple heuristic: sum end - start when available. If end empty assume current year.
    import datetime
    now = datetime.datetime.utcnow().year
    total = 0
    for e in exp_list:
        parsed = parse_experience(e)
        s = parsed.get('start')
        en = parsed.get('end')
        try:
            si = int(s) if s and s.isdigit() else None
            ei = int(en) if en and en.isdigit() else None
            if si and ei:
                total += max(0, ei - si)
            elif si and not ei:
                total += max(0, now - si)
        except Exception:
            continue
    return total