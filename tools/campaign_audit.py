#!/usr/bin/env python3
"""Audit the explicitly requested fixed-trio campaign, preserving source gates.

This is a separate review protocol, not a claim that returning participants are
fresh reviewers. The default audit.py and its fresh-reviewer gate are unchanged.
The content snapshot pins the authorization, three actual agent identities,
participation, independent reports, and all ordinary content/evidence records.
"""
from __future__ import annotations

import copy
import json
import hashlib
import re
from pathlib import Path
import sys

import fitz
from jsonschema import Draft202012Validator
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / '.agents/skills/math-notes-evidence-audit/scripts'
sys.path.insert(0, str(SCRIPTS))
import audit as standard


POLICY_SCHEMA = {
    'type': 'object', 'additionalProperties': False,
    'required': ['mode', 'note_id', 'boss_id', 'authorization_artifact_id', 'reviewer_ids'],
    'properties': {
        'mode': {'const': 'user_requested_fixed_trio'},
        'note_id': {'type': 'string', 'minLength': 1},
        'boss_id': {'type': 'string', 'minLength': 1},
        'authorization_artifact_id': {'type': 'string', 'minLength': 1},
        'reviewer_ids': {'type': 'array', 'items': {'type': 'string', 'minLength': 1},
                         'minItems': 3, 'maxItems': 3, 'uniqueItems': True},
    },
}


class CampaignAuditor(standard.Auditor):
    def schema(self, value: dict, filename: str) -> bool:
        schema = copy.deepcopy(standard.load_json(standard.SCHEMA_DIR / filename))
        if filename == 'ledger.schema.json':
            schema['properties']['review_policy'] = POLICY_SCHEMA
            schema['required'].append('review_policy')
            crop = schema['properties']['artifacts']['items']['properties']['source_crop']
            crop['properties']['dpi'] = {'type': 'integer', 'minimum': 72, 'maximum': 1200}
            # Some source PDFs retain strokes beyond their physical MediaBox.
            # This explicitly declared viewport exposes only existing PDF marks;
            # it is not an ordinary in-page source crop.
            schema['properties']['artifacts']['items']['properties']['pdf_viewport'] = {
                'type': 'object', 'additionalProperties': False,
                'required': ['page_id', 'mediabox_pdf_pt', 'clip_pdf_pt', 'dpi'],
                'properties': {
                    'page_id': {'type': 'string', 'minLength': 1},
                    'mediabox_pdf_pt': {'type': 'array', 'minItems': 4, 'maxItems': 4,
                                       'items': {'type': 'number'}},
                    'clip_pdf_pt': {'type': 'array', 'minItems': 4, 'maxItems': 4,
                                   'items': {'type': 'number'}},
                    'dpi': {'type': 'integer', 'minimum': 72, 'maximum': 1200},
                    'form_expansion': {
                        'type': 'object', 'additionalProperties': False,
                        'required': ['xref', 'bbox_original', 'bbox_expanded',
                                     'clip_original', 'clip_expanded', 'original_stream_sha256'],
                        'properties': {
                            'xref': {'type': 'integer', 'minimum': 1},
                            'bbox_original': {'type': 'string'},
                            'bbox_expanded': {'type': 'string'},
                            'clip_original': {'type': 'string'},
                            'clip_expanded': {'type': 'string'},
                            'original_stream_sha256': {'type': 'string', 'pattern': '^[0-9a-f]{64}$'},
                        },
                    },
                },
            }
        errors = sorted(Draft202012Validator(schema).iter_errors(value), key=lambda e: str(e.path))
        for error in errors:
            self.error('SCHEMA', f'{filename} {list(error.path)}: {error.message}')
        return not errors

    def check_artifacts(self) -> dict:
        """Validate ordinary artifacts and render high-dpi crops from the PDF."""
        artifacts = self.unique_index(self.ledger['artifacts'], 'artifact')
        if not {'transcription', 'study'}.issubset({a['kind'] for a in artifacts.values()}):
            self.error('DELIVERY_CONTENT', 'one transcription and one study artifact are required')
        seen_paths = set()
        for identifier, artifact in artifacts.items():
            path = self.checked_file(self.ledger_path.parent, artifact, f'artifact:{identifier}')
            if path and path in seen_paths:
                self.error('ARTIFACT_ALIAS', f'different artifacts use the same file: {artifact["path"]}')
            if path:
                seen_paths.add(path)
            if artifact['kind'] != 'evidence' and artifact['format'] != 'text':
                self.error('ARTIFACT_FORMAT', f'content artifact {identifier} must be UTF-8 text')
            if not path:
                continue
            try:
                if artifact['format'] == 'text':
                    content = path.read_text(encoding='utf-8')
                    if artifact['kind'] == 'evidence' and not content.strip():
                        raise ValueError('empty evidence file')
                    continue
                crop = artifact.get('source_crop')
                viewport = artifact.get('pdf_viewport')
                if viewport:
                    if crop or artifact['kind'] != 'evidence':
                        raise ValueError('a PDF viewport is distinct from a normal source crop')
                    page = next((p for p in self.manifest['pages'] if p['id'] == viewport['page_id']), None)
                    if page is None:
                        raise ValueError('PDF viewport references an unknown page')
                    pdf_path = standard.safe_path(self.manifest_path.parent, self.manifest['source_pdf']['path'])
                    with fitz.open(pdf_path) as document:
                        pdf_page = document[page['number'] - 1]
                        original = pdf_page.mediabox
                        expanded = fitz.Rect(viewport['mediabox_pdf_pt'])
                        if (not expanded.contains(original) or expanded.is_empty or
                            max(abs(expanded[i] - original[i]) for i in range(4)) > 72):
                            raise ValueError('supplementary viewport must only expand the physical page by at most 72 pt')
                        pdf_page.set_mediabox(expanded)
                        form = viewport.get('form_expansion')
                        if form:
                            # Permit only expansion of an existing Form's BBox and
                            # its single rectangular clip. All drawing bytes stay
                            # identical; no general PDF code replacement occurs.
                            xref = form['xref']
                            if xref not in {item[0] for item in pdf_page.get_xobjects()}:
                                raise ValueError('expanded Form is not an XObject of the source page')
                            if document.xref_get_key(xref, 'BBox') != ('array', form['bbox_original']):
                                raise ValueError('original Form BBox differs')
                            stream = document.xref_stream(xref)
                            if hashlib.sha256(stream).hexdigest() != form['original_stream_sha256']:
                                raise ValueError('original Form stream hash differs')
                            number = r'-?(?:\d+(?:\.\d*)?|\.\d+)'
                            rect_pattern = rf'({number}) ({number}) ({number}) ({number}) re\nW\* n\n'
                            parsed = []
                            for key in ('clip_original', 'clip_expanded'):
                                match = re.fullmatch(rect_pattern, form[key])
                                if not match:
                                    raise ValueError('Form edit must contain only one rectangular clip')
                                x, y, width, height = map(float, match.groups())
                                parsed.append(fitz.Rect(x, y, x + width, y + height))
                            before, after = parsed
                            if (not after.contains(before) or after.is_empty or
                                max(abs(after[i] - before[i]) for i in range(4)) > 288):
                                raise ValueError('Form clip must only expand by at most 288 local units')
                            bboxes = []
                            for key in ('bbox_original', 'bbox_expanded'):
                                match = re.fullmatch(rf'\[({number}) ({number}) ({number}) ({number})\]', form[key])
                                if not match:
                                    raise ValueError('Form BBox must be a four-number rectangle')
                                bboxes.append(fitz.Rect(*map(float, match.groups())))
                            if (not bboxes[1].contains(bboxes[0]) or bboxes[1].is_empty or
                                max(abs(bboxes[1][i] - bboxes[0][i]) for i in range(4)) > 288):
                                raise ValueError('Form BBox must only expand by at most 288 local units')
                            old_clip, new_clip = form['clip_original'].encode(), form['clip_expanded'].encode()
                            if stream.count(old_clip) != 1:
                                raise ValueError('original clipping instruction is not unique')
                            changed = stream.replace(old_clip, new_clip, 1)
                            if changed.replace(new_clip, old_clip, 1) != stream:
                                raise ValueError('Form edit changes bytes outside its clipping rectangle')
                            document.xref_set_key(xref, 'BBox', form['bbox_expanded'])
                            document.update_stream(xref, changed)
                            pdf_page = document.reload_page(pdf_page)
                        clip = fitz.Rect(viewport['clip_pdf_pt'])
                        if clip.is_empty or not pdf_page.rect.contains(clip):
                            raise ValueError('viewport clip lies outside the declared expanded page')
                        pix = pdf_page.get_pixmap(dpi=viewport['dpi'], clip=clip,
                                                  colorspace=fitz.csRGB, alpha=False)
                        expected = Image.frombytes('RGB', [pix.width, pix.height], pix.samples)
                    with Image.open(path) as image:
                        image.load()
                        if (image.format != 'PNG' or image.size != expected.size or
                            image.convert('RGB').tobytes() != expected.tobytes()):
                            raise ValueError('viewport pixels differ from the declared original-PDF render')
                    continue
                page = next((p for p in self.manifest['pages'] if crop and p['id'] == crop['page_id']), None)
                if artifact['kind'] != 'evidence' or not crop or page is None:
                    raise ValueError('image evidence needs a source_crop page and bbox')
                box = crop['bbox_px']
                if not (0 <= box[0] < box[2] <= page['width_px'] and
                        0 <= box[1] < box[3] <= page['height_px']):
                    raise ValueError('extra crop bbox is outside source page')
                full_path = self.evidence.get(f'image:{page["id"]}')
                if full_path is None:
                    raise ValueError('extra crop full-page evidence is unverified')
                if 'dpi' in crop:
                    pdf_path = standard.safe_path(self.manifest_path.parent, self.manifest['source_pdf']['path'])
                    base_dpi = self.manifest['render']['dpi']
                    clip = fitz.Rect(*(value * 72.0 / base_dpi for value in box))
                    with fitz.open(pdf_path) as document:
                        pix = document[page['number'] - 1].get_pixmap(
                            dpi=crop['dpi'], clip=clip, colorspace=fitz.csRGB, alpha=False)
                        expected = Image.frombytes('RGB', [pix.width, pix.height], pix.samples)
                else:
                    with Image.open(full_path) as full:
                        expected = full.convert('RGB').crop(box)
                with Image.open(path) as image:
                    image.load()
                    if image.format != 'PNG' or image.size != expected.size or image.convert('RGB').tobytes() != expected.tobytes():
                        raise ValueError('extra crop pixels do not match the source PDF at the declared dpi/bbox')
            except (OSError, UnicodeError, ValueError, RuntimeError) as error:
                self.evidence.pop(f'artifact:{identifier}', None)
                self.error('ARTIFACT_INVALID', f'{identifier}: {error}')
        return artifacts

    def policy_participants(self) -> set[str]:
        policy = self.ledger['review_policy']
        participants = set(policy['reviewer_ids'])
        if policy['boss_id'] in participants:
            self.error('TRIO_BOSS', 'the integrating Boss cannot replace one of the three subagents')
        evidence_id = 'artifact:' + policy['authorization_artifact_id']
        self.references([evidence_id], 'fixed-trio authorization')
        path = self.evidence.get(evidence_id)
        if path:
            try:
                record = standard.load_json(path)
                actual = [entry['id'] for entry in record['subagents']]
                if len(actual) != 3 or len(set(actual)) != 3 or set(actual) != participants:
                    raise ValueError('authorization must register the same three distinct actual subagents')
                if record['note_id'] != policy['note_id'] or record['boss_id'] != policy['boss_id']:
                    raise ValueError('authorization note/Boss differs from the review policy')
                if record['model'] != 'gpt-6.2-sol' or record['reasoning_effort'] != 'max':
                    raise ValueError('campaign requires gpt-6.2-sol / max')
                if len(record['authorization'].strip()) < 24 or len(record['independence_scope'].strip()) < 24:
                    raise ValueError('explicit authorization and participation disclosure are required')
            except (OSError, ValueError, KeyError, TypeError) as error:
                self.error('TRIO_AUTHORIZATION', str(error))
        return participants

    def check_rounds(self, issues: dict) -> None:
        """Same complete-snapshot gates, with the declared fixed-trio identity rule."""
        participants = self.policy_participants()
        rounds = self.ledger['final_rounds']
        self.unique_index(rounds, 'final round')
        reviewers, sessions = set(), set()
        prior_evidence_paths = set(self.evidence.values()) | self.protected
        audit_evidence_paths, audit_evidence_hashes = set(), set()
        previous = None
        for number, record in enumerate(rounds, 1):
            identifier = record['id']
            if record['round'] != number:
                self.error('ROUND_SEQUENCE', f'{identifier}: rounds must be consecutive starting at 1')
            if record['previous_round_sha256'] != previous or record['record_sha256'] != standard.round_hash(record):
                self.error('ROUND_HASH_CHAIN', f'{identifier}: altered, unsealed, or broken previous-round link')
            previous = record['record_sha256']
            if record['reviewer_id'] not in participants or record['reviewer_id'] in reviewers:
                self.error('ROUND_REVIEWER', f'{identifier}: each round requires a different registered trio member')
            if record['session_id'] in sessions:
                self.error('ROUND_SESSION', f'{identifier}: a final-round session was reused')
            reviewers.add(record['reviewer_id'])
            sessions.add(record['session_id'])
            for phase in ['blind_reading', 'report']:
                item = record[phase]
                path = self.checked_file(self.ledger_path.parent, item, f'round:{identifier}:{phase}')
                if path:
                    if path in prior_evidence_paths or path in audit_evidence_paths or item['sha256'] in audit_evidence_hashes:
                        self.error('ROUND_EVIDENCE_REUSE', f'{identifier}/{phase}: independent files and content are required')
                    audit_evidence_paths.add(path)
                    audit_evidence_hashes.add(item['sha256'])
                    try:
                        if len(path.read_text(encoding='utf-8').strip()) < 8:
                            raise ValueError('review evidence must be substantive UTF-8 text')
                    except (OSError, UnicodeError, ValueError) as error:
                        self.evidence.pop(f'round:{identifier}:{phase}', None)
                        self.error('ROUND_EVIDENCE_INVALID', f'{identifier}/{phase}: {error}')
            self.references(record['evidence_ids'], identifier)
            for finding in record['findings']:
                if finding not in issues:
                    self.error('ROUND_FINDING', f'{identifier}: finding {finding} needs an issue record')
        if len(rounds) != 3 or reviewers != participants:
            self.error('FINAL_THREE_ROUNDS', 'exactly three complete rounds by all three registered agents are required')
        scope = standard.expected_scope(self.manifest, self.ledger)
        required_images = {f'image:{identifier}' for identifier in scope['page_ids'] + scope['region_ids']}
        for record in rounds[-3:]:
            identifier = record['id']
            if record['snapshot_sha256'] != self.snapshot:
                self.error('ROUND_SNAPSHOT', f'{identifier}: snapshot differs from current delivery files and records')
            if record['findings'] != []:
                self.error('FINAL_FINDINGS', f'{identifier}: final rounds must have an empty new-findings list')
            for field, ids in scope.items():
                if set(record['scope'][field]) != set(ids):
                    self.error('ROUND_SCOPE', f'{identifier}/{field}: complete current inventory required')
            notes = [entry['page_id'] for entry in record['page_notes']]
            if len(notes) != len(set(notes)) or set(notes) != set(scope['page_ids']):
                self.error('ROUND_PAGE_NOTES', f'{identifier}: every physical page needs an observation')
            self.references(record['evidence_ids'], identifier, required_images)

    def run(self) -> dict:
        report = super().run()
        report['review_protocol'] = 'user_requested_fixed_trio'
        report['fresh_final_reviewers_claimed'] = False
        report['limitations'] = list(report['limitations']) + [
            '本次按用户要求由当前篇固定三名代理跨阶段独立复核；不声称终审代理此前未参与当前篇。']
        return report


if __name__ == '__main__':
    # Use the unchanged CLI snapshot/seal implementation and the explicit audit class.
    standard.Auditor = CampaignAuditor
    standard.main()
