"use strict";
// Preserve the full exposed old and new monthly ledgers while storing identical trajectories once.
const assert = require("node:assert/strict");
const crypto = require("node:crypto");
const fs = require("node:fs");
const path = require("node:path");
const vm = require("node:vm");
const zlib = require("node:zlib");
const {execFileSync} = require("node:child_process");
const {once} = require("node:events");
const {finished} = require("node:stream/promises");
const root = process.cwd();
const prefix = "work/boss 1/research/tasks/household_engine/";
const out = ".fresh-v2";
const oldCommit = "1580e869769a9410b88d040acf08bab394c6f9d2";
const current = "7394ed770c1b47d134bc51e64aa3bb721dc157e0";
const git = (...args) => execFileSync("git", args, {encoding:"utf8"});
const fromOld = name => git("show", oldCommit + ":" + prefix + name);
const currentFile = name => path.join(root, prefix, name);
const hash = content => crypto.createHash("sha256").update(content).digest("hex");

async function main() {
  assert.equal(git("rev-parse", "HEAD").trim(), current);
  const context = vm.createContext({});
  new vm.Script(fromOld("engine.js"), {filename:"old-engine.js"}).runInContext(context);
  const old = context.HouseholdEngine;
  const fresh = require(currentFile("engine.js"));
  const oldHouse = JSON.parse(fromOld("synthetic_household.json"));
  const newHouse = require(currentFile("synthetic_household.json"));
  const paths = require(currentFile("scenarios.json"));
  assert.deepEqual(paths, JSON.parse(fromOld("scenarios.json")));
  const earlier = old.assess(oldHouse, paths, 500);
  const later = fresh.assess(newHouse, paths, 500);
  const reference = require(currentFile("contract_migration_replay.json"));
  const fields = reference.comparedMonthlyFields;
  const zip = zlib.createGzip({level:6});
  const file = fs.createWriteStream(path.join(out, "monthly_replay.jsonl.gz"));
  zip.pipe(file);
  const emit = async record => {
    if (!zip.write(JSON.stringify(record) + "\n")) await once(zip, "drain");
  };
  await emit({type:"schema", format:"full-monthly-ledger.v1", oldCommit, current, fields,
    representation:"One trajectory line per exact JSON row-vector sequence. Each pair references an old and a current SHA-256. Values are unrounded Number, boolean or null as emitted by the engines."});
  const seen = new Set();
  const fullOld = crypto.createHash("sha256"), fullNew = crypto.createHash("sha256");
  const centOld = crypto.createHash("sha256"), centNew = crypto.createHash("sha256");
  async function capture(rows, fullHash, centHash) {
    const vectors = rows.map(row => {
      assert.deepEqual(Object.keys(row), fields);
      return fields.map(f => row[f]);
    });
    const encoded = JSON.stringify(vectors);
    const id = hash(encoded);
    fullHash.update(encoded + "\n");
    centHash.update(JSON.stringify(vectors.map(v => v.map(x => typeof x === "number" ? Math.round(x*100) : x))) + "\n");
    if (!seen.has(id)) {
      seen.add(id);
      await emit({type:"trajectory", id, rows:vectors});
    }
    return id;
  }
  let pairs = 0, monthsBefore = 0, monthsAfter = 0, rawDifferent = 0;
  for (let i = 0; i < later.results.length; i++) {
    const id = later.results[i].strategy.id;
    assert.equal(id, earlier.results[i].strategy.id);
    for (const scenario of paths) {
      const a = old.inspect(earlier, id, scenario.id).rows;
      const b = fresh.inspect(later, id, scenario.id).rows;
      const oldRows = await capture(a, fullOld, centOld);
      const newRows = await capture(b, fullNew, centNew);
      await emit({type:"pair", rule:id, scenario:scenario.id, old:oldRows, new:newRows});
      pairs++; monthsBefore += a.length; monthsAfter += b.length;
      if (oldRows !== newRows) rawDifferent++;
    }
  }
  zip.end();
  await finished(file);
  const record = {policyScenarioPairs:pairs, oldMonths:monthsBefore, newMonths:monthsAfter, fields:fields.length,
    uniqueRawSingleScenarioTrajectories:seen.size, unequalUnroundedPairs:rawDifferent,
    unroundedOldJointSHA256:fullOld.digest("hex"), unroundedNewJointSHA256:fullNew.digest("hex"),
    roundedOldJointSHA256:centOld.digest("hex"), roundedNewJointSHA256:centNew.digest("hex"),
    archiveSHA256:hash(fs.readFileSync(path.join(out,"monthly_replay.jsonl.gz")))};
  assert.equal(record.roundedOldJointSHA256, reference.oldJointRowsSHA256);
  assert.equal(record.roundedNewJointSHA256, reference.newJointRowsSHA256);
  assert.equal(pairs, reference.matchedPolicyScenarioPairs);
  assert.equal(monthsBefore, reference.observedMonthsCompared);
  console.log(JSON.stringify(record,null,2));
}
main().catch(e => {console.error(e); process.exitCode = 1;});
