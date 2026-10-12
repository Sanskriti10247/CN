#!/usr/bin/env bash
# usage: ./build.sh S1 [quality_dir]
#   -> out/with_captions/S1_captions.mp4  (captions burned in, in a strip below the picture)
#      out/without_captions/S1.mp4        (clean video + toggleable subtitle track)
#      out/without_captions/S1.srt        (sidecar subtitles)
# Audio is cleaned up on the way: rumble high-pass, light de-ess, loudness-normalised to -16 LUFS.
set -e
cd "$(dirname "$0")"
N=$1; Q=${2:-720p30}
mod=$(echo $N | tr 'S' 's')
SRC=media/videos/$mod/$Q/$N.mp4
W=out/with_captions; C=out/without_captions
mkdir -p $W $C
# Homebrew ffmpeg lacks libass; use the static build from the venv for burning captions.
FFB=$(.venv/bin/python -c "import imageio_ffmpeg as i;print(i.get_ffmpeg_exe())" 2>/dev/null || echo ffmpeg)
cp captions/$N.srt $C/$N.srt
AF="highpass=f=70,equalizer=f=6500:t=q:w=2:g=-3,loudnorm=I=-16:TP=-1.5:LRA=9,aresample=48000"
# captioned version: the frame is scaled to 86% and captions get their own strip underneath, so they never cover a diagram
STYLE="FontName=Helvetica Neue,FontSize=11.5,PrimaryColour=&H00FFFFFF,OutlineColour=&H00000000,Outline=0.6,Shadow=0,BorderStyle=1,MarginV=5,Alignment=2"
LB="scale=1104:622,pad=1280:720:88:2:color=0x0d0f14"
ffmpeg -y -v error -i $SRC -i captions/$N.srt -map 0:v -map 0:a -map 1:0 \
  -c:v copy -af "$AF" -c:a aac -b:a 192k -c:s mov_text -metadata:s:s:0 language=eng -movflags +faststart $C/$N.mp4
"$FFB" -y -v error -i $SRC -vf "$LB,subtitles=captions/$N.srt:force_style='$STYLE'" -af "$AF" \
  -c:v libx264 -preset medium -crf 20 -c:a aac -b:a 192k -movflags +faststart $W/${N}_captions.mp4
ls -la $W/${N}_* $C/$N.*
