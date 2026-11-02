"""One cross-source identity comparison; no coefficient or SPE replay.

Read only route/target/rounding/name metadata from an existing TAR and its
already reviewed seat report, and compare with the newly acquired gap list.
"""
from pathlib import Path
import hashlib
import json
import re
import sys
import tarfile
import time


def identity(path):
    data = path.read_bytes()
    return {"path": str(path), "size": len(data), "sha256": hashlib.sha256(data).hexdigest()}


def serial(keys):
    return [{"route": list(route), "K": target} for route, target in sorted(keys)]


def main():
    if len(sys.argv) != 2:
        raise SystemExit("usage: review_gap_keys_once.py REPO_ROOT")
    repo = Path(sys.argv[1]).resolve()
    here = Path(__file__).resolve().parent
    gap = here / "original" / "4c4b8e8f667a42cc4cee" / "research4_seven_maxima_n6_gap.md"
    archive = repo / "archives/customer-attraction/tools/evidence/seven-maxima/86a32ad290bde4d6e34d.raw"
    old_report = repo / "archives/customer-attraction/tools/evidence/seven-maxima/independent_seat_assets.json"
    output = here / "gap-key-review-001"
    if output.exists():
        raise SystemExit("output exists; preserve this event and use a package copy for replay")
    before = {"gap": identity(gap), "TAR": identity(archive), "seat_report": identity(old_report)}
    assert before["gap"]["sha256"] == "f2d2d4a88ec0df49b66dcad5c6bbf5da0ca897b270b1da51c902ac5b52fb44be"
    assert before["TAR"]["sha256"] == "cae7856e0b44336502dec2f20e162b78053fe264a80414000910150af849f9a2"
    start_utc = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    start = time.perf_counter()
    text = gap.read_text()
    block = text.split("```text", 1)[1].split("```", 1)[0]
    entries = []
    for route, targets in re.findall(r"(?<!\d)([0-6]{6}):([0-9,]+)", block):
        entries.extend((tuple(map(int, route)), int(k)) for k in targets.split(","))
    assert entries and len(entries) == len(set(entries))
    listed = set(entries)
    with tarfile.open(archive, "r:*") as tar:
        members = [m for m in tar.getmembers() if m.name.endswith("seven_maxima_new_rows/scan_n6_seat.json")]
        assert len(members) == 1
        stream = tar.extractfile(members[0])
        assert stream is not None
        scan_bytes = stream.read()
        scan = json.loads(scan_bytes)
    report = json.loads(old_report.read_bytes())["n6"]
    key = lambda record: (tuple(record["route"]), record.get("target", record.get("K")))
    all_scan = {key(x) for x in scan["certificates"]}
    direct = {key(x) for x in scan["certificates"] if "multipliers" in x}
    failures = {key(x) for x in scan["failures"]}
    rounding = {key(x) for x in scan["failures"] if x.get("rounding_failed")}
    genuine = failures - rounding
    reviewed = {key(x) for x in report["certificates"]}
    missing = {key(x) for x in report["missing_orbits"]}
    elapsed = time.perf_counter() - start
    after = {"gap": identity(gap), "TAR": identity(archive), "seat_report": identity(old_report)}
    assert before == after
    extra = reviewed - direct
    extra_records = [x for x in report["certificates"] if key(x) in extra]
    result = {
        "status": "completed-metadata-comparison", "input_identity": before,
        "source_prepost_identical": True,
        "TAR_member": {"name": members[0].name, "size": len(scan_bytes),
                       "sha256": hashlib.sha256(scan_bytes).hexdigest()},
        "counts": {"new_gap_list": len(listed), "scan_certificates": len(all_scan),
                   "scan_with_multipliers": len(direct), "scan_failures": len(failures),
                   "scan_rounding_failures": len(rounding), "scan_nonrounding_failures": len(genuine),
                   "report_reviewed_keys": len(reviewed), "report_missing_keys": len(missing)},
        "new_list_equals_scan_nonrounding_failures": listed == genuine,
        "new_list_equals_report_missing": listed == missing,
        "list_minus_scan_failures": serial(listed - failures),
        "scan_failures_minus_list": serial(failures - listed),
        "list_minus_report_missing": serial(listed - missing),
        "report_missing_minus_list": serial(missing - listed),
        "report_keys_not_in_original_direct_assets": serial(extra),
        "extra_report_records": extra_records,
        "rounding_records": [x for x in scan["failures"] if x.get("rounding_failed")],
        "direct_keys_not_in_report": serial(direct - reviewed),
        "reviewed_union_missing_equals_all_scan": reviewed | missing == all_scan,
        "reviewed_and_missing_disjoint": not (reviewed & missing),
        "new_gap_list_all_entries": serial(listed),
        "target_values": sorted({K for _, K in listed}),
        "scope": "route/target/name/rounding identity only; no certificate residual or asset-tree validity replay",
        "execution": {"run_count": 1, "start_utc": start_utc,
                      "argv": sys.argv, "elapsed_seconds": elapsed,
                      "native_dense_checker_calls": 0, "native_direct_probe_calls": 0,
                      "LP_calls": 0, "seat_coefficient_replay_calls": 0, "SPE_calls": 0}
    }
    output.mkdir()
    (output / "review.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps({"counts": result["counts"],
                      "listed_equals_nonrounding": listed == genuine,
                      "listed_equals_missing": listed == missing,
                      "extra_reviewed": serial(extra), "seconds": elapsed}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
