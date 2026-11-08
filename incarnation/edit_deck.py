#!/usr/bin/env python3
"""Incarnation deck edit (Nov 8, 2026):
- Replace slide 4 (word-made-flesh clip) with a link slide to the stitched full video.
- Delete the other two embedded clip slides (annunciation #9, bethlehem-night #12).
- Insert a new 'people of the video' radial slide after the film slide.
- Renumber all footers; update slide 2's segment count.
"""
import math, re, sys

PATH = '/home/hatch/workspace/ocia-slides/incarnation/index.html'
html = open(PATH, encoding='utf-8').read()

# ---------- CSS additions ----------
CSS = """
/* film link slide */
.filmlink{display:flex;flex-direction:column;align-items:center;gap:20px;margin-top:26px}
.playbtn{display:inline-flex;align-items:center;gap:16px;background:var(--maroon);border:2px solid var(--gold);color:#fff;font-size:30px;padding:22px 46px;border-radius:999px;text-decoration:none;box-shadow:0 8px 32px rgba(0,0,0,.5);font-family:inherit}
.playbtn .tri{font-size:32px;color:var(--gold-lt)}
.filmmeta{font-size:18px;color:var(--muted2);text-align:center;line-height:1.7}
.filmquote{font-size:24px;font-style:italic;color:var(--paper)}
/* people radial slide */
.people{position:relative;height:492px}
.pcenter{position:absolute;left:50%;top:45%;transform:translate(-50%,-50%);width:196px;height:196px;border-radius:50%;background:radial-gradient(circle at 50% 38%,#7a2b30,var(--maroon-dk) 72%);border:3px solid var(--gold);display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;padding:14px;z-index:2}
.pcenter .pn{font-size:31px;font-weight:700;color:#fff;line-height:1.3}
.pcenter .pr{font-size:15px;color:var(--gold-lt);line-height:1.5;margin-top:6px}
.pcard{position:absolute;width:224px;transform:translate(-50%,-50%);background:rgba(246,239,221,.07);border:1px solid rgba(201,162,39,.55);border-radius:12px;padding:9px 12px;text-align:center}
.pcard .pn{font-size:19px;font-weight:700;color:var(--gold-lt);margin-bottom:3px}
.pcard .pr{font-size:14.5px;line-height:1.45;color:var(--paper)}
.pfoot{position:absolute;left:0;right:0;bottom:-6px;text-align:center;font-size:19px;color:var(--gold-lt)}
"""
assert '/* footer */' in html
html = html.replace('/* footer */', CSS + '/* footer */', 1)

# ---------- split into head / sections / tail ----------
parts = html.split('<section')
head = parts[0]
chunks = ['<section' + p for p in parts[1:]]
assert len(chunks) == 26, f'expected 26 sections, got {len(chunks)}'
last = chunks[-1]
cut = last.index('</section>') + len('</section>')
last_section, tail = last[:cut], last[cut:]
sections = chunks[:-1] + [last_section]

def has(s, needle):
    return needle in s

# identify slides (0-based)
i_film_old = next(i for i, s in enumerate(sections) if has(s, 'word-made-flesh.mp4'))
i_annun = next(i for i, s in enumerate(sections) if has(s, 'annunciation.mp4'))
i_beth = next(i for i, s in enumerate(sections) if has(s, 'bethlehem-night.mp4'))
print('video slides at 1-based:', i_film_old + 1, i_annun + 1, i_beth + 1)

FOOT = '<div class="foot"><span>耶穌基督降生成人・聖心堂慕道班</span><span>{n} / {t}</span></div>'

film_slide = (
    '<section class="slide dark"><div class="kicker">影片</div><h1>降生成人短片・完整版</h1>'
    '<div class="filmlink">'
    '<div class="filmquote">「聖言成了血肉，寄居在我們中間。」（若 1:14）</div>'
    '<a class="playbtn" href="incarnation-reactions-dual-sub.mp4"><span class="tri">▶</span><span>播放完整短片</span></a>'
    '<div class="filmmeta">「一個嬰孩，眾多的心」——從天主的許諾，一路到黑落德的殺機，一次看完降生的故事<br>'
    '約2分20秒・英文字幕＋繁體中文字幕・短片檔案與投影片放在同一目錄</div>'
    '</div>'
    + FOOT.format(n=0, t=25) +
    '<aside class="notes">講解：完整短片（雙語字幕）：從天主的許諾、匝加利亞的懷疑、瑪利亞的「願意」，到客店主人的拒絕與黑落德的殺機。播放前提醒學員：留意片中每一個人對這嬰孩的回應——下一頁我們一起看。</aside></section>'
)

PEOPLE = [
    ('天主聖三', '「童貞女將懷孕生子」——天主的許諾（依 7:14）'),
    ('聖母瑪利亞', '「願照你的話成就於我罷！」（路 1:38）'),
    ('天使加俾額爾', '向匝加利亞與瑪利亞傳報喜訊（路 1）'),
    ('匝加利亞', '「我憑什麼知道這事？」——懷疑，因而沉默（路 1:18）'),
    ('依撒伯爾', '「我主的母親來到我這裡」——歡喜迎接（路 1:43）'),
    ('聖若瑟', '一句話也沒說，起來就遵行（瑪 1:24）'),
    ('客店主人', '「沒有地方」——把他們拒於門外（路 2:7）'),
    ('凱撒奧古斯都', '下令登記戶口，自以為掌管世界（路 2:1）'),
    ('牧羊人', '「我們往白冷去罷！」——最先聽到喜訊（路 2:15）'),
    ('三賢士', '跟隨星光，遠道而來獻禮朝拜（瑪 2:1-11）'),
    ('黑落德王', '假意朝拜，心懷殺機（瑪 2:8）'),
]
cards = []
for k, (name, role) in enumerate(PEOPLE):
    ang = math.radians(-90 + k * (360 / len(PEOPLE)))
    left = 50 + 40.5 * math.cos(ang)
    top = 45 + 41 * math.sin(ang)
    cards.append(f'<div class="pcard" style="left:{left:.1f}%;top:{top:.1f}%"><div class="pn">{name}</div><div class="pr">{role}</div></div>')

people_slide = (
    '<section class="slide dark"><div class="kicker">短片人物</div><h1>一個嬰孩，眾多的心</h1>'
    '<div class="people">'
    '<div class="pcenter"><div class="pn">耶穌基督</div><div class="pr">天主聖子<br>聖言成了血肉</div></div>'
    + ''.join(cards) +
    '<div class="pfoot">同一個嬰孩，各人不同的回應——「哪一個聲音，是你的？」</div>'
    '</div>'
    + FOOT.format(n=0, t=25) +
    '<aside class="notes">講解：短片中的人物都圍繞著中間的嬰孩耶穌：有人懷疑（匝加利亞），有人說「願意」（瑪利亞），有人默默遵行（若瑟），有人把祂拒於門外（客店主人），有人假意朝拜（黑落德）。影片最後問：「哪一個聲音是你的？」請學員靜默想一想：我最像誰？</aside></section>'
)

# slide 2 count text
assert '70分鐘・26段' in sections[1]
sections[1] = sections[1].replace('70分鐘・26段', '70分鐘・25段')

# rebuild list: replace film slide, insert people slide after it, drop the other two
new_sections = []
for i, s in enumerate(sections):
    if i == i_film_old:
        new_sections.append(film_slide)
        new_sections.append(people_slide)
    elif i in (i_annun, i_beth):
        continue
    else:
        new_sections.append(s)
assert len(new_sections) == 25, len(new_sections)

# renumber footers
for i, s in enumerate(new_sections):
    s2, n = re.subn(r'<span>\d+ / \d+</span>', f'<span>{i + 1} / 25</span>', s)
    assert n == 1, f'footer replace failed on slide {i + 1}'
    new_sections[i] = s2

out = head + ''.join(new_sections) + tail
open(PATH, 'w', encoding='utf-8').write(out)
print('done: 25 sections written')
