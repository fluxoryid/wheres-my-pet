#!/usr/bin/env python3
"""Generate the game's audio directly with the official ElevenLabs API.
Reads ELEVENLABS_API_KEY from the environment or ignored private .env.local. Never stores it or sends it to the game.
Requests are sequential and resumable: previously generated clips are retained.
"""
import json,os,sys,pathlib,urllib.request,urllib.error,time
ROOT=pathlib.Path(__file__).resolve().parents[1]
OUT=ROOT/'dist'/'audio'
VOICE=os.environ.get('ELEVENLABS_VOICE_ID','EXAVITQu4vr4xnSDxMaL')
SFX=[
 ('birds',10,True,'Small songbirds chirping naturally in a leafy city park, several individual distant birds, outdoor stereo ambience, no music or voices.'),
 ('wind',12,True,'Gentle breeze rustling tree leaves and grass, soft natural outdoor wind, seamless background ambience, no birds no voices no music.'),
 ('river',12,True,'Deep flowing urban river, rippling current and gentle water lapping against stone embankment, close natural field recording, no music.'),
 ('traffic',12,True,'Dense city traffic, several passenger car engines idling and passing at moderate speed, tire noise on asphalt, outdoor field recording without horns or music.'),
 ('horn',3,False,'Two short friendly city car horn honks from different vehicles, one low then one high, natural realistic exterior recording, no music.'),
 ('crowd',12,True,'Busy pedestrian street, soft overlapping natural conversational murmur in Indonesian, several adults chatting while walking, indistinct words, no music.'),
 ('footsteps',6,True,'First person walking footsteps at natural steady pace, trainers on concrete pavement, close dry foley, no voices no music.'),
 ('tools',8,True,'Metal hook and padlock being carefully manipulated, light metal rattles, scraping and small clicks, close realistic foley, no music.'),
 ('welding',8,True,'Small electric welding torch working on a metal padlock, controlled welding crackle and soft electric hiss, close realistic foley, no music.'),
 ('pet-dog',4,False,'Friendly pet dog gives two soft barks and a small curious whine, natural clean outdoor recording, no voices no music.'),
 ('pet-cat',4,False,'Friendly pet cat makes two clear meows and a short quiet purr, natural clean close recording, no voices no music.'),
 ('pet-horse',4,False,'A horse gives a gentle whinny and snorts, clean natural outdoor recording, no voices or music.'),
 ('pet-small',4,False,'Small pet rodent soft squeaks and quiet rustling as it sniffs and moves, subtle natural close recording, no music.'),
 ('pet-bird',4,False,'A duck quacks twice then a chicken softly clucks, natural pet bird sounds outdoors, no music.'),
 ('pet-goat',4,False,'Small domestic goat bleating gently twice in an outdoor yard, natural clean animal recording, no music.'),
 ('success',3,False,'Playful friendly success chime with soft wooden percussion and a warm upward bell flourish, gentle family adventure game sound, no speech.'),
 ('pickup',2,False,'Soft happy animal rescue interaction chime with a short gentle jingle of a pet collar, clean family game foley.')]
SPEECH=[('citizen','Halo! Tadi saya melihat hewan berkalung merah lewat di dekat taman. Coba periksa jejak terakhir di peta, ya.'),('owner-voice','Terima kasih sudah membantu. Dia sangat berarti bagi saya. Tolong bawa dia pulang dengan selamat.'),('rescue-voice','Hewannya ada di dalam truk. Gunakan alat di kompartemen dan buka kandangnya sebelum patroli kembali.')]
def safe_request(path,body,key):
 req=urllib.request.Request('https://api.elevenlabs.io'+path,data=json.dumps(body).encode(),headers={'xi-api-key':key,'Content-Type':'application/json','Accept':'audio/mpeg'},method='POST')
 try:
  with urllib.request.urlopen(req,timeout=120) as response:
   data=response.read()
   if not response.headers.get('Content-Type','').startswith('audio/'):raise RuntimeError('Provider returned a non-audio response.')
   return data
 except urllib.error.HTTPError as e:
  # Intentionally omit provider response bodies, request headers and secret values.
  if e.code==401:raise RuntimeError('ElevenLabs rejected the API key or its permissions (401).') from None
  if e.code==402:raise RuntimeError('ElevenLabs requires sufficient credits or an eligible plan (402).') from None
  if e.code==429:raise RuntimeError('ElevenLabs rate limit reached. Retry later; completed clips are retained (429).') from None
  raise RuntimeError(f'ElevenLabs request failed (HTTP {e.code}).') from None
 except urllib.error.URLError:raise RuntimeError('Could not connect to api.elevenlabs.io. Check the environment network settings.') from None
def main():
 key=os.environ.get('ELEVENLABS_API_KEY')
 if not key:
  private=ROOT/'.env.local'
  if private.exists():
   for line in private.read_text().splitlines():
    if line.startswith('ELEVENLABS_API_KEY='):
     key=line.split('=',1)[1].strip().strip(chr(34)).strip(chr(39))
     break
 if not key:print('Missing ELEVENLABS_API_KEY. Add it through secure environment settings, never through chat.');return 2
 OUT.mkdir(parents=True,exist_ok=True);clips=[]
 existing=OUT/'manifest.json'
 if existing.exists():clips=json.loads(existing.read_text()).get('clips',[])
 def commit():
  data={'provider':'ElevenLabs','source':'https://api.elevenlabs.io','status':'ready' if clips else 'requires_connection','clips':clips}
  tmp=OUT/'manifest.json.tmp';tmp.write_text(json.dumps(data,indent=2));tmp.replace(existing)
 try:
  from_catalog=json.loads((ROOT/'dist'/'models'/'manifest.json').read_text())['models']
  names=[x.get('description','') for x in from_catalog if x['name'].startswith('pet-')]
  for clip_id,duration,loop,prompt in SFX:
   if any(c['id']==clip_id for c in clips)and(OUT/(clip_id+'.mp3')).exists():continue
   data=safe_request('/v1/sound-generation?output_format=mp3_44100_128',{'text':prompt,'duration_seconds':duration,'loop':loop,'model_id':'eleven_text_to_sound_v2','prompt_influence':.35},key)
   (OUT/(clip_id+'.mp3')).write_bytes(data);record={'id':clip_id,'file':clip_id+'.mp3','provider':'ElevenLabs','model':'eleven_text_to_sound_v2','loop':loop,'duration':duration}
   if clip_id.startswith('pet-'):
    keywords={'pet-dog':['Anjing','Rubah','Musang','Ferret'],'pet-cat':['Kucing'],'pet-horse':['Kuda','Keledai','Zebra'],'pet-small':['Hamster','Marmut','Landak','Tikus','Chinchilla','Kelinci','Tupai','Kapibara'],'pet-bird':['Ayam','Bebek'],'pet-goat':['Kambing','Domba','Sapi','Alpaka','Rusa']}[clip_id]
    record['animalIds']=[i for i,n in enumerate(names)if any(k in n for k in keywords)]
   clips.append(record);commit();print('Generated',clip_id)
  for clip_id,text in SPEECH:
   if any(c['id']==clip_id for c in clips)and(OUT/(clip_id+'.mp3')).exists():continue
   data=safe_request('/v1/text-to-speech/'+VOICE+'?output_format=mp3_44100_128',{'text':text,'model_id':'eleven_multilingual_v2','voice_settings':{'stability':.55,'similarity_boost':.65}},key)
   (OUT/(clip_id+'.mp3')).write_bytes(data);clips.append({'id':clip_id,'file':clip_id+'.mp3','provider':'ElevenLabs','model':'eleven_multilingual_v2','loop':False});commit();print('Generated',clip_id)
 except RuntimeError as e:print(str(e));return 1
 print('Audio pack ready:',len(clips),'ElevenLabs clips.');return 0
if __name__=='__main__':sys.exit(main())
