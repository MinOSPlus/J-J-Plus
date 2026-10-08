import subprocess,sys,tempfile,pathlib
script=pathlib.Path(__file__).with_name('AL1_recovery_apply.py')
old1=' if (code[begin]&255)!=0xff{return 0;}if (code[begin+1]&255)!=0xb5{return 0;}var base_slot:i64=jj_mto_slot_from_disp(jj_mto_rd32(code+begin+2));if base_slot<0{return 0;}'
old2=' if code[index_at]!=0x48{return 0;}if (code[index_at+1]&255)!=0x8b{return 0;}if (code[index_at+2]&255)!=0x85{return 0;}var index_slot:i64=jj_mto_slot_from_disp(jj_mto_rd32(code+index_at+3));if index_slot<0{return 0;}if base_slot==index_slot{return 0;}'
with tempfile.TemporaryDirectory() as t:
 d=pathlib.Path(t); src=d/'original.j'; dst=d/'candidate.j'; src.write_text('fn test()->i64{\n'+old1+'\n'+old2+'\nreturn 0;}\n')
 def run(s,d):return subprocess.run([sys.executable,str(script),str(s),str(d)],text=True,capture_output=True)
 r=run(src,dst); assert r.returncode==0,(r.stderr,r.stdout); assert len(src.read_bytes())-len(dst.read_bytes())==226
 print('PASS exact-two-block replacement; delta_bytes=226')
 r=run(src,src);assert r.returncode!=0;print('PASS refuses source=destination')
 bad=d/'bad.j';bad.write_text(src.read_text().replace('code[index_at+2]','code[index_at+9]')); r=run(bad,d/'bad-output.j');assert r.returncode!=0 and not (d/'bad-output.j').exists(); print('PASS fail-closed on altered pattern, no output')
 dup=d/'duplicate.j';dup.write_text(src.read_text()+old1);r=run(dup,d/'duplicate-output.j'); assert r.returncode!=0;print('PASS fail-closed on non-unique match')
print('RESULT=4/4 patch-mechanics gates PASS; compiler/selfhost NOT TESTED')
