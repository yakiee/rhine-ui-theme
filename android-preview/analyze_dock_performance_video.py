from pathlib import Path
import sys
import json
import statistics
sys.path.insert(0, 'rhine_exact/tools')
import cv2
from PIL import Image, ImageDraw

label = sys.argv[1]
out = Path('rhine_exact/output/animation-performance-20260915')
capture = cv2.VideoCapture(str(out / (label + '.mp4')))
targets = [.5, 1.2, 1.8, 2.5, 3.4, 4.3, 5.2, 6.1, 7.0, 8.2]
frames = []
times = []
changes = []
previous = None
while True:
    ok, frame = capture.read()
    if not ok:
        break
    timestamp = capture.get(cv2.CAP_PROP_POS_MSEC) / 1000
    times.append(timestamp)
    gray = cv2.cvtColor(frame[500:1420, 330:700], cv2.COLOR_BGR2GRAY)
    if previous is not None:
        changes.append(float(cv2.absdiff(gray, previous).mean()))
    previous = gray
    if len(frames) < len(targets) and timestamp >= targets[len(frames)]:
        picture = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        picture.thumbnail((160, 348))
        frames.append((timestamp, picture))
capture.release()
contact = Image.new('RGB', (800, 736), '#222222')
draw = ImageDraw.Draw(contact)
for index, (timestamp, picture) in enumerate(frames):
    x, y = (index % 5) * 160, (index // 5) * 368
    contact.paste(picture, (x, y+20))
    draw.text((x+5, y+3), f'{timestamp:.2f}s', fill='white')
contact.save(out / (label + '-contact.jpg'), quality=70)
intervals = [(b-a)*1000 for a,b in zip(times,times[1:]) if b>a]
report = {'frames':len(times), 'duration':times[-1] if times else None, 'encoded_interval_p50_ms':statistics.median(intervals) if intervals else None, 'encoded_interval_p95_ms':sorted(intervals)[int(.95*len(intervals))] if intervals else None, 'note':'Video encoding cadence includes launcher frames; it is not a measurement of KLWP render FPS.', 'times':times,'pixel_changes':changes}
(out / (label + '-video-analysis.json')).write_text(json.dumps(report),encoding='utf-8')
print(json.dumps({k:v for k,v in report.items() if k not in ('times','pixel_changes')}))
