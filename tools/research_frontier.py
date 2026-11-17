"""Read-only, branch-preserving consumption of research_runtime.context().

The fixed point below assumes every textual condition has been checked. It is
an aid for locating work, never a mathematical verdict or a registry update.
"""
from __future__ import annotations

import argparse
import copy
import json
import os
from pathlib import Path
import re
import subprocess
import sys
from urllib.parse import urlsplit, urlunsplit

import research_runtime as runtime


POSITIVE = runtime.LOGICAL - {"refutes"}
ROUTING = {"GIT_DIR", "GIT_WORK_TREE", "GIT_COMMON_DIR", "GIT_INDEX_FILE",
           "GIT_OBJECT_DIRECTORY", "GIT_ALTERNATE_OBJECT_DIRECTORIES",
           "GIT_IMPLICIT_WORK_TREE", "GIT_GRAFT_FILE", "GIT_SHALLOW_FILE",
           "GIT_PREFIX", "GIT_INTERNAL_SUPER_PREFIX"}


def _redact_remote(value):
    """A repository URL is useful provenance; embedded credentials are not."""
    if "://" in value:
        parsed = urlsplit(value)
        if "@" in parsed.netloc:
            value = urlunsplit((parsed.scheme, "[REDACTED]@" + parsed.netloc.rsplit("@", 1)[1],
                                parsed.path, parsed.query, parsed.fragment))
    return re.sub(r"(?:github_pat_|gh[pousr]_)[A-Za-z0-9_]{12,}", "[REDACTED]", value)


def repository_snapshot(root, expected_branch=None):
    """Inspect only local Git metadata, without authentication or a fetch."""
    root = Path(root).resolve()
    env = {key: value for key, value in os.environ.items() if key not in ROUTING}
    env["GIT_TERMINAL_PROMPT"] = "0"

    def git(*args, required=True):
        result = subprocess.run(["git", *args], cwd=root, env=env,
                                capture_output=True, text=True, timeout=15)
        if required and result.returncode:
            raise ValueError("Cannot inspect the local research repository")
        return result.stdout.strip() if result.returncode == 0 else None

    actual_root = git("rev-parse", "--show-toplevel")
    if Path(actual_root).resolve() != root:
        raise ValueError("--repo must name the repository root")
    snapshot = {
        "branch": git("symbolic-ref", "--quiet", "--short", "HEAD", required=False),
        "commit": git("rev-parse", "HEAD"),
        "remote": _redact_remote(git("remote", "get-url", "origin", required=False) or "") or None,
        "worktree_dirty": bool(git("status", "--porcelain")),
        "source": "local-snapshot-not-remote-confirmation",
    }
    if expected_branch is not None and snapshot["branch"] != expected_branch:
        raise ValueError("Expected branch " + expected_branch + "; observed " +
                         str(snapshot["branch"]) + " at " + snapshot["commit"])
    return snapshot


def _cyclic_components(routes, closure, bases):
    """Find cycles in the dependency projection without paying hyperedges."""
    adjacency = {}
    for route in routes:
        if not route["structurally_eligible"]:
            continue
        target = route["target_id"]
        adjacency.setdefault(target, set()).update(route["all_premises"])
        for premise in route["all_premises"]:
            adjacency.setdefault(premise, set())

    # Iterative Kosaraju avoids recursion limits on large dependency closures.
    seen, order = set(), []
    for start in sorted(adjacency):
        if start in seen:
            continue
        stack = [(start, False)]
        while stack:
            node, exiting = stack.pop()
            if exiting:
                order.append(node)
                continue
            if node in seen:
                continue
            seen.add(node)
            stack.append((node, True))
            stack.extend((child, False) for child in sorted(adjacency[node], reverse=True)
                         if child not in seen)
    reverse = {node: set() for node in adjacency}
    for node, children in adjacency.items():
        for child in children:
            reverse[child].add(node)
    seen, result = set(), []
    for start in reversed(order):
        if start in seen:
            continue
        component, stack = set(), [start]
        while stack:
            node = stack.pop()
            if node in seen:
                continue
            seen.add(node)
            component.add(node)
            stack.extend(reverse[node] - seen)
        if len(component) == 1 and start not in adjacency[start]:
            continue
        outside = sorted({premise for node in component for premise in adjacency[node]
                          if premise not in component})
        entry_routes = [route["route_id"] for route in routes
                        if route["structurally_eligible"] and route["target_id"] in component
                        and not component.intersection(route["all_premises"])
                        and set(route["all_premises"]) <= closure]
        result.append({
            "object_ids": sorted(component), "external_premise_ids": outside,
            "declared_base_ids": sorted(component & bases),
            "external_structural_entry_routes": entry_routes,
            "unresolved_object_ids": sorted(component - closure),
            "self_payment_allowed": False,
            "instruction": "A cycle supplies no initial premise. Only a declared base or an independently grounded ALL route can enter it; textual conditions still require review.",
        })
    return sorted(result, key=lambda row: row["object_ids"])


def frontier_report(ctx):
    """Return ALL/OR routes and an explicitly conditional structural fixed point.

    ``ctx`` must be an unmodified context() result. An optional ``snapshot`` is
    provenance supplied by the caller; this function performs no I/O.
    """
    objects = {obj["object_id"]: obj for obj in ctx.get("objects", [])}
    edges = {edge["edge_id"]: edge for edge in ctx.get("edges", [])}
    bases = {oid for oid, obj in objects.items()
             if obj.get("truth_status") in {"definition", "proved"}
             and obj.get("binding_status") == "current"}
    routes = []
    for target, options in sorted(ctx.get("support_options", {}).items()):
        for option in options:
            edge = edges.get(option["edge_id"], {})
            direction = option.get("direction", "forward")
            premises = list(option.get("all_premises", []))
            blockers = []
            if edge.get("status") != "accepted" or edge.get("kind") not in POSITIVE:
                blockers.append("not-an-accepted-positive-logical-relation")
            if "contribution" in edge:
                blockers.append("partial-contribution-does-not-pay-the-whole-target")
            if not isinstance(edge.get("whole_result"), str) or not edge["whole_result"].strip():
                blockers.append("whole-result-scope-requires-review")
            if direction not in {"forward", "reverse"} or (direction == "reverse" and edge.get("kind") != "equivalent_to"):
                blockers.append("invalid-logical-direction")
            expected = edge.get("source_ids", []) if direction == "forward" else edge.get("target_ids", [])
            conclusions = edge.get("target_ids", []) if direction == "forward" else edge.get("source_ids", [])
            if not premises or set(premises) != set(expected) or target not in set(conclusions) - set(premises):
                blockers.append("incomplete-or-mismatched-ALL-route")
            unknown = sorted({oid for oid in [target, *premises] if oid not in objects}
                             | set(option.get("unknown_endpoints", [])))
            changed = sorted({oid for oid in edge.get("source_ids", []) + edge.get("target_ids", [])
                              if oid in objects and objects[oid].get("binding_status") != "current"}
                             | set(option.get("endpoint_binding_changes", [])))
            if unknown:
                blockers.append("unknown-endpoints")
            if changed or edge.get("binding_status") != "current" or not option.get("current_declared_support", False):
                blockers.append("bindings-require-refresh")
            route = {
                "route_id": target + "::" + option["edge_id"] + "::" + direction,
                "target_id": target, "edge_id": option["edge_id"], "direction": direction,
                "all_premises": premises, "conclusion_ids": copy.deepcopy(option.get("conclusion_ids", conclusions)),
                "conditions": copy.deepcopy(option.get("conditions", edge.get("conditions"))),
                "scope": copy.deepcopy(option.get("scope", edge.get("scope"))),
                "relation_mode": option.get("relation_mode", edge.get("relation_mode")),
                "explanation": option.get("explanation", edge.get("explanation")),
                "proof_scope": ("step" if "contribution" in edge else
                                "whole" if edge.get("whole_result") else "unclassified"),
                "whole_result": edge.get("whole_result"),
                "contribution": copy.deepcopy(edge.get("contribution")),
                "result": copy.deepcopy(edge.get("contribution", {}).get("result", edge.get("whole_result"))),
                "remaining": copy.deepcopy(edge.get("contribution", {}).get("remaining")),
                "evidence": copy.deepcopy(option.get("evidence", edge.get("evidence", []))),
                "declaration_pin": edge.get("declaration_pin"),
                "endpoint_pins": copy.deepcopy(edge.get("endpoint_pins", {})),
                "evidence_pins": copy.deepcopy(edge.get("evidence_pins", {})),
                "review_digest": edge.get("review_digest"),
                "object_pins": {oid: objects[oid].get("registration_pin")
                                for oid in sorted(set([target, *premises])) if oid in objects},
                "declared_unpaid_premises": copy.deepcopy(option.get("unpaid_premises", [])),
                "unpaid_premises": copy.deepcopy(option.get("unpaid_premises", [])),
                "unknown_endpoints": unknown, "endpoint_binding_changes": changed,
                "binding_errors": copy.deepcopy(edge.get("binding_errors", [])),
                "structurally_eligible": not blockers, "structural_blockers": blockers,
                "condition_application_review_required": True,
            }
            routes.append(route)

    closure = set(bases)
    witnesses = {}
    while True:
        added = set()
        for route in routes:
            if (route["structurally_eligible"] and set(route["all_premises"]) <= closure
                    and route["target_id"] not in closure):
                added.add(route["target_id"])
                witnesses.setdefault(route["target_id"], []).append(route["route_id"])
        if not added:
            break
        closure.update(added)

    actions = []
    for route in routes:
        route["unresolved_premises_after_structural_closure"] = [
            {"object_id": oid, "truth_status": objects.get(oid, {}).get("truth_status", "unknown"),
             "binding_status": objects.get(oid, {}).get("binding_status", "unavailable"),
             "objections": objects.get(oid, {}).get("objections")}
            for oid in route["all_premises"] if oid not in closure]
        route["structurally_ready_assuming_conditions"] = (
            route["structurally_eligible"] and set(route["all_premises"]) <= closure)
        route["actionable_frontier"] = [{
            "kind": "condition-application-review", "conditions": route["conditions"],
            "scope": route["scope"],
            "instruction": "Read the exact bodies and evidence; check model, domain, quantifiers, variable mapping and every condition against the original problem. This review is required even for an unconditional relation.",
        }]
        if route["unresolved_premises_after_structural_closure"]:
            route["actionable_frontier"].append({
                "kind": "unresolved-ALL-premises", "premises": route["unresolved_premises_after_structural_closure"],
                "instruction": "Discharge every premise of this route, or select a genuinely independent OR alternative.",
            })
        if route["structural_blockers"]:
            route["actionable_frontier"].append({
                "kind": "route-repair-or-review", "blockers": route["structural_blockers"],
                "unknown_endpoints": route["unknown_endpoints"],
                "endpoint_binding_changes": route["endpoint_binding_changes"],
                "binding_errors": route["binding_errors"],
            })
        actions.extend(dict(action, route_id=route["route_id"]) for action in route["actionable_frontier"])

    contributions = []
    for edge in ctx.get("research_leads", []):
        if "contribution" not in edge:
            continue
        contributions.append({
            "edge": copy.deepcopy(edge), "result": edge["contribution"]["result"],
            "remaining": edge["contribution"]["remaining"],
            "pays_whole_target": False,
            "actionable_frontier": "Verify applicability of result, then prove remaining obligations. A useful independently stated subresult can be registered separately; the target is not promoted by this contribution.",
        })
        actions.append({
            "kind": "contribution-remaining", "edge_id": edge["edge_id"],
            "source_ids": copy.deepcopy(edge.get("source_ids", [])),
            "target_ids": copy.deepcopy(edge.get("target_ids", [])),
            "result": edge["contribution"]["result"], "remaining": edge["contribution"]["remaining"],
            "conditions": edge.get("conditions"), "declaration_pin": edge.get("declaration_pin"),
            "binding_status": edge.get("binding_status"), "pays_whole_target": False,
        })
    refutations = [{"edge": copy.deepcopy(edge), "precise_target_ids": list(edge.get("target_ids", [])),
                    "instruction": "Check the exact target version, assumptions and witness. Refuting an auxiliary bridge does not refute the original problem; stale or partial evidence requires targeted review."}
                   for edge in ctx.get("refutations", [])]
    for refutation in refutations:
        actions.append({"kind": "precise-refutation-review",
                        "edge_id": refutation["edge"]["edge_id"],
                        "precise_target_ids": refutation["precise_target_ids"],
                        "declaration_pin": refutation["edge"].get("declaration_pin"),
                        "binding_status": refutation["edge"].get("binding_status"),
                        "instruction": refutation["instruction"]})
    cycles = _cyclic_components(routes, closure, bases)
    for cycle in cycles:
        if cycle["unresolved_object_ids"]:
            actions.append({"kind": ("ungrounded-cycle" if not cycle["declared_base_ids"]
                                     and not cycle["external_structural_entry_routes"]
                                     else "unresolved-cyclic-dependencies"), **cycle})
    route_targets = {route["target_id"] for route in routes}
    for oid in ctx.get("seed_ids", []):
        if oid not in closure and oid not in route_targets:
            actions.append({"kind": "no-whole-support-route", "object_id": oid,
                            "truth_status": objects.get(oid, {}).get("truth_status", "unknown"),
                            "instruction": "Research this precise obligation or retrieve an applicable full support route; nearby contributions and references do not supply it."})
    snapshot = copy.deepcopy(ctx.get("snapshot", {}))
    for key in ("branch", "commit", "remote"):
        snapshot.setdefault(key, None)
    return {
        "schema": 1, "kind": "structural-frontier-not-a-mathematical-verdict",
        "snapshot": snapshot, "registry": ctx.get("registry"), "registry_pin": ctx.get("registry_pin"),
        "seed_ids": copy.deepcopy(ctx.get("seed_ids", [])),
        "closure_assumption": "Every textual condition and application mapping is assumed checked for this structural calculation only. No such review is performed or recorded by this report; membership is not an actually usable proof.",
        "declared_bases": sorted(bases),
        "structural_assuming_conditions_closure": sorted(closure),
        "structural_entry_witnesses": witnesses,
        "support_semantics": "OR between routes for the same target; ALL within a route. Each original branch remains visible even when an alternative is structurally grounded.",
        "routes": routes, "cyclic_dependency_components": cycles,
        "contributions": contributions, "refutations": refutations,
        "other_research_leads": [copy.deepcopy(edge) for edge in ctx.get("research_leads", [])
                                 if "contribution" not in edge],
        "actionable_frontier": actions,
        "unavailable_edge_files": copy.deepcopy(ctx.get("unavailable_edge_files", [])),
        "instruction": "Read and verify selected exact mathematical sources. Keep declared truth, structural support, applicability review, independent checking and publication separate. Nothing here changes registry truth or starts an agent.",
    }


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=Path, required=True)
    parser.add_argument("--registry", default=runtime.REGISTRY)
    parser.add_argument("--goal", action="append", required=True)
    parser.add_argument("--edge", action="append")
    parser.add_argument("--expect-branch")
    args = parser.parse_args(argv)
    root = args.repo.resolve()
    snapshot = repository_snapshot(root, args.expect_branch)
    ctx = runtime.context(root, args.goal, args.registry, edge_ids=args.edge)
    ctx["snapshot"] = snapshot
    print(json.dumps(frontier_report(ctx), ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (ValueError, OSError, KeyError, subprocess.TimeoutExpired) as exc:
        print(str(exc), file=sys.stderr)
        raise SystemExit(2)
