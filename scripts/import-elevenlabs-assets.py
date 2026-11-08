#!/usr/bin/env python3
"""Import tool-generated ElevenLabs files from private temporary download metadata.
Signed download URLs are never copied into the game's public manifest.
"""
import json,pathlib,urllib.request,subprocess,sys,tempfile,concurrent.futures
ROOT=pathlib.Path(__file__).resolve().parents[1];OUT=ROOT/'dist/audio'
def main():
 payload=json.loads(pathlib.Path(sys.argv[1]).read_text());OUT.mkdir(parents=True,exist_ok=True)
 manifest=OUT/'manifest.json';old=json.loads(manifest.read_text()) if manifest.exists() else {};clips=old.get('clips',[]);existing={c.get('generation_id') for c in clips}
 animals=json.loads(subprocess.check_output(['node','--input-type=module','-e',"import {animals} from './dist/catalog.js'; console.log(JSON.stringify(animals.map(x=>x[1])));"],cwd=ROOT,text=True))
 families={'pet-dog':['Anjing','Rubah','Musang','Ferret'],'pet-cat':['Kucing'],'pet-horse':['Kuda','Keledai','Zebra'],'pet-small':['Hamster','Marmut','Landak','Tikus','Chinchilla','Kelinci','Tupai','Kapibara'],'pet-bird':['Ayam','Bebek'],'pet-goat':['Kambing','Domba','Sapi','Alpaka','Rusa'],'pet-reptile':['Kura-kura','Iguana','Ular']}
 jobs=[]
 for d in payload['downloads']:
  if d['generation_id'] in existing:continue
  category=d['id'];filename=category+'-'+d['generation_id']+'.mp3';jobs.append((d,filename))
 def download(job):
  d,filename=job;category=d['id'];target=OUT/filename
  try:
   with tempfile.NamedTemporaryFile(suffix='.source',delete=False) as f:
    temp=pathlib.Path(f.name)
    with urllib.request.urlopen(d['url'],timeout=60) as r:f.write(r.read())
   target_lufs=-23 if category=='music' else -19 if 'voice' in category or category=='citizen' else -22
   process=subprocess.run(['ffmpeg','-nostdin','-hide_banner','-loglevel','error','-y','-i',str(temp),'-vn','-ac','2','-ar','44100','-af',f'loudnorm=I={target_lufs}:TP=-2:LRA=11','-codec:a','libmp3lame','-b:a','128k',str(target)],capture_output=True)
   temp.unlink(missing_ok=True)
   if process.returncode:raise RuntimeError('Audio conversion failed')
   metadata=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','json',str(target)],text=True));duration=float(metadata['format']['duration'])
   c={'id':category+'-'+d['generation_id'],'category':category,'file':filename,'provider':'ElevenLabs','model':d['model'],'generation_id':d['generation_id'],'duration':round(duration,3),'loop':d['loop']}
   if category.startswith('pet-'):c['animalIds']=[i for i,species in enumerate(animals)if any(k in species for k in families.get(category,[]))]
   return c
  except Exception:
   print('Could not import',category,flush=True);return None
 with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
  for c in executor.map(download,jobs):
   if c:clips.append(c);print('Imported',c['category'],flush=True)
 desired=set(payload['desired_categories']);present={c.get('category',c['id']) for c in clips}
 data={'provider':'ElevenLabs','source':'Connected ElevenLabs Creative Studio','flow_id':payload['flow_id'],'status':'ready' if desired<=present else 'partial','expected_categories':sorted(desired),'available_categories':sorted(present),'clips':clips}
 temporary=manifest.with_suffix('.json.tmp');temporary.write_text(json.dumps(data,ensure_ascii=False,indent=2));temporary.replace(manifest)
 print(json.dumps({'clips':len(clips),'categories':len(present),'missing':sorted(desired-present)}),flush=True)
if __name__=='__main__':main()
