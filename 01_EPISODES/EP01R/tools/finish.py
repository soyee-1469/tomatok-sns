#!/usr/bin/env python3
# One-command finishing chain: assemble picks -> subtitles -> BGM (ducked) -> title template -> social export.
# usage: finish.py <assemble_vNN.py> <tag> [--bgm-vol 0.08] [--no-template] [--no-bgm]
# outputs: edit/EP01_PICTURE_LOCK_<tag>.mp4, edit/EP01_<tag>_subs.mp4, edit/EP01_<tag>_subs_bgm.mp4, export/EP01_FINAL_<date>_<tag>.mp4
import sys,os,json,subprocess,argparse,datetime
R="/Users/ymy/project/sns/01_EPISODES/EP01R"; A="/Users/ymy/project/sns/00_MASTER_ASSETS"; F="/Users/ymy/project/ai-creative-studio/node_modules/ffmpeg-static/ffmpeg"
ap=argparse.ArgumentParser(); ap.add_argument("assemble"); ap.add_argument("tag"); ap.add_argument("--bgm-vol",type=float,default=0.08); ap.add_argument("--bgm",default=f"{A}/07_BGM/BGM_EP01_playful_sitcom_sonilo_take01.mp4")
ap.add_argument("--template",default=f"{A}/09_TEMPLATE/EP01_TITLE_topleft.png"); ap.add_argument("--no-template",action="store_true"); ap.add_argument("--no-bgm",action="store_true"); ap.add_argument("--open",action="store_true"); ap.add_argument("--final",action="store_true",help="copy to 99_FINAL/EP01_..._FINAL.mp4 (replaces the previous final)"); ap.add_argument("--final-name",default=None,help="required with --final; use the confirmed canonical filename in 99_FINAL")
o=ap.parse_args()
if o.final and not o.final_name:
    ap.error("--final requires --final-name: confirm the episode and canonical filename in 99_FINAL/README.md")
if o.final_name and (os.path.basename(o.final_name) != o.final_name or not o.final_name.endswith("_FINAL.mp4")):
    ap.error("--final-name must be a filename ending in _FINAL.mp4, without directories")
os.chdir(R); tag=o.tag
def run(a): print("$"," ".join(str(x) for x in a)[:160]); subprocess.run([str(x) for x in a],check=True)
lock=f"edit/EP01R_PICTURE_LOCK_{tag}.mp4"; run(["python3",o.assemble,lock]); J=json.load(open(lock+".json")); starts=J["starts"]; total=J["total"]; gap=J.get("bgm_gap")
subs=f"edit/EP01R_{tag}_subs.mp4"; run(["python3","tools/subtitles_pass.py",lock+".json",lock,subs]); cur=subs
if not o.no_bgm:
    bg=f"edit/EP01R_{tag}_subs_bgm.mp4"; fo=total-2.5
    run([F,"-y","-loglevel","error","-i",cur,"-i",o.bgm,"-filter_complex",f"[1:a]atrim=0:{total},asetpts=PTS-STARTPTS,aresample=44100,volume={o.bgm_vol},afade=t=in:st=2.0:d=1.0,volume=enable='lt(t,2)':volume=0,"+(f"volume=enable='between(t,{gap[0]},{gap[1]})':volume=0," if gap else "")+f"afade=t=out:st={fo:.2f}:d=2.5[bgm];[0:a]asplit=2[dlg][sc];[bgm][sc]sidechaincompress=threshold=0.05:ratio=8:attack=30:release=600:makeup=1[duck];[dlg][duck]amix=inputs=2:normalize=0:dropout_transition=0,alimiter=limit=0.95[aout]","-map","0:v","-map","[aout]","-c:v","copy","-c:a","aac","-b:a","192k","-movflags","+faststart",bg]); cur=bg
out=f"export/EP01R_FINAL_{datetime.date.today():%Y%m%d}_{tag}.mp4"; os.makedirs("export",exist_ok=True)
vf=["-map","0:v"]; ins=["-i",cur]; fc=None
if not o.no_template and os.path.exists(o.template):
    end=starts.get("OUT",total); ins+=["-loop","1","-framerate","24","-t",str(total),"-i",o.template]
    fc=f"[1]format=rgba,fade=t=in:st=0.3:d=0.4:alpha=1,fade=t=out:st={end-0.5:.2f}:d=0.4:alpha=1[t];[0:v][t]overlay=0:0:shortest=1:enable='between(t,0,{end})'[v]"; vf=["-filter_complex",fc,"-map","[v]"]
run([F,"-y","-loglevel","error",*ins,*vf,"-map","0:a","-c:v","libx264","-preset","slow","-crf","18","-profile:v","high","-level","4.1","-pix_fmt","yuv420p","-r","24","-af","loudnorm=I=-14:TP=-1.5:LRA=11","-c:a","aac","-b:a","192k","-ar","48000","-movflags","+faststart",out])
print("FINAL",out)
if o.final:
    import shutil; dst=f"/Users/ymy/project/sns/99_FINAL/{o.final_name}"; shutil.copyfile(out,dst); print("99_FINAL updated ->",dst)
    rd="/Users/ymy/project/sns/99_FINAL/README.md"; t=open(rd).read(); import re
    t=re.sub(r"\|([^|\n]*)\| "+re.escape(o.final_name)+r" \|[^\n]*\n",lambda m:f"|{m.group(1)}| {o.final_name} | {datetime.date.today()} | {os.path.basename(out)} |\n",t); open(rd,"w").write(t)
if o.open: subprocess.run(["open",dst if o.final else out])
