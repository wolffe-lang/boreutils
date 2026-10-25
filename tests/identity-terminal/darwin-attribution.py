#!/usr/bin/env python3
"""CI-only attribution: code x fresh oracle-build matrix on one Darwin image.

Uses owned boreutils tooling; never reads GNU implementation source. All
legacy verdicts remain real verdicts. This is a diagnostic, not a waiver.
"""
import contextlib,hashlib,importlib.machinery,importlib.util,json,os,pathlib,platform,shutil,subprocess,tempfile,tomllib
ROOT=pathlib.Path(__file__).resolve().parents[2]
if os.environ.get('GITHUB_ACTIONS')!='true' or platform.system()!='Darwin':
    raise SystemExit('REFUSED: this probe runs only on the disposable Darwin CI runner')
TRUNK='37e3825c1b7ba374e1480cdcddefd959f5ecdb51'
FAMILIES=['dir','vdir','numfmt','od']
base=pathlib.Path(tempfile.mkdtemp(prefix='bu35-darwin-',dir=os.environ['RUNNER_TEMP']))
logs=base/'logs';logs.mkdir()
print('ATTRIBUTION_ROOT',base,flush=True)
def command(argv,cwd=ROOT,env=None,log=None):
    if log:
        with log.open('w') as f:r=subprocess.run(argv,cwd=cwd,env=env,stdout=f,stderr=subprocess.STDOUT)
        if r.returncode:print(log.read_text(),flush=True)
    else:r=subprocess.run(argv,cwd=cwd,env=env)
    if r.returncode:raise SystemExit(f'REFUSED: command exit{r.returncode}: {argv!r}')
command(['git','fetch','--no-tags','--depth=1','origin',TRUNK])
trunk=base/'trunk';command(['git','worktree','add','--detach',str(trunk),TRUNK])
print('CODE_HEAD',subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT).decode().strip(),'TRUNK',TRUNK,flush=True)
headpin=tomllib.loads((ROOT/'wolf-toolchain.toml').read_text());oldpin=tomllib.loads((trunk/'wolf-toolchain.toml').read_text())
assert [(headpin[k]['version'] if k!='std' else headpin[k]['rev']) for k in ['wolf','lupin','std']]==[(oldpin[k]['version'] if k!='std' else oldpin[k]['rev']) for k in ['wolf','lupin','std']]
compiler={**os.environ,'WOLF_BIN':str(ROOT/'.wolf-bin/wolf'),'LUPIN_BIN':str(ROOT/'.wolf-bin/lupin'),'WOLF_STD':str(ROOT/'.wolf-bin/std')}
command(['tools/build',*FAMILIES,'date'],cwd=trunk,env=compiler,log=logs/'build-trunk.log')
command(['tools/build',*FAMILIES,'date'],env=compiler,log=logs/'build-head.log')
stages={}
for name,code in [('trunk-config',trunk),('head-config',ROOT)]:
    # Fresh stage prevents a matching host GNU or an old cache from
    # turning this into an accidental comparison against the same build.
    stage_root=base/name;stage_root.mkdir();(stage_root/'tools').mkdir()
    for f in ['fetch-oracle','lib-toml.sh']:shutil.copy2(code/'tools'/f,stage_root/'tools'/f)
    shutil.copy2(code/'gnu-oracle.toml',stage_root/'gnu-oracle.toml')
    config=tomllib.loads((stage_root/'gnu-oracle.toml').read_text())['oracle']
    print('ORACLE_CONFIGURATION',name,json.dumps(config,sort_keys=True),flush=True)
    command(['tools/fetch-oracle'],cwd=stage_root,env={**os.environ,'BORE_GNU_PREFIX':'bu35-force-fresh-'},log=logs/(name+'-build.log'))
    stages[name]=stage_root/'.gnu-bin/bin'
    print((logs/(name+'-build.log')).read_text(),flush=True)
    for util in [*FAMILIES,'true','uniq','date']:
        exe=stages[name]/util;assert exe.is_file() and os.access(exe,os.X_OK),exe
        print('ORACLE_MEMBER',name,util,hashlib.sha256(exe.read_bytes()).hexdigest(),flush=True)
# Keep the originally selected head stage as a cache/build-drift control.
if (ROOT/'.gnu-bin/bin/true').is_file():stages['active-head-stage']=ROOT/'.gnu-bin/bin'
results=[]
def unbounded_show(side,result,fields):
    if result is None:return f'    {side}: TIMED OUT'
    return '\n'.join(f'    {side} {field}: {result[field]!r}' for field in fields)
for code_name,code in [('trunk-code',trunk),('head-code',ROOT)]:
    loader=importlib.machinery.SourceFileLoader('difftest_'+code_name.replace('-','_'),str(code/'tools/difftest'))
    spec=importlib.util.spec_from_loader(loader.name,loader);module=importlib.util.module_from_spec(spec);loader.exec_module(module)
    # Reporting only: execution/comparison/expected results are unmodified.
    module.show=unbounded_show
    for stage_name,stage in stages.items():
        os.environ['PATH']=str(stage)+os.pathsep+compiler['PATH'];os.environ['BORE_GNU_PREFIX']='';os.environ.pop('BORE_ORACLE_ANY',None)
        for family in FAMILIES:
            out=logs/(code_name+'--'+stage_name+'--'+family+'.log')
            with out.open('w') as stream,contextlib.redirect_stdout(stream):
                result=module.main(['--bin',str(code/'target/release'),family])
            text=out.read_text();summaries=[x for x in text.splitlines() if x.startswith('difftest: ') and 'passed,' in x]
            row={'code':code_name,'oracle':stage_name,'family':family,'exit':result,'summary':summaries[-1] if summaries else 'NO SUMMARY'};results.append(row)
            print('ATTRIBUTION_CELL',json.dumps(row,sort_keys=True),flush=True)
            for chunk in text.split('FAIL ')[1:]:
                print('EXACT_DIFF',code_name,stage_name,family,'FAIL '+chunk.split('\nok   ',1)[0].split('\nSKIP ',1)[0],flush=True)
            if result not in [0,1]:raise SystemExit('REFUSED: attribution harness did not return a verdict')
# Individual fields, never a guessed attribution from truncated matrices.
for stage_name,stage in stages.items():
    for value in ['0001-01-02 03:04:05.000000001','0100-01-02','10000-01-02','@-62167219200','@946695845','@0.120000000']:
        for fmt in ['%c','%Ec','%N','%-N','%-8N','%_N','%Y','%F','%G']:
            env={**os.environ,'LC_ALL':'C','TZ':'UTC0','_POSIX2_VERSION':'200112'}
            for side,exe in [('GNU',stage/'date'),('BORE',ROOT/'target/release/date')]:
                r=subprocess.run([str(exe),'-d',value,'+'+fmt],capture_output=True,env=env)
                print('ISOLATED_DATE_FIELD',json.dumps({'oracle':stage_name,'side':side,'input':value,'format':fmt,'exit':r.returncode,'stdout':repr(r.stdout),'stderr':repr(r.stderr)},sort_keys=True),flush=True)
print('ATTRIBUTION_MATRIX',json.dumps(results,sort_keys=True),flush=True)
print('ATTRIBUTION_COMPLETE: differences recorded, no family waived; original ls gate follows',flush=True)
