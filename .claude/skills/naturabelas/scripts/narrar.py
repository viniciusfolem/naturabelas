import sys,json,base64,os,urllib.request
voice,text,out=sys.argv[1],sys.argv[2],sys.argv[3]
body=json.dumps({"text":text,"model_id":"eleven_multilingual_v2","language_code":"pt","voice_settings":{"stability":0.45,"similarity_boost":0.8,"style":0.35,"use_speaker_boost":True}}).encode()
req=urllib.request.Request(f"https://api.elevenlabs.io/v1/text-to-speech/{voice}/with-timestamps?output_format=mp3_44100_128",data=body,headers={"xi-api-key":os.environ["ELEVENLABS_API_KEY"],"Content-Type":"application/json"})
try:
    d=json.load(urllib.request.urlopen(req))
except urllib.error.HTTPError as e:
    print("ERR",e.code,e.read()[:300]); sys.exit(1)
open(out+".mp3","wb").write(base64.b64decode(d["audio_base64"]))
json.dump(d["alignment"],open(out+".align.json","w"))
print("ok",out)
