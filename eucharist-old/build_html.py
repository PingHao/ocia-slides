#!/usr/bin/env python3
"""Build a single-file offline HTML slide deck for 感恩祭（彌撒） OCIA class."""
import os, html

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "感恩祭彌撒-慕道班.html")

def esc(t):
    return html.escape(t)

def bullet_html(b):
    if isinstance(b, str):
        return f"<li>{esc(b)}</li>"
    inner = ""
    for x in b:
        if isinstance(x, tuple):
            txt, bo, it = x
            t = esc(txt)
            if bo: t = f"<b>{t}</b>"
            if it: t = f"<i>{t}</i>"
            inner += t
        else:
            inner += esc(x)
    return f"<li>{inner}</li>"

CSS = """
:root{
  --maroon:#5e1a1e; --maroon-dk:#421014; --gold:#c9a227; --gold-lt:#e4c85a;
  --cream:#fdfbf6; --parch:#f6efdd; --ink:#2b2620; --muted:#6b5d4f; --dark:#141210;
}
*{box-sizing:border-box;margin:0;padding:0}
html,body{height:100%;background:#000;overflow:hidden}
body{font-family:"Microsoft JhengHei","PingFang TC","Noto Sans TC","Heiti TC",sans-serif;color:var(--ink)}
#viewport{position:fixed;inset:0;display:flex;align-items:center;justify-content:center;background:#000}
#stage{width:1280px;height:720px;position:relative;flex:none;transform-origin:center center;background:var(--cream);overflow:hidden}
.slide{position:absolute;inset:0;display:none;padding:56px 72px;animation:fade .35s ease}
.slide.active{display:block}
@keyframes fade{from{opacity:0}to{opacity:1}}
.kicker{font-size:15px;font-weight:700;letter-spacing:6px;color:var(--gold);margin-bottom:10px}
.kicker::after{content:"";display:block;width:72px;height:3px;background:var(--gold);margin-top:8px}
h1{font-size:42px;color:var(--maroon);margin-bottom:26px;line-height:1.25}
.slide ul{list-style:none}
.slide ul li{font-size:22px;line-height:1.65;margin-bottom:14px;padding-left:28px;position:relative}
.slide ul li::before{content:"";position:absolute;left:2px;top:16px;width:10px;height:10px;background:var(--gold);border-radius:50%}
.slide ul li b{color:var(--maroon)}
blockquote{font-size:25px;line-height:1.8;font-style:italic;color:var(--ink);border-left:5px solid var(--gold);padding-left:26px;margin:6px 0 18px}
cite{display:block;font-style:normal;font-size:17px;color:var(--muted)}
.slide.parch{background:var(--parch)}
.slide.dark{background:var(--dark);color:var(--cream)}
.slide.dark h1{color:#fff}
.slide.maroon{background:var(--maroon);color:#fff}
.slide.maroon h1{color:#fff}
.slide.maroon-dk{background:var(--maroon-dk);color:#fff}
/* cover */
.cover{display:flex;align-items:center;gap:48px;height:100%}
.cover .ctext{flex:1}
.cover h1{font-size:72px;color:#fff;margin-bottom:14px}
.cover .sub{font-size:24px;font-style:italic;color:var(--gold-lt);margin-bottom:40px}
.cover .date{font-size:20px;color:#fff}
.cover .cimg{flex:0 0 380px;display:flex;justify-content:center}
.cover .cimg img{max-height:600px;max-width:380px;object-fit:contain;box-shadow:0 12px 48px rgba(0,0,0,.55);cursor:zoom-in}
/* art slides */
.artrow{display:flex;gap:44px;align-items:center;height:520px}
.artrow.flip{flex-direction:row-reverse}
.artimg{flex:1;display:flex;align-items:center;justify-content:center;min-width:0}
.artimg img{max-height:520px;max-width:100%;object-fit:contain;cursor:zoom-in;box-shadow:0 8px 32px rgba(0,0,0,.5)}
.artcap{flex:0 0 340px}
.artcap h3{font-size:24px;color:var(--gold);margin-bottom:12px;line-height:1.4}
.artcap p{font-size:18px;line-height:1.7;color:var(--cream)}
/* video */
.vidwrap{display:flex;flex-direction:column;align-items:center}
video{width:960px;max-height:500px;background:#000;box-shadow:0 8px 32px rgba(0,0,0,.5)}
.vidcap{margin-top:12px;font-size:16px;color:var(--gold-lt)}
/* takehome */
.takehome h1{font-size:44px;color:#fff;margin-bottom:36px}
.takehome .item{display:flex;gap:20px;margin-bottom:26px;align-items:baseline}
.takehome .num{font-size:34px;font-weight:700;color:var(--gold);flex:0 0 56px}
.takehome .txt{font-size:25px;color:#fff;line-height:1.5}
/* closing */
.closing{display:flex;flex-direction:column;align-items:center;justify-content:center;height:100%;text-align:center}
.closing blockquote{border:none;font-size:30px;color:#fff;padding:0;max-width:900px}
.closing .src{font-size:18px;color:var(--gold-lt);margin:14px 0 44px}
.closing .thanks{font-size:40px;font-weight:700;color:#fff;margin-bottom:16px}
.closing .srcline{font-size:13px;color:var(--gold-lt)}
/* footer */
.foot{position:absolute;left:72px;right:72px;bottom:22px;display:flex;justify-content:space-between;font-size:12px;color:var(--muted)}
.slide.dark .foot,.slide.maroon .foot,.slide.maroon-dk .foot{color:var(--gold-lt)}
/* notes */
.notes{position:absolute;left:0;right:0;bottom:0;background:rgba(20,18,16,.94);color:#ffe9a8;font-size:15px;line-height:1.6;padding:14px 72px;display:none;z-index:40;max-height:40%}
body.show-notes .notes{display:block}
/* lightbox */
#lightbox{position:fixed;inset:0;background:rgba(0,0,0,.93);display:none;align-items:center;justify-content:center;z-index:100;cursor:zoom-out}
#lightbox.open{display:flex}
#lightbox img{max-width:94vw;max-height:94vh;object-fit:contain;box-shadow:0 0 80px rgba(0,0,0,.8)}
#lightbox .lbcap{position:absolute;bottom:18px;left:0;right:0;text-align:center;color:var(--gold-lt);font-size:15px}
/* counter + hint */
#counter{position:fixed;right:18px;bottom:14px;color:#8a8a8a;font-size:13px;z-index:50}
#hint{position:fixed;left:18px;bottom:14px;color:#5a5a5a;font-size:12px;z-index:50}
"""

JS = """
const slides=[...document.querySelectorAll('.slide')];
let idx=0;
const counter=document.getElementById('counter');
function show(i){
  idx=Math.max(0,Math.min(slides.length-1,i));
  slides.forEach((s,k)=>s.classList.toggle('active',k===idx));
  counter.textContent=(idx+1)+' / '+slides.length;
  try{history.replaceState(null,'','#'+(idx+1));}catch(e){}
  const v=slides[idx].querySelector('video');
  document.querySelectorAll('video').forEach(x=>{if(x!==v)x.pause();});
}
document.addEventListener('keydown',e=>{
  if(e.key==='Escape'){closeLB();return;}
  if(document.getElementById('lightbox').classList.contains('open'))return;
  const tag=(e.target.tagName||'').toLowerCase();
  if(tag==='input'||tag==='textarea')return;
  if(['ArrowRight','PageDown',' '].includes(e.key)){e.preventDefault();show(idx+1);}
  else if(['ArrowLeft','PageUp'].includes(e.key)){e.preventDefault();show(idx-1);}
  else if(e.key==='Home'){show(0);}
  else if(e.key==='End'){show(slides.length-1);}
  else if(e.key==='f'||e.key==='F'){
    if(document.fullscreenElement)document.exitFullscreen();
    else document.documentElement.requestFullscreen().catch(()=>{});
  }
  else if(e.key==='n'||e.key==='N'){document.body.classList.toggle('show-notes');}
});
let tx=0;
document.addEventListener('touchstart',e=>{tx=e.changedTouches[0].clientX;},{passive:true});
document.addEventListener('touchend',e=>{
  const dx=e.changedTouches[0].clientX-tx;
  if(Math.abs(dx)>60)show(idx+(dx<0?1:-1));
},{passive:true});
const lb=document.getElementById('lightbox'),lbimg=document.getElementById('lbimg'),lbcap=document.getElementById('lbcap');
function openLB(src,cap){lbimg.src=src;lbcap.textContent=cap||'';lb.classList.add('open');}
function closeLB(){lb.classList.remove('open');lbimg.src='';}
lb.addEventListener('click',closeLB);
document.querySelectorAll('img.zoomable').forEach(im=>{
  im.addEventListener('click',e=>{e.stopPropagation();openLB(im.src,im.dataset.cap||'');});
});
function fit(){
  const s=Math.min(innerWidth/1280,innerHeight/720);
  document.getElementById('stage').style.transform=`scale(${s})`;
}
addEventListener('resize',fit);fit();
(function(){const m=location.hash.match(/#(\d+)/);show(m?parseInt(m[1],10)-1:0);})();
addEventListener('hashchange',()=>{const m=location.hash.match(/#(\d+)/);if(m)show(parseInt(m[1],10)-1);});
"""

def slide_open(cls=""):
    return f'<section class="slide {cls}">'

def foot(n, total):
    return f'<div class="foot"><span>感恩祭（彌撒）・聖心堂慕道班</span><span>{n} / {total}</span></div>'

def notes(t):
    return f'<aside class="notes">講解：{esc(t)}</aside>' if t else ""

def content(n, total, kicker, title, bullets, note):
    lis = "".join(bullet_html(b) for b in bullets)
    return (slide_open() +
        f'<div class="kicker">{esc(kicker)}</div><h1>{esc(title)}</h1><ul>{lis}</ul>' +
        foot(n, total) + notes(note) + "</section>")

def quote(n, total, kicker, title, text, cite, note):
    return (slide_open("parch") +
        f'<div class="kicker">{esc(kicker)}</div><h1>{esc(title)}</h1>' +
        f"<blockquote>{esc(text)}</blockquote><cite>——{esc(cite)}</cite>" +
        foot(n, total) + notes(note) + "</section>")

def art(n, total, kicker, img, cap_title, cap_text, note, flip=False):
    fcls = " flip" if flip else ""
    return (slide_open("dark") +
        f'<div class="kicker">{esc(kicker)}</div><div class="artrow{fcls}">' +
        f'<div class="artimg"><img class="zoomable" src="{esc(img)}" data-cap="{esc(cap_title)}"></div>' +
        f'<div class="artcap"><h3>{esc(cap_title)}</h3><p>{esc(cap_text)}</p></div></div>' +
        foot(n, total) + notes(note) + "</section>")

def video(n, total, kicker, title, src, poster, cap, note):
    return (slide_open("dark") +
        f'<div class="kicker">{esc(kicker)}</div><h1>{esc(title)}</h1>' +
        f'<div class="vidwrap"><video src="{esc(src)}" poster="{esc(poster)}" controls preload="metadata"></video>' +
        f'<div class="vidcap">{esc(cap)}</div></div>' +
        foot(n, total) + notes(note) + "</section>")

TOTAL = 30
S = []

# 1 封面
S.append(slide_open("maroon") +
    '<div class="cover"><div class="ctext">' +
    '<div class="kicker">聖心堂慕道班・2026年11月1日</div>' +
    '<h1>感恩祭（彌撒）</h1>' +
    '<div class="sub">從逾越節到祭台：盟約、祭獻與共融</div>' +
    "</div>" +
    '<div class="cimg"><img class="zoomable" src="salvador-eucaristico.jpg" data-cap="亞涅茲《聖體救主》（普拉多博物館）"></div></div>' +
    foot(1, TOTAL) + "</section>")

# 2 開場
S.append(content(2, TOTAL, "開場", "今晚的路線",
    ["天主怎樣餵養祂的子民——從逾越節羔羊，經過最後晚餐，到主日的祭台。",
     "盟約 → 逾越節 → 最後晚餐 → 聖經 → 初期教會 → 彌撒 → 領受聖體的意義"],
    "今晚走一條線：天主怎樣餵養祂的子民——從逾越節羔羊，經過最後晚餐，到主日的祭台。"))

# 3 盟約文字
S.append(content(3, TOTAL, "舊約", "天主立盟約——用一頓飯作印記",
    ["整部舊約，天主不斷與人立盟約：亞巴郎（創12、15）、梅瑟（出19–24）。",
     "每個盟約形狀都一樣：天主召叫 → 許下承諾 → 人答應 → 以祭獻作印記。",
     "印記幾乎都是一頓共餐——一起吃飯，成為一家人。"],
    "天主不只給誡命，祂建立一個家庭；家庭是一起吃飯的。今晚就跟著這條「盟約之餐」的線走。"))

# 4 麥基洗德
S.append(art(4, TOTAL, "舊約", "rubens-melchizedek.jpg",
    "魯本斯《亞巴郎與麥基洗德相遇》", "麥基洗德獻上餅和酒（創14）——聖體聖事的預像",
    "麥基洗德是至高天主的司祭，他獻上的餅和酒，教會從起初就認出是聖體的預像。"))

# 5 逾越節
S.append(content(5, TOTAL, "舊約", "逾越節：出谷紀第十二章",
    [[("羔羊：", True, False), ("一歲、雄性、無殘疾", False, False)],
     [("血：", True, False), ("塗在門框和門楣上", False, False)],
     [("吃：", True, False), ("烤著吃，配無酵餅和苦菜——束腰、穿鞋、手持棍杖，急速吃", False, False)]],
    "天主親自規定每個細節，因為細節都在教導。無殘疾的羔羊——完美；木頭上的血——得救的記號；無酵餅——匆忙、除舊；苦菜——為奴之苦；旅人的姿態——天主要帶他們去一個地方。"))

# 6 紀念日
S.append(quote(6, TOTAL, "舊約", "「這是紀念日」",
    "這血在你們所住的房屋上，當作你們的記號：我打擊埃及國的時候，一見這血，就越過你們去，毀滅的災禍不落在你們身上。這一天將是你們的紀念日，要當作上主的節日來慶祝；你們要世世代代過這節日，作為永遠的法規。",
    "出 12:13–14",
    "兩個重點。得救靠的是血，不是人的好。「紀念」不是懷舊：禮儀使天主的救援臨於每一代。注意天主把孩子的問題寫進禮儀裡——「這禮有什麼意思？」（出12:26–27）禮儀本身就是要理講授，教會至今如此。"))

# 7 最後晚餐文字
S.append(content(7, TOTAL, "新約", "最後晚餐：一頓逾越節晚餐",
    ["「你願我們在哪裡，給你預備吃逾越節晚餐？」——門徒去預備了。",
     "晚上，祂與十二門徒坐席。",
     "在逾越節晚餐中，新的事發生了：拿餅、祝福、擘開——還有杯。"],
    "關鍵：耶穌沒有廢除逾越節，祂慶祝它，並在其中建立新的禮。「新約的血」呼應出24:8梅瑟灑血立約。西乃山的形狀重現——這次以祂自己的血作印記，在前一夜預先獻上。"))

# 8 丁托列托
S.append(art(8, TOTAL, "新約", "tintoretto-last-supper.jpg",
    "丁托列托《最後晚餐》(1594)", "基督在畫面中央分餅，光照全場",
    "關鍵：耶穌沒有廢除逾越節，祂慶祝它，並在其中建立新的禮。", flip=True))

# 9 瑪26
S.append(quote(9, TOTAL, "新約", "「這是我的身體……這是我的血」",
    "他們正吃晚餐的時候，耶穌拿起餅來，祝福了，擘開遞給門徒說：「你們拿去吃罷！這是我的身體。」然後，又拿起杯來，祝謝了，遞給他們說：「你們都由其中喝罷！因為這是我的血，新約的血，為大眾傾流，以赦免罪過。我告訴你們：從今以後，我不再喝這葡萄汁了，直到在我父的國裏那一天，與你們同喝新酒。」",
    "瑪 26:26–29・另見谷14・路22・格前11",
    "新約中重複最多的話。「紀念」就是逾越節的紀念——禮儀使祭獻臨在，不只是回想。所以彌撒是祭獻，不是追思會。29節別錯過：「在我父的國裏……與你們同喝新酒」——指向天國的婚宴：聖體是未來的預嘗。"))

# 10 若6:48-58
S.append(content(10, TOTAL, "聖經", "「我的肉是真實的食品」",
    ["48 我是生命的食糧。……51 我是從天上降下的生活的食糧；誰若吃了這食糧，必要生活直到永遠。我所要賜給的食糧，就是我的肉，是為世界的生命而賜給的。",
     "53 「我實實在在告訴你們：你們若不吃人子的肉，不喝他的血，在你們內，便沒有生命。」",
     "55 「因為我的肉，是真實的食品；我的血，是真實的飲料。」",
     "56 「誰吃我的肉，並喝我的血，便住在我內，我也住在他內。」"],
    "這是福音中唯一一次，耶穌因一條教導失去跟隨者，卻不追回去解釋「我是比喻」。祂是認真的。注意55節「真實的食品」；56節「住在我內，我也住在他內」——聖體是雙向的寓居。"))

# 11 若6:66-69
S.append(quote(11, TOTAL, "聖經", "門徒離去，伯多祿留下",
    "從此，他的門徒中有許多人退去了，不再同他往來。於是耶穌向那十二人說：「難道你們也願走嗎？」西滿伯多祿回答說：「主！惟你有永生的話，我們去投奔誰呢？我們相信，而且已知道你是天主的聖者。」",
    "若 6:66–69",
    "伯多祿的回答就是教會至今的回答：即使難懂，我們留下。"))

# 12 宗2
S.append(content(12, TOTAL, "聖經", "初期教會：「擘餅」",
    ["「他們專心聽取宗徒的訓誨，時常團聚，擘餅，祈禱。」——宗2:42",
     "「每天都成群結隊地前往聖殿，也挨戶擘餅，懷著歡樂和誠實的心一起進食。」——宗2:46",
     "「上主天天使那些得救的人加入會眾。」——宗2:47"],
    "聖體聖事不是後來的發明，是教會的第一口呼吸。注意次序：先有擘餅，才有「上主使人加入」。聖體建立教會，教會才去傳教。"))

# 13 厄瑪烏文字
S.append(content(13, TOTAL, "聖經", "厄瑪烏：在餐桌上被認出",
    ["路上祂講解聖經——「我們的心不是火熱的嗎？」",
     "「當耶穌與他們坐下吃飯的時候，就拿起餅來，祝福了，擘開，遞給他們。他們的眼睛開了，這纔認出耶穌來。」——路24:30–31"],
    "聖經預備心，聖事賜下相遇。心在聽道時火熱，眼睛卻在擘餅時開。記住這個形狀——就是每台彌撒的形狀。"))

# 14 林布蘭厄瑪烏
S.append(art(14, TOTAL, "聖經", "rembrandt-emmaus.jpg",
    "林布蘭《厄瑪烏的晚餐》(1648)", "燭光下耶穌擘餅，門徒驚悟",
    "聖經預備心，聖事賜下相遇。心在聽道時火熱，眼睛卻在擘餅時開。", flip=True))

# 15 影片
S.append(video(15, TOTAL, "聖經", "厄瑪烏", "emmaus-combined.mp4", "emmaus-poster.jpg",
    "23秒：林布蘭畫作開場 → 路上同行（路24:32）→ 擘餅認出（路24:30–31）",
    "播放影片。聖經預備心，聖事賜下相遇——這就是每台彌撒的形狀。"))

# 16 初期基督徒
S.append(content(16, TOTAL, "初期教會", "初期基督徒相信什麼",
    ["《十二宗徒遺訓》（一／二世紀）：「在主日聚會，擘餅、獻感恩祭……」",
     "安提約基雅的聖依納爵（†107）：聖體是「不朽之藥」，「使我們脫免死亡，在耶穌基督內永生」。",
     "殉道者聖猶思定（約155年）向外教皇帝描述的主日聚會：讀經、講道、祈禱、餅酒、眾人應「阿們」、分送——並由執事送給缺席者。"],
    "都在宗徒去世一代人之內。猶思定向外教皇帝描述的程序，我們都認得。要理說：這基本輪廓「直到今天，仍完好地為各大禮儀族群所保存」（CCC 1345）。"))

# 17 兩張桌子
S.append(content(17, TOTAL, "彌撒", "今天的彌撒：兩張桌子，一個敬禮",
    ["感恩祭禮儀有兩大部分，形成一個整體（CCC 1346）：",
     [("聖道禮儀", True, False), ("——天主聖言的桌子", False, False)],
     [("聖祭禮儀", True, False), ("——主基督身體的桌子", False, False)],
     "「為我們擺設的感恩祭宴席，是天主聖言和主基督身體的雙重桌子。」",
     "正是厄瑪烏的形狀：路上講解聖經，同席時「拿起餅來，祝謝了，擘開，遞給他們」（參 CCC 1347）。"],
    "回答「彌撒為什麼長這樣」——因為厄瑪烏長這樣。兩張桌子，一頓飯，一個敬禮。"))

# 18 走一遍彌撒
S.append(content(18, TOTAL, "彌撒", "走一遍彌撒",
    [[("1. 進堂禮", True, False), ("——集合：問候、懺悔禮、光榮頌，成為一個團體", False, False)],
     [("2. 聖道禮儀", True, False), ("——讀經、聖詠、福音、講道、信經、信友禱文；天主說話，我們回應", False, False)],
     [("3. 聖祭禮儀", True, False), ("——奉獻餅酒、感恩經與祝聖、天主經、羔羊頌、領聖體；天上觸及人間", False, False)],
     [("4. 禮成禮", True, False), ("——降福與遣散：「彌撒禮成，你們去吧。」被派遣", False, False)]],
    "慢慢走——多數慕道者望過彌撒，卻沒人為他們講解過。落在關鍵：感恩經之前都是預備，之後都是感恩與使命。遣散不是結束，是派遣。"))

# 19 聖瑪竇
S.append(art(19, TOTAL, "彌撒", "guido-matthew.jpg",
    "圭多・雷尼《聖瑪竇與天使》", "天使引著聖史的手寫福音——天主說話的樣子",
    "聖道禮儀：讀經、聖詠、福音、講道——天主說話，我們回應。"))

# 20 波佐
S.append(art(20, TOTAL, "彌撒", "triumph-of-st-ignatius.jpg",
    "波佐《聖依納爵的勝利》（羅馬聖依納爵堂穹頂，1694）",
    "抬頭仰望，藍天之上基督在光中，聖人天使層層環繞——正是「天上觸及人間」的樣子",
    "聖祭禮儀：奉獻餅酒、感恩經與祝聖、天主經、羔羊頌、領聖體——天上觸及人間。", flip=True))

# 21 神秘羔羊
S.append(art(21, TOTAL, "彌撒", "eyck-mystic-lamb.jpg",
    "揚・范艾克《神祕羔羊的欽崇》（根特祭壇畫，1432）",
    "祭台上的羔羊，血流入聖爵，聖人環繞欽崇——「天主的羔羊」",
    "羔羊頌：「除免世罪的天主羔羊，求祢垂憐我們。」——逾越節的羔羊，如今在祭台上。"))

# 22 真實臨在
S.append(content(22, TOTAL, "教會的教導", "基督真實臨在——簡單說",
    ["祝聖之後，餅酒真正成為耶穌——祂的體和血。",
     "不是象徵，不是紀念：是真真實實的祂。",
     "教會稱這轉變為「實體轉變」（CCC 1376）：餅酒的外形仍在，但其實體已成為基督。",
     "「藉著餅與酒的被祝聖，餅的整個實體，被轉變成為我主基督身體的實體；酒的整個實體，被轉變成為祂寶血的實體。」——CCC 1376"],
    "簡單而肯定：因為祂說「這是我的身體」，教會從一開始就相信。一個專有名詞，一句白話解釋——這個階段夠了。"))

# 23 果效
S.append(content(23, TOTAL, "教會的教導", "領聖體在我們內做什麼",
    ["加深與基督的結合。",
     "赦免小罪，堅固我們抵擋將來的大罪。",
     "使我們成為一個身體——「感恩祭建立教會」。",
     "派遣我們走向窮人。"],
    "聖體是食糧：滋養、醫治、結合。兩句要落地：它是罪人的良藥，不是完人的獎品——但正因它是基督，要求我們預備好自己。"))

# 24 預備領受
S.append(content(24, TOTAL, "活出來", "預備領受",
    ["「所以人應省察自己，然後纔可以吃這餅，喝這杯。」——格前11:28",
     "自覺有大罪：先辦告解。",
     "守聖體齋（一小時）。",
     "以迎接貴賓的心來——「因為此刻基督要成為我們的貴賓」（CCC 1387）。"],
    "三個具體習慣：省察良心（週六晚上正是時候）、大罪先告解、守齋。說得溫暖：預備不是門檻，是迎接所愛之人的方式。"))

# 25 浪子回頭
S.append(art(25, TOTAL, "活出來", "rembrandt-prodigal-son.jpg",
    "林布蘭《浪子回頭》(1669)", "父親擁抱跪著的兒子——告解就是回家",
    "預備不是門檻，是迎接所愛之人的方式——告解就是回家。", flip=True))

# 26 從聖體生活
S.append(content(26, TOTAL, "活出來", "從聖體生活",
    ["五個習慣，一週的節奏：",
     [("1. 好好預備", True, False), ("領聖體", False, False)],
     [("2. 探訪", True, False), ("明供的聖體", False, False)],
     [("3. 朝拜聖體", True, False)],
     [("4. 定期告解", True, False)],
     [("5. 讀聖人的傳記", True, False), ("——那些深愛聖體的人", False, False)]],
    "具體化：說出本堂朝拜聖體的時間。建議本週一次十五分鐘的探訪。可以提的聖人：聖女大德蘭、聖維雅納、聖小德蘭、真福卡洛・阿庫蒂斯——「聖體聖事是我通往天堂的高速公路」。"))

# 27 三王來朝
S.append(art(27, TOTAL, "活出來", "monaco-magi.jpg",
    "洛倫佐・摩納哥《三王來朝》(1420)", "賢士俯伏朝拜聖嬰——朝拜的樣子",
    "朝拜聖體：賢士走了遠路，只為俯伏朝拜。這週，找十五分鐘，去探訪祂。"))

# 28 三句話
S.append(slide_open("maroon") +
    '<div class="kicker">帶回家</div><div class="takehome"><h1>帶回家的三句話</h1>' +
    '<div class="item"><div class="num">一</div><div class="txt">聖體聖事是基督寶血所立的新約——逾越節的成全，不是一個象徵。</div></div>' +
    '<div class="item"><div class="num">二</div><div class="txt">教會從宗徒時代就這樣慶祝——主日復主日，不朽之藥。</div></div>' +
    '<div class="item"><div class="num">三</div><div class="txt">基督成為你的貴賓——預備好自己，讓祂使你與祂合而為一。</div></div></div>' +
    foot(28, TOTAL) + notes("慢慢說，說兩遍也可以。這是給停車場的三句話——請大家寫下一句。") + "</section>")

# 29 反省
S.append(content(29, TOTAL, "反省", "反省",
    ["「感恩祭建立教會」——這週我該怎樣對待身邊的人？",
     "聖保祿說「人應省察自己」（格前11:28）——我的週六晚上可以怎樣省察？",
     "這週，哪裡可以安插一次短短的聖體探訪？"],
    "讀出來，靜默兩分鐘——或分組分享。分享要短，最後帶回基督的臨在。"))

# 30 結束
S.append(slide_open("maroon-dk") +
    '<div class="closing"><blockquote>「因為餅只是一個，我們雖多，只是一個身體，因為我們眾人都共享這一個餅。」</blockquote>' +
    '<div class="src">——格前 10:17</div>' +
    '<div class="thanks">謝謝大家</div>' +
    '<div class="srcline">資料：思高聖經・《天主教要理》・教父</div></div>' +
    foot(30, TOTAL) + notes("以祈禱結束——「基督的靈魂」禱文，或簡單的謝恩。") + "</section>")

assert len(S) == TOTAL, f"slide count {len(S)} != {TOTAL}"

BODY = "\n".join(S)
HTML = f"""<!DOCTYPE html>
<html lang="zh-Hant">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>感恩祭（彌撒）・聖心堂慕道班</title>
<style>{CSS}</style>
</head>
<body>
<div id="viewport"><div id="stage">
{BODY}
</div></div>
<div id="lightbox"><img id="lbimg" alt=""><div class="lbcap" id="lbcap"></div></div>
<div id="hint">← → 翻頁・F 全螢幕・N 講稿・點畫放大</div>
<div id="counter"></div>
<script>{JS}</script>
</body>
</html>
"""
with open(OUT, "w", encoding="utf-8") as f:
    f.write(HTML)
print("saved:", OUT, os.path.getsize(OUT), "bytes")
