"""Compiler contracts and boundary regressions; no general NE solver claim."""
from fractions import Fraction as F
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from multi_facility_spe.complement_reduction import (
    as_facility_instance, compile_game, decode_ne, rational, to_bounded_complement,
)
from multi_facility_spe.greedy_box import construct_on_path, verify_on_path

ROOT = Path(__file__).resolve().parents[1]


class ComplementReductionTests(unittest.TestCase):
    def test_actual_constructor_and_exclusion_decoding(self):
        obj = json.loads((ROOT/'examples/multi_facility/complement_source_two_speed.json').read_text())
        p = compile_game(**obj)
        inst = as_facility_instance(p)
        layout, a, audit = construct_on_path(inst)
        verify_on_path(inst,layout,a)
        self.assertEqual(p['greedy']['layout'],list(layout))
        self.assertEqual(audit['home_returns'],0)
        inverse = {old:new for new,old in enumerate(p['abstract_to_source_site'])}
        decoded = decode_ne(p,[inverse[t] for t in a[:len(obj['u'])]])
        chosen = [next(t for t in obj['A'][i] if t != decoded[i]) for i in range(len(decoded))]
        loads = [sum(F(obj['u'][i]) for i,t in enumerate(chosen) if t == s) for s in range(2)]
        for i,s in enumerate(chosen):
            t = 1-s
            self.assertLessEqual(loads[s]/obj['q'][s],(loads[t]+F(obj['u'][i]))/obj['q'][t])

    def test_empty_and_single_option_customers(self):
        for u,A in (([],[]),([F(3,7)],[[0]])):
            p=compile_game([2],[0],u,A)
            self.assertEqual(p['greedy']['multiplicities'],[2,1])
            self.assertEqual(decode_ne(p,[0]*len(u)),[0]*len(u))

    def test_bad_data_and_non_ne_decode_are_rejected(self):
        baseline=dict(q=[2,1],B=[0,0],u=[1,2],A=[[0,1],[0,1]])
        for patch in (dict(q=[True,1]),dict(B=[-1,0]),dict(u=[0,2]),
                      dict(u=[0.25,2]),dict(A=[[],[0,1]]),dict(eta='0'),dict(eta='3/4')):
            with self.subTest(patch=patch), self.assertRaises(ValueError):
                compile_game(**(baseline|patch))
        p=compile_game(**baseline)
        for a in ([0,0],[True,1],[0],[0,2]):
            with self.subTest(a=a), self.assertRaises(ValueError):
                decode_ne(p,a)

    def test_bounded_interface_keeps_all_original_deviations(self):
        obj=json.loads((ROOT/'examples/multi_facility/bounded_complement_outside_box.json').read_text())
        p=to_bounded_complement(obj['q'],obj['c'],obj['w'],obj['A'])
        self.assertEqual(p['source']['B'],['3/2','1','5/4'])
        self.assertEqual(p['lower_load'],['1','1','1'])
        self.assertEqual(p['upper_load'],['2','2','2'])
        self.assertEqual(p['initial_exclusions'],[0,1])
        for q,c,w,A in (([1,2],[0,0],['1/2'],[[0,1]]),
                        ([2,1],[0,0],[1],[[0,1]]),
                        ([2,1],[0,2],['1/2'],[[0,1]])):
            with self.assertRaises(ValueError):
                to_bounded_complement(q,c,w,A)

    def test_binary_speed_and_fraction_io_exceed_decimal_limit(self):
        before=sys.get_int_max_str_digits()
        speed=1 << 20000
        p=to_bounded_complement([speed,1],['1/2',0],['1/3'],[[0,1]])
        self.assertEqual(p['source']['q'],[speed,1])
        self.assertGreater(len(p['upper_load'][0]),6000)
        self.assertEqual(rational(p['upper_load'][0]),F(speed)*rational(p['M']))
        small='1/'+'9'*5000
        self.assertEqual(rational(small),F(1,10**5000-1))
        compiled=compile_game([1],[0],[small],[[0]])
        self.assertEqual(decode_ne(compiled,[0]),[0])
        self.assertEqual(sys.get_int_max_str_digits(),before)

    def test_cli_writes_interface_and_preserves_existing_file(self):
        with tempfile.TemporaryDirectory(prefix='complement-test-') as directory:
            output=Path(directory)/'compiled.json'
            cmd=[sys.executable,'-m','multi_facility_spe.complement_reduction',
                 'examples/multi_facility/complement_source_two_speed.json','--output',str(output)]
            first=subprocess.run(cmd,cwd=ROOT,text=True,capture_output=True)
            self.assertEqual(first.returncode,0,first.stderr)
            original=output.read_bytes()
            self.assertEqual(json.loads(original)['target']['k'],4)
            second=subprocess.run(cmd,cwd=ROOT,text=True,capture_output=True)
            self.assertNotEqual(second.returncode,0)
            self.assertIn('Refusing to overwrite',second.stderr)
            self.assertEqual(output.read_bytes(),original)


if __name__ == '__main__':
    unittest.main()
