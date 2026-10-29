"""Typed immutable records for the canonical epistemic hypergraph."""

from __future__ import annotations

import copy
import hashlib
import json
from dataclasses import dataclass, field
from types import MappingProxyType
from typing import Any, Iterable, Mapping


def _canonical(value: Any) -> bytes:
    return json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
        default=str,
    ).encode("utf-8")


def _freeze(value: Any) -> Any:
    if isinstance(value, Mapping):
        return MappingProxyType({
            str(key): _freeze(item) for key, item in value.items()
        })
    if isinstance(value, (list, tuple)):
        return tuple(_freeze(item) for item in value)
    if isinstance(value, set):
        return tuple(sorted((_freeze(item) for item in value), key=repr))
    return copy.deepcopy(value)


def thaw(value: Any) -> Any:
    if isinstance(value, Mapping):
        return {str(key): thaw(item) for key, item in value.items()}
    if isinstance(value, tuple):
        return [thaw(item) for item in value]
    return copy.deepcopy(value)


def content_id(kind: str, payload: Mapping[str, Any], *,
               length: int = 32) -> str:
    """Return a deterministic typed identifier for a graph object."""
    if not kind:
        raise ValueError("content id kind is required")
    digest = hashlib.sha256(
        kind.encode("utf-8") + b":" + _canonical(thaw(payload))
    ).hexdigest()
    return digest[:length]


@dataclass(frozen=True)
class NodeRecord:
    node_id: str
    kind: str
    attributes: Mapping[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not self.node_id or not self.kind:
            raise ValueError("node_id and kind are required")
        object.__setattr__(self, "attributes", _freeze(self.attributes))

    def to_json(self) -> dict[str, Any]:
        return {
            "node_id": self.node_id,
            "kind": self.kind,
            "attributes": thaw(self.attributes),
        }

    @classmethod
    def from_json(cls, value: Mapping[str, Any]) -> "NodeRecord":
        return cls(
            node_id=str(value["node_id"]),
            kind=str(value["kind"]),
            attributes=dict(value.get("attributes", {})),
        )


@dataclass(frozen=True)
class HyperEdgeRecord:
    edge_id: str
    kind: str
    source_ids: tuple[str, ...]
    target_ids: tuple[str, ...]
    attributes: Mapping[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        sources = tuple(str(value) for value in self.source_ids)
        targets = tuple(str(value) for value in self.target_ids)
        if not self.edge_id or not self.kind:
            raise ValueError("edge_id and kind are required")
        if not sources or not targets:
            raise ValueError("a hyperedge needs sources and targets")
        if len(set(sources)) != len(sources):
            raise ValueError("a hyperedge has duplicate sources")
        if len(set(targets)) != len(targets):
            raise ValueError("a hyperedge has duplicate targets")
        object.__setattr__(self, "source_ids", sources)
        object.__setattr__(self, "target_ids", targets)
        object.__setattr__(self, "attributes", _freeze(self.attributes))

    def to_json(self) -> dict[str, Any]:
        return {
            "edge_id": self.edge_id,
            "kind": self.kind,
            "source_ids": list(self.source_ids),
            "target_ids": list(self.target_ids),
            "attributes": thaw(self.attributes),
        }

    @classmethod
    def from_json(cls, value: Mapping[str, Any]) -> "HyperEdgeRecord":
        return cls(
            edge_id=str(value["edge_id"]),
            kind=str(value["kind"]),
            source_ids=tuple(value["source_ids"]),
            target_ids=tuple(value["target_ids"]),
            attributes=dict(value.get("attributes", {})),
        )


def make_node(kind: str, attributes: Mapping[str, Any], *,
              node_id: str | None = None) -> NodeRecord:
    payload = dict(attributes)
    return NodeRecord(
        node_id=node_id or content_id(f"node:{kind}", payload),
        kind=kind,
        attributes=payload,
    )


def make_edge(kind: str, source_ids: Iterable[str],
              target_ids: Iterable[str], *,
              attributes: Mapping[str, Any] | None = None,
              edge_id: str | None = None) -> HyperEdgeRecord:
    sources = tuple(str(value) for value in source_ids)
    targets = tuple(str(value) for value in target_ids)
    attrs = dict(attributes or {})
    payload = {
        "source_ids": sources,
        "target_ids": targets,
        "attributes": attrs,
    }
    return HyperEdgeRecord(
        edge_id=edge_id or content_id(f"edge:{kind}", payload),
        kind=kind,
        source_ids=sources,
        target_ids=targets,
        attributes=attrs,
    )


@dataclass(frozen=True)
class GraphSnapshot:
    revision: int
    nodes: Mapping[str, NodeRecord] = field(default_factory=dict)
    edges: Mapping[str, HyperEdgeRecord] = field(default_factory=dict)
    retired_node_ids: frozenset[str] = frozenset()
    retired_edge_ids: frozenset[str] = frozenset()
    state_root: str = ""

    def __post_init__(self) -> None:
        if self.revision < 0:
            raise ValueError("graph revision cannot be negative")
        object.__setattr__(
            self, "nodes", MappingProxyType(dict(self.nodes))
        )
        object.__setattr__(
            self, "edges", MappingProxyType(dict(self.edges))
        )
        object.__setattr__(
            self, "retired_node_ids", frozenset(self.retired_node_ids)
        )
        object.__setattr__(
            self, "retired_edge_ids", frozenset(self.retired_edge_ids)
        )

    def active_node(self, node_id: str) -> NodeRecord | None:
        if node_id in self.retired_node_ids:
            return None
        return self.nodes.get(node_id)

    def active_edge(self, edge_id: str) -> HyperEdgeRecord | None:
        if edge_id in self.retired_edge_ids:
            return None
        return self.edges.get(edge_id)

    def nodes_of_kind(self, kind: str, *,
                      active_only: bool = True) -> tuple[NodeRecord, ...]:
        return tuple(sorted(
            (
                node for node_id, node in self.nodes.items()
                if node.kind == kind and (
                    not active_only or node_id not in self.retired_node_ids
                )
            ),
            key=lambda node: node.node_id,
        ))

    def edges_of_kind(self, kind: str, *,
                      active_only: bool = True) -> tuple[HyperEdgeRecord, ...]:
        return tuple(sorted(
            (
                edge for edge_id, edge in self.edges.items()
                if edge.kind == kind and (
                    not active_only or edge_id not in self.retired_edge_ids
                )
            ),
            key=lambda edge: edge.edge_id,
        ))

    def outgoing(self, node_id: str, *,
                 kind: str | None = None) -> tuple[HyperEdgeRecord, ...]:
        return tuple(
            edge for edge in self.edges_of_kind(kind)
            if node_id in edge.source_ids
        ) if kind is not None else tuple(sorted(
            (
                edge for edge_id, edge in self.edges.items()
                if edge_id not in self.retired_edge_ids
                and node_id in edge.source_ids
            ),
            key=lambda edge: edge.edge_id,
        ))

    def incoming(self, node_id: str, *,
                 kind: str | None = None) -> tuple[HyperEdgeRecord, ...]:
        return tuple(
            edge for edge in self.edges_of_kind(kind)
            if node_id in edge.target_ids
        ) if kind is not None else tuple(sorted(
            (
                edge for edge_id, edge in self.edges.items()
                if edge_id not in self.retired_edge_ids
                and node_id in edge.target_ids
            ),
            key=lambda edge: edge.edge_id,
        ))

    def to_json(self) -> dict[str, Any]:
        return {
            "revision": self.revision,
            "nodes": [
                self.nodes[node_id].to_json()
                for node_id in sorted(self.nodes)
            ],
            "edges": [
                self.edges[edge_id].to_json()
                for edge_id in sorted(self.edges)
            ],
            "retired_node_ids": sorted(self.retired_node_ids),
            "retired_edge_ids": sorted(self.retired_edge_ids),
            "state_root": self.state_root,
        }
