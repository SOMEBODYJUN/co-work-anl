"""Run the pinned genagents implementation; this file only adapts I/O.

This is a genagents execution adapter, not a reproduction of Second Me or
ThinkPersona training, and not evidence that an author has been cloned.
Upstream prompts, memory scoring, retrieval, reflection, response parsing and
state serialization are executed from the submodule, not reimplemented here.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import sys
import time
import types
import zipfile


HERE = Path(__file__).resolve().parent
FIDELITY = (
    "这是作者人格与认识重建任务。把材料中的判断作为该作者的认识来吸收；"
    "忠实保留他的观点、分析取舍、价值观和表达强度，不加入外部真假审判，"
    "不自行把明确判断弱化。作者自己提出的研究、验证与修正方法照原意吸收。"
    "不要把任何几个词当成学习目标。只按下面原版请求的格式返回结果。"
)


def digest(data):
    return hashlib.sha256(data).hexdigest()


def write_json(path, data):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_name(path.name + ".tmp")
    tmp.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    tmp.replace(path)


def prepare(archive, output, batch_chars=30000):
    """Lossless file routing. Batch size is an execution limit, not a method."""
    out = Path(output)
    out.mkdir(parents=True, exist_ok=True)
    articles = []
    with zipfile.ZipFile(archive) as z:
        for name in sorted(z.namelist()):
            basename = Path(name).name
            if not (basename[:4].isdigit() and basename[4:5] == "_"):
                continue
            if Path(name).suffix.lower() != ".md":
                continue
            raw = z.read(name)
            text = raw.decode("utf-8-sig")
            article_id = basename[:4]
            destination = out / "private" / "raw" / basename
            destination.parent.mkdir(parents=True, exist_ok=True)
            destination.write_bytes(raw)
            articles.append({
                "id": article_id, "filename": basename, "sha256": digest(raw),
                "raw_chars": len(text), "path": str(destination.resolve()),
            })
    ids = [a["id"] for a in articles]
    if len(ids) != len(set(ids)):
        raise ValueError("Duplicate article IDs; no data has been marked learned")
    batches, current, size = [], [], 0
    for a in articles:
        if current and size + a["raw_chars"] > batch_chars:
            batches.append(current)
            current, size = [], 0
        current.append(a["id"])
        size += a["raw_chars"]
    if current:
        batches.append(current)
    manifest = {
        "archive_sha256": digest(Path(archive).read_bytes()),
        "article_count": len(articles), "articles": articles,
        "batch_char_budget": batch_chars, "batches": batches,
        "formal_model": "gpt-6-astra", "formal_reasoning_effort": "max",
        "test_model": "gpt-6-sol", "learned_article_count": 0,
        "status": "input_prepared_not_learned",
    }
    write_json(out / "manifest.json", manifest)
    return manifest


class QueueTransport:
    """A fresh Work subagent answers actual upstream requests, one at a time."""

    def __init__(self, directory, model, timeout=1800, prompt_char_budget=150000):
        self.directory = Path(directory)
        self.directory.mkdir(parents=True, exist_ok=True)
        self.model, self.timeout = model, timeout
        self.prompt_char_budget = prompt_char_budget
        self.call_count = 0

    def request(self, prompt, model=None, max_tokens=1500):
        if len(prompt) > self.prompt_char_budget:
            raise RuntimeError(
                f"Native prompt is {len(prompt)} characters, above the explicit execution budget "
                f"{self.prompt_char_budget}. No text was truncated. Resolve input/retrieval capacity "
                "against the actual model before continuing; this budget is not a model-limit claim."
            )
        key = digest((self.model + "\0" + prompt).encode())
        request_path = self.directory / (key + ".request.json")
        response_path = self.directory / (key + ".response.json")
        write_json(request_path, {
            "request_id": key, "requested_model": self.model,
            "native_prompt_sha256": digest(prompt.encode()),
            "native_prompt_chars": len(prompt),
            "native_prompt": prompt, "user_fidelity_instruction": FIDELITY,
            "upstream_max_tokens_argument": max_tokens,
            "status": "awaiting_real_subagent_response",
        })
        self.call_count += 1
        with (self.directory / "calls.jsonl").open("a", encoding="utf-8") as log:
            log.write(json.dumps({"request_id": key, "event": "request", "unix_time": time.time(), "model": self.model}) + "\n")
        print(json.dumps({"waiting_for": str(request_path)}, ensure_ascii=False), flush=True)
        deadline = time.monotonic() + self.timeout
        while time.monotonic() < deadline:
            if response_path.exists():
                data = json.loads(response_path.read_text())
                if data.get("request_id") != key or data.get("model") != self.model:
                    raise ValueError("Response request/model does not match")
                if not data.get("agent_id") or not isinstance(data.get("text"), str):
                    raise ValueError("Missing actual agent identity or response text")
                # Preserve the response before upstream parsing, including
                # responses that subsequently fail in the native JSON parser.
                write_json(self.directory / "received" / f"{key}-{time.time_ns()}.json", data)
                return data["text"]
            time.sleep(0.1)
        raise TimeoutError(f"No real model response for {request_path}")


class BGEEmbedding:
    """Explicit optional encoder replacement; never advertised as OpenAI vectors.

    Long memories use overlapping encoder windows so no text is silently
    discarded. The original genagents relevance/scoring/retrieval is unchanged.
    """

    def __init__(self, model_dir):
        import numpy as np
        import onnxruntime as ort
        from tokenizers import Tokenizer
        ort.disable_telemetry_events()
        self.np = np
        self.tokenizer = Tokenizer.from_file(str(Path(model_dir) / "tokenizer.json"))
        options = ort.SessionOptions()
        options.intra_op_num_threads = 2
        self.session = ort.InferenceSession(
            str(Path(model_dir) / "onnx/model_quantized.onnx"),
            sess_options=options, providers=["CPUExecutionProvider"],
        )
        self.inputs = {i.name for i in self.session.get_inputs()}
        self.cache = {}

    def __call__(self, text, model=None):
        if text in self.cache:
            return self.cache[text]
        ids = self.tokenizer.encode(text, add_special_tokens=False).ids
        if not ids:
            raise ValueError("Cannot embed empty text")
        vectors = []
        for start in range(0, len(ids), 448):
            window = [101] + ids[start:start + 510] + [102]
            values = {
                "input_ids": self.np.array([window], dtype="int64"),
                "attention_mask": self.np.ones((1, len(window)), dtype="int64"),
                "token_type_ids": self.np.zeros((1, len(window)), dtype="int64"),
            }
            states = self.session.run(None, {k: v for k, v in values.items() if k in self.inputs})[0]
            v = states[0, 0] if states.ndim == 3 else states[0]
            vectors.append(v / self.np.linalg.norm(v))
        vector = self.np.mean(vectors, axis=0)
        vector = (vector / self.np.linalg.norm(vector)).astype(float).tolist()
        self.cache[text] = vector
        return vector


def load_native(transport, embedding_dir=None):
    source = HERE / "upstream" / "genagents"
    if not (source / "genagents/genagents.py").exists():
        raise RuntimeError("Run git submodule update --init --recursive first")
    lock = json.loads((HERE / "upstream.lock.json").read_text())["projects"]["genagents"]
    for relative, expected in lock["source_hashes"].items():
        if digest((source / relative).read_bytes()) != expected:
            raise RuntimeError(f"Pinned native source changed: {relative}")
    sys.path.insert(0, str(source))
    settings = types.ModuleType("simulation_engine.settings")
    settings.OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "work-transport-no-api-call")
    settings.KEY_OWNER = "author-learning"
    settings.DEBUG = False
    settings.MAX_CHUNK_SIZE = 4
    settings.LLM_VERS = transport.model
    settings.BASE_DIR = str(source)
    settings.POPULATIONS_DIR = str(source / "agent_bank/populations")
    settings.LLM_PROMPT_DIR = str(source / "simulation_engine/prompt_template")
    sys.modules[settings.__name__] = settings
    import simulation_engine.gpt_structure as gpt
    gpt.gpt_request = transport.request
    if embedding_dir:
        gpt.get_text_embedding = BGEEmbedding(embedding_dir)
    elif not os.environ.get("OPENAI_API_KEY"):
        raise RuntimeError("Native OpenAI embedding requires a key; select explicit --bge-model-dir for the adapted test")
    from genagents.genagents import GenerativeAgent

    # Upstream wrapper passes time_step into reflection_count. Repair only
    # argument forwarding; MemoryStream.reflect itself is the original method.
    def corrected_reflect(self, anchor, time_step=0):
        return self.memory_stream.reflect(anchor, time_step=time_step)
    GenerativeAgent.reflect = corrected_reflect
    return GenerativeAgent


def run_batch(args):
    manifest = json.loads(Path(args.manifest).read_text())
    selected = set(args.ids.split(","))
    rows = [r for r in manifest["articles"] if r["id"] in selected]
    if len(rows) != len(selected):
        raise ValueError("Unknown or duplicate article IDs")
    if args.mode == "formal" and args.model != "gpt-6-astra":
        raise ValueError("Formal batch requires user-selected gpt-6-astra / max Work subagent")
    out = Path(args.output)
    transport = QueueTransport(out / "requests", args.model, prompt_char_budget=args.prompt_char_budget)
    Native = load_native(transport, args.bge_model_dir)
    state = out / "private/native_state"
    agent = Native(str(state)) if (state / "scratch.json").exists() else Native()
    agent.update_scratch({"first_name": "窥市", "last_name": "寻真", "task": FIDELITY})
    source_map = {}
    for i, row in enumerate(rows):
        raw = Path(row["path"]).read_bytes()
        if digest(raw) != row["sha256"]:
            raise ValueError("Raw input has changed")
        content = f"[原文 {row['id']} | {row['filename']}]\n" + raw.decode("utf-8-sig")
        source_map[str(i)] = {k: row[k] for k in ("id", "filename", "sha256", "raw_chars")}
        existing = [n for n in agent.memory_stream.seq_nodes if n.node_type == "observation"]
        if i < len(existing):
            if existing[i].content != content:
                raise ValueError("Existing native state is for different input")
            continue
        agent.remember(content, time_step=i + 1)
        agent.save(str(state))
    write_json(out / "source_map.json", source_map)
    if not any(n.node_type == "reflection" for n in agent.memory_stream.seq_nodes):
        agent.reflect(anchor=args.anchor, time_step=len(rows) + 1)
        agent.save(str(state))
    answer = agent.utterance(
        [("提问者", args.question)],
        context="请依据我已有的认识回答当前问题，保留我的判断取舍和语调。",
    )
    if not isinstance(answer, str) or not answer.strip():
        raise RuntimeError("Native utterance returned no answer")
    (out / "answer.md").write_text(answer, encoding="utf-8")
    # Persist after the answer and reload through the upstream constructor.
    agent.save(str(state))
    reloaded = Native(str(state))
    assert [n.package() for n in reloaded.memory_stream.seq_nodes] == [n.package() for n in agent.memory_stream.seq_nodes]
    reflections = [{"node_id": n.node_id, "source_nodes": n.pointer_id, "text": n.content}
                   for n in agent.memory_stream.seq_nodes if n.node_type == "reflection"]
    write_json(out / "reflections.json", reflections)
    status = {
        "status": "native_genagents_chain_executed_not_author_clone_complete",
        "mode": args.mode, "requested_model": args.model,
        "article_ids": [r["id"] for r in rows],
        "source_chars": sum(r["raw_chars"] for r in rows),
        "observation_count": reloaded.memory_stream.count_observations(),
        "reflection_count": len(reflections), "native_calls": transport.call_count,
        "native_calls_scope": "current_process_including_cached_response_reads",
        "distinct_request_count": len(list((out / "requests").glob("*.request.json"))),
        "saved_and_reloaded": True,
        "upstream_commit": json.loads((HERE / "upstream.lock.json").read_text())["projects"]["genagents"]["commit"],
        "embedding_backend": "bge-small-zh-v1.5-onnx-adaptation" if args.bge_model_dir else "upstream-openai-text-embedding-3-small",
        "limitations": ["This run is not full 1508-article learning", "No Second Me or ThinkPersona training has occurred", "A completed native execution is not a fidelity score"],
    }
    write_json(out / "execution.json", status)
    (out / "DONE").write_text("native chain completed; author-clone status remains incomplete\n")
    print(json.dumps(status, ensure_ascii=False), flush=True)


def join_and_answer(args):
    """Import saved native states, remap IDs, then use the same native methods.

    No new extraction, distillation, graph method or content rewrite occurs in
    the join. The original source text, scores, embeddings and links survive.
    """
    out = Path(args.output)
    transport = QueueTransport(out / "requests", args.model, prompt_char_budget=args.prompt_char_budget)
    Native = load_native(transport, args.bge_model_dir)
    nodes, embeddings, origins, scratch = [], {}, {}, None
    for path in args.states:
        source = Path(path)
        original = Native(str(source))
        if scratch is None:
            scratch = original.scratch
        mapping = {n.node_id: len(nodes) + i for i, n in enumerate(original.memory_stream.seq_nodes)}
        for n in original.memory_stream.seq_nodes:
            row = n.package()
            row["node_id"] = mapping[n.node_id]
            if isinstance(row["pointer_id"], list):
                row["pointer_id"] = [mapping[x] for x in row["pointer_id"]]
            elif row["pointer_id"] is not None:
                row["pointer_id"] = mapping[row["pointer_id"]]
            origins[str(row["node_id"])] = {"state": str(source), "original_node_id": n.node_id}
            nodes.append(row)
        for content, vector in original.memory_stream.embeddings.items():
            if content in embeddings and embeddings[content] != vector:
                raise ValueError("Different vector versions for the same memory")
            embeddings[content] = vector
    state = out / "private/native_state"
    write_json(state / "scratch.json", scratch)
    write_json(state / "memory_stream/nodes.json", nodes)
    write_json(state / "memory_stream/embeddings.json", embeddings)
    agent = Native(str(state))
    agent.reflect(args.anchor, time_step=max([n.created for n in agent.memory_stream.seq_nodes], default=0) + 1)
    answer = agent.utterance([("提问者", args.question)], context="依据我已形成的认识分析当前问题，保留我的判断方式和语调。")
    if not isinstance(answer, str) or not answer.strip():
        raise RuntimeError("Native utterance returned no answer")
    agent.save(str(state))
    reloaded = Native(str(state))
    assert [n.package() for n in agent.memory_stream.seq_nodes] == [n.package() for n in reloaded.memory_stream.seq_nodes]
    (out / "answer.md").write_text(answer, encoding="utf-8")
    write_json(out / "source_state_map.json", origins)
    write_json(out / "reflections.json", [
        {"node_id": n.node_id, "source_nodes": n.pointer_id, "text": n.content}
        for n in agent.memory_stream.seq_nodes if n.node_type == "reflection"
    ])
    status = {"status": "native_cross_batch_use_executed_not_author_clone_complete", "mode": args.mode,
              "requested_model": args.model, "input_states": list(args.states),
              "imported_nodes": len(nodes), "observation_count": agent.memory_stream.count_observations(),
              "new_reflection_count": len(agent.memory_stream.seq_nodes) - len(nodes),
              "native_calls": transport.call_count, "saved_and_reloaded": True,
              "embedding_backend": "bge-small-zh-v1.5-onnx-adaptation" if args.bge_model_dir else "upstream-openai-text-embedding-3-small"}
    write_json(out / "execution.json", status)
    (out / "DONE").write_text("native cross-batch use completed; author clone remains incomplete\n")
    print(json.dumps(status, ensure_ascii=False), flush=True)


def main():
    p = argparse.ArgumentParser(description=__doc__)
    sub = p.add_subparsers(dest="command", required=True)
    a = sub.add_parser("prepare")
    a.add_argument("--archive", required=True)
    a.add_argument("--output", required=True)
    a.add_argument("--batch-chars", type=int, default=30000)
    a = sub.add_parser("run-batch")
    a.add_argument("--manifest", required=True)
    a.add_argument("--ids", required=True)
    a.add_argument("--output", required=True)
    a.add_argument("--model", choices=["gpt-6-sol", "gpt-6-astra"], required=True)
    a.add_argument("--mode", choices=["test", "formal"], default="test")
    a.add_argument("--bge-model-dir")
    a.add_argument("--prompt-char-budget", type=int, default=150000)
    a.add_argument("--anchor", required=True)
    a.add_argument("--question", required=True)
    a = sub.add_parser("join-and-answer")
    a.add_argument("--states", nargs="+", required=True)
    a.add_argument("--output", required=True)
    a.add_argument("--model", choices=["gpt-6-sol", "gpt-6-astra"], required=True)
    a.add_argument("--mode", choices=["test", "formal"], default="test")
    a.add_argument("--bge-model-dir")
    a.add_argument("--prompt-char-budget", type=int, default=150000)
    a.add_argument("--anchor", required=True)
    a.add_argument("--question", required=True)
    args = p.parse_args()
    if getattr(args, "bge_model_dir", None):
        # The BGE/Work-queue path needs no network. Fail closed if the OS cannot
        # prevent egress, including a dependency's unexpected telemetry.
        from offline_runtime import deny_network
        deny_network()
    if args.command == "prepare":
        result = prepare(args.archive, args.output, args.batch_chars)
        print(json.dumps({"articles": result["article_count"], "batches": len(result["batches"]), "status": result["status"]}, ensure_ascii=False))
    elif args.command == "run-batch":
        run_batch(args)
    else:
        if args.mode == "formal" and args.model != "gpt-6-astra":
            raise ValueError("Formal use requires user-selected Astra Max Work subagent")
        join_and_answer(args)


if __name__ == "__main__":
    main()
