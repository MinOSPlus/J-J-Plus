#!/usr/bin/env python3
"""Offline-only candidate transformation. Does not modify input or official repo."""
import argparse, hashlib, pathlib, sys
p=argparse.ArgumentParser()
p.add_argument('source',type=pathlib.Path)
p.add_argument('destination',type=pathlib.Path)
a=p.parse_args()
old1=' if (code[begin]&255)!=0xff{return 0;}if (code[begin+1]&255)!=0xb5{return 0;}var base_slot:i64=jj_mto_slot_from_disp(jj_mto_rd32(code+begin+2));if base_slot<0{return 0;}'
old2=' if code[index_at]!=0x48{return 0;}if (code[index_at+1]&255)!=0x8b{return 0;}if (code[index_at+2]&255)!=0x85{return 0;}var index_slot:i64=jj_mto_slot_from_disp(jj_mto_rd32(code+index_at+3));if index_slot<0{return 0;}if base_slot==index_slot{return 0;}'
new1=' var base_slot:i64=jj_mto_load_shape(code,begin);if base_slot<0{return 0;}'
new2=' var index_slot:i64=jj_mto_moved_load_shape(code,index_at);if index_slot<0{return 0;}if base_slot==index_slot{return 0;}'
s=a.source.read_bytes()
for x in (old1,old2):
 if s.count(x.encode())!=1: sys.exit('FAIL: expected unique source block not found')
if a.destination.resolve()==a.source.resolve(): sys.exit('FAIL: refuse in-place change')
t=s.replace(old1.encode(),new1.encode()).replace(old2.encode(),new2.encode())
if len(s)-len(t)!=226:sys.exit('FAIL: unexpected delta')
a.destination.parent.mkdir(parents=True,exist_ok=True)
a.destination.write_bytes(t)
print('CANDIDATE_PATCH_APPLIED, not validated by compiler')
print('source_sha256',hashlib.sha256(s).hexdigest())
print('candidate_sha256',hashlib.sha256(t).hexdigest())
print('delta_bytes',len(s)-len(t))
