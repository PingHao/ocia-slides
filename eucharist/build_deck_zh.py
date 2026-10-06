#!/usr/bin/env python3
"""Build the Traditional Chinese 感恩祭（彌撒） OCIA slide deck (Nov 1, 2026)."""
import os
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from PIL import Image

MAROON = RGBColor(0x5E, 0x1A, 0x1E)
MAROON_DK = RGBColor(0x42, 0x10, 0x14)
GOLD = RGBColor(0xC9, 0xA2, 0x27)
GOLD_LT = RGBColor(0xE4, 0xC8, 0x5A)
CREAM = RGBColor(0xFD, 0xFB, 0xF6)
PARCH = RGBColor(0xF6, 0xEF, 0xDD)
INK = RGBColor(0x2B, 0x26, 0x20)
MUTED = RGBColor(0x6B, 0x5D, 0x4F)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)
DARK = RGBColor(0x14, 0x12, 0x10)
FONT = "Microsoft JhengHei"

HERE = os.path.dirname(os.path.abspath(__file__))
def asset(name):
    return os.path.join(HERE, name)

prs = Presentation()
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)
BLANK = prs.slide_layouts[6]
TOTAL = 30

def bg(slide, color):
    fill = slide.background.fill
    fill.solid()
    fill.fore_color.rgb = color

def textbox(slide, l, t, w, h):
    return slide.shapes.add_textbox(Inches(l), Inches(t), Inches(w), Inches(h))

def para(tf, text, size=20, bold=False, italic=False, color=INK,
         align=PP_ALIGN.LEFT, space_after=6, space_before=0, first=False):
    p = tf.paragraphs[0] if first else tf.add_paragraph()
    p.space_after = Pt(space_after)
    p.space_before = Pt(space_before)
    p.alignment = align
    r = p.add_run()
    r.text = text
    r.font.size = Pt(size)
    r.font.bold = bold
    r.font.italic = italic
    r.font.color.rgb = color
    r.font.name = FONT
    return p

def rich(tf, parts, size=20, color=INK, align=PP_ALIGN.LEFT, space_after=10, first=False):
    p = tf.paragraphs[0] if first else tf.add_paragraph()
    p.space_after = Pt(space_after)
    p.alignment = align
    for text, b, i in parts:
        r = p.add_run()
        r.text = text
        r.font.size = Pt(size)
        r.font.bold = b
        r.font.italic = i
        r.font.color.rgb = color
        r.font.name = FONT
    return p

def kicker_box(slide, text, top=0.45):
    tb = textbox(slide, 0.9, top, 11.5, 0.5)
    tf = tb.text_frame
    tf.word_wrap = True
    para(tf, text, size=14, bold=True, color=GOLD, space_after=0, first=True)
    shp = slide.shapes.add_shape(1, Inches(0.9), Inches(top + 0.32), Inches(1.2), Pt(3))
    shp.fill.solid(); shp.fill.fore_color.rgb = GOLD
    shp.line.fill.background()
    return top + 0.55

def title_text(slide, text, top, size=38, color=MAROON):
    tb = textbox(slide, 0.9, top, 11.5, 1.4)
    tf = tb.text_frame
    tf.word_wrap = True
    para(tf, text, size=size, bold=True, color=color, space_after=0, first=True)

def footer(slide, n, dark=False):
    c = GOLD_LT if dark else MUTED
    tb = textbox(slide, 0.9, 6.95, 8, 0.4)
    tf = tb.text_frame; tf.word_wrap = True
    para(tf, "感恩祭（彌撒）・聖心堂慕道班", size=11, color=c, space_after=0, first=True)
    tb2 = textbox(slide, 12.0, 6.95, 0.8, 0.4)
    tf2 = tb2.text_frame; tf2.word_wrap = True
    para(tf2, f"{n} / {TOTAL}", size=11, color=c, align=PP_ALIGN.RIGHT, space_after=0, first=True)

def add_notes(slide, text):
    slide.notes_slide.placeholders[1].text = text

def content_slide(n, kicker, title, bullets, notes, size=21, title_size=38):
    slide = prs.slides.add_slide(BLANK)
    bg(slide, CREAM)
    top = kicker_box(slide, kicker)
    title_text(slide, title, top, size=title_size)
    tb = textbox(slide, 0.9, top + 1.35, 11.5, 4.6)
    tf = tb.text_frame
    tf.word_wrap = True
    first = True
    for b in bullets:
        if isinstance(b, str):
            parts = [(b, False, False)]
        else:
            parts = [x if isinstance(x, tuple) else (x, False, False) for x in b]
        rich(tf, parts, size=size, first=first)
        first = False
    footer(slide, n)
    add_notes(slide, notes)
    return slide

def quote_slide(n, kicker, title, quote, cite, notes, qsize=24):
    slide = prs.slides.add_slide(BLANK)
    bg(slide, PARCH)
    top = kicker_box(slide, kicker)
    title_text(slide, title, top, size=34)
    tb = textbox(slide, 1.3, top + 1.4, 10.7, 3.8)
    tf = tb.text_frame
    tf.word_wrap = True
    para(tf, "「" + quote + "」", size=qsize, italic=True, first=True, space_after=10)
    para(tf, "——" + cite, size=17, color=MUTED, space_after=0)
    footer(slide, n)
    add_notes(slide, notes)
    return slide

def image_slide(n, kicker, img_name, cap_title, cap_text, notes):
    slide = prs.slides.add_slide(BLANK)
    bg(slide, DARK)
    top = kicker_box(slide, kicker)
    # fit image into box, preserve aspect
    path = asset(img_name)
    im = Image.open(path)
    iw, ih = im.size
    bw, bh = 11.9, 4.55
    s = min(bw / iw, bh / ih)
    w, h = iw * s, ih * s
    l = 0.7167 + (bw - w) / 2
    t = top + 0.3 + (bh - h) / 2
    slide.shapes.add_picture(path, Inches(l), Inches(t), Inches(w), Inches(h))
    tb = textbox(slide, 0.9, top + 0.3 + bh + 0.08, 11.5, 0.85)
    tf = tb.text_frame; tf.word_wrap = True
    rich(tf, [(cap_title, True, False)], size=19, color=GOLD, align=PP_ALIGN.CENTER,
         space_after=2, first=True)
    para(tf, cap_text, size=15, color=CREAM, align=PP_ALIGN.CENTER, space_after=0)
    footer(slide, n, dark=True)
    add_notes(slide, notes)
    return slide

def video_slide(n, kicker, title, video_name, poster_name, cap, notes):
    slide = prs.slides.add_slide(BLANK)
    bg(slide, DARK)
    top = kicker_box(slide, kicker)
    title_text(slide, title, top, size=30, color=WHITE)
    vw, vh = 10.6, 5.96  # 16:9
    l = (13.333 - vw) / 2
    t = top + 1.15
    slide.shapes.add_movie(asset(video_name), Inches(l), Inches(t), Inches(vw), Inches(vh),
                           poster_frame_image=asset(poster_name), mime_type="video/mp4")
    tb = textbox(slide, 0.9, t + vh + 0.1, 11.5, 0.6)
    tf = tb.text_frame; tf.word_wrap = True
    para(tf, cap, size=15, color=GOLD_LT, align=PP_ALIGN.CENTER, space_after=0, first=True)
    footer(slide, n, dark=True)
    add_notes(slide, notes)
    return slide

# ============================================================ 1 封面
slide = prs.slides.add_slide(BLANK)
bg(slide, MAROON)
shp = slide.shapes.add_shape(1, Inches(0.9), Inches(1.5), Inches(2.0), Pt(4))
shp.fill.solid(); shp.fill.fore_color.rgb = GOLD; shp.line.fill.background()
tb = textbox(slide, 0.9, 1.9, 11.5, 2.2)
tf = tb.text_frame; tf.word_wrap = True
para(tf, "感恩祭（彌撒）", size=64, bold=True, color=WHITE, space_after=6, first=True)
para(tf, "從逾越節到祭台：盟約、祭獻與共融", size=22, italic=True, color=GOLD_LT, space_after=0)
tb = textbox(slide, 0.9, 5.0, 11.5, 1.6)
tf = tb.text_frame; tf.word_wrap = True
para(tf, "聖心堂慕道班・2026年11月1日", size=20, color=WHITE, space_after=4, first=True)
add_notes(slide, "歡迎。今晚走一條線：天主怎樣餵養祂的子民——從逾越節羔羊，經過最後晚餐，到主日的祭台。路線：盟約 → 逾越節 → 最後晚餐 → 聖經 → 初期教會 → 彌撒 → 領受聖體的意義。")

# ============================================================ 2 開場
content_slide(2, "開場", "今晚的路線",
    ["天主怎樣餵養祂的子民——從逾越節羔羊，經過最後晚餐，到主日的祭台。",
     "盟約 → 逾越節 → 最後晚餐 → 聖經 → 初期教會 → 彌撒 → 領受聖體的意義"],
    "今晚走一條線：天主怎樣餵養祂的子民——從逾越節羔羊，經過最後晚餐，到主日的祭台。")

# ============================================================ 3 盟約（文字）
content_slide(3, "舊約", "天主立盟約——用一頓飯作印記",
    ["整部舊約，天主不斷與人立盟約：亞巴郎（創12、15）、梅瑟（出19–24）。",
     "每個盟約形狀都一樣：天主召叫 → 許下承諾 → 人答應 → 以祭獻作印記。",
     "印記幾乎都是一頓共餐——一起吃飯，成為一家人。"],
    "天主不只給誡命，祂建立一個家庭；家庭是一起吃飯的。今晚就跟著這條「盟約之餐」的線走。")

# ============================================================ 4 盟約（麥基洗德）
image_slide(4, "舊約", "rubens-melchizedek.jpg",
    "魯本斯《亞巴郎與麥基洗德相遇》",
    "麥基洗德獻上餅和酒（創14）——聖體聖事的預像",
    "天主不只給誡命，祂建立一個家庭；家庭是一起吃飯的。麥基洗德是至高天主的司祭，他獻上的餅和酒，教會從起初就認出是聖體的預像。")

# ============================================================ 5 逾越節
content_slide(5, "舊約", "逾越節：出谷紀第十二章",
    [[("羔羊：", True, False), ("一歲、雄性、無殘疾", False, False)],
     [("血：", True, False), ("塗在門框和門楣上", False, False)],
     [("吃：", True, False), ("烤著吃，配無酵餅和苦菜——束腰、穿鞋、手持棍杖，急速吃", False, False)]],
    "天主親自規定每個細節，因為細節都在教導。無殘疾的羔羊——完美；木頭上的血——得救的記號；無酵餅——匆忙、除舊；苦菜——為奴之苦；旅人的姿態——天主要帶他們去一個地方。")

# ============================================================ 6 「這是紀念日」
quote_slide(6, "舊約", "「這是紀念日」",
    "這血在你們所住的房屋上，當作你們的記號：我打擊埃及國的時候，一見這血，就越過你們去，毀滅的災禍不落在你們身上。這一天將是你們的紀念日，要當作上主的節日來慶祝；你們要世世代代過這節日，作為永遠的法規。",
    "出 12:13–14",
    "兩個重點。得救靠的是血，不是人的好。「紀念」不是懷舊：禮儀使天主的救援臨於每一代。注意天主把孩子的問題寫進禮儀裡——「這禮有什麼意思？」（出12:26–27）禮儀本身就是要理講授，教會至今如此。", qsize=22)

# ============================================================ 7 最後晚餐（文字）
content_slide(7, "新約", "最後晚餐：一頓逾越節晚餐",
    ["「你願我們在哪裡，給你預備吃逾越節晚餐？」——門徒去預備了。",
     "晚上，祂與十二門徒坐席。",
     "在逾越節晚餐中，新的事發生了：拿餅、祝福、擘開——還有杯。"],
    "關鍵：耶穌沒有廢除逾越節，祂慶祝它，並在其中建立新的禮。「新約的血」呼應出24:8梅瑟灑血立約。西乃山的形狀重現——這次以祂自己的血作印記，在前一夜預先獻上。")

# ============================================================ 8 最後晚餐（丁托列托）
image_slide(8, "新約", "tintoretto-last-supper.jpg",
    "丁托列托《最後晚餐》(1594)",
    "基督在畫面中央分餅，光照全場",
    "關鍵：耶穌沒有廢除逾越節，祂慶祝它，並在其中建立新的禮。「新約的血」呼應出24:8梅瑟灑血立約。")

# ============================================================ 9 建立聖事（瑪26）
quote_slide(9, "新約", "「這是我的身體……這是我的血」",
    "他們正吃晚餐的時候，耶穌拿起餅來，祝福了，擘開遞給門徒說：「你們拿去吃罷！這是我的身體。」然後，又拿起杯來，祝謝了，遞給他們說：「你們都由其中喝罷！因為這是我的血，新約的血，為大眾傾流，以赦免罪過。我告訴你們：從今以後，我不再喝這葡萄汁了，直到在我父的國裏那一天，與你們同喝新酒。」",
    "瑪 26:26–29・另見谷14・路22・格前11",
    "新約中重複最多的話。「紀念」就是逾越節的紀念——禮儀使祭獻臨在，不只是回想。所以彌撒是祭獻，不是追思會。29節別錯過：「在我父的國裏……與你們同喝新酒」——指向天國的婚宴：聖體是未來的預嘗。", qsize=20)

# ============================================================ 10 若6:48-58
content_slide(10, "聖經", "「我的肉是真實的食品」",
    ["48 我是生命的食糧。……51 我是從天上降下的生活的食糧；誰若吃了這食糧，必要生活直到永遠。我所要賜給的食糧，就是我的肉，是為世界的生命而賜給的。",
     "53 「我實實在在告訴你們：你們若不吃人子的肉，不喝他的血，在你們內，便沒有生命。」",
     "55 「因為我的肉，是真實的食品；我的血，是真實的飲料。」",
     "56 「誰吃我的肉，並喝我的血，便住在我內，我也住在他內。」"],
    "這是福音中唯一一次，耶穌因一條教導失去跟隨者，卻不追回去解釋「我是比喻」。祂是認真的。注意55節「真實的食品」——這段的標題就從這裡來；56節「住在我內，我也住在他內」——聖體是雙向的寓居。", size=19)

# ============================================================ 11 若6:66-69
quote_slide(11, "聖經", "門徒離去，伯多祿留下",
    "從此，他的門徒中有許多人退去了，不再同他往來。於是耶穌向那十二人說：「難道你們也願走嗎？」西滿伯多祿回答說：「主！惟你有永生的話，我們去投奔誰呢？我們相信，而且已知道你是天主的聖者。」",
    "若 6:66–69",
    "伯多祿的回答就是教會至今的回答：即使難懂，我們留下。", qsize=22)

# ============================================================ 12 宗2 擘餅
content_slide(12, "聖經", "初期教會：「擘餅」",
    ["「他們專心聽取宗徒的訓誨，時常團聚，擘餅，祈禱。」——宗2:42",
     "「每天都成群結隊地前往聖殿，也挨戶擘餅，懷著歡樂和誠實的心一起進食。」——宗2:46",
     "「上主天天使那些得救的人加入會眾。」——宗2:47"],
    "聖體聖事不是後來的發明，是教會的第一口呼吸。注意次序：先有擘餅，才有「上主使人加入」。聖體建立教會，教會才去傳教。")

# ============================================================ 13 厄瑪烏（文字）
content_slide(13, "聖經", "厄瑪烏：在餐桌上被認出",
    ["路上祂講解聖經——「我們的心不是火熱的嗎？」",
     "「當耶穌與他們坐下吃飯的時候，就拿起餅來，祝福了，擘開，遞給他們。他們的眼睛開了，這纔認出耶穌來。」——路24:30–31"],
    "聖經預備心，聖事賜下相遇。心在聽道時火熱，眼睛卻在擘餅時開。記住這個形狀——就是每台彌撒的形狀。")

# ============================================================ 14 厄瑪烏（林布蘭）
image_slide(14, "聖經", "rembrandt-emmaus.jpg",
    "林布蘭《厄瑪烏的晚餐》(1648)",
    "燭光下耶穌擘餅，門徒驚悟",
    "聖經預備心，聖事賜下相遇。心在聽道時火熱，眼睛卻在擘餅時開。記住這個形狀——就是每台彌撒的形狀。")

# ============================================================ 15 厄瑪烏（影片）
video_slide(15, "聖經", "厄瑪烏",
    "emmaus-combined.mp4", "/tmp/emmaus_poster.jpg",
    "23秒：林布蘭畫作開場 → 路上同行（路24:32）→ 擘餅認出（路24:30–31）",
    "播放影片。聖經預備心，聖事賜下相遇——這就是每台彌撒的形狀。")

# ============================================================ 16 初期基督徒
content_slide(16, "初期教會", "初期基督徒相信什麼",
    ["《十二宗徒遺訓》（一／二世紀）：「在主日聚會，擘餅、獻感恩祭……」",
     "安提約基雅的聖依納爵（†107）：聖體是「不朽之藥」，「使我們脫免死亡，在耶穌基督內永生」。",
     "殉道者聖猶思定（約155年）向外教皇帝描述的主日聚會：讀經、講道、祈禱、餅酒、眾人應「阿們」、分送——並由執事送給缺席者。"],
    "都在宗徒去世一代人之內。猶思定向外教皇帝描述的程序，我們都認得。要理說：這基本輪廓「直到今天，仍完好地為各大禮儀族群所保存」（CCC 1345）。", size=19)

# ============================================================ 17 兩張桌子
content_slide(17, "彌撒", "今天的彌撒：兩張桌子，一個敬禮",
    ["感恩祭禮儀有兩大部分，形成一個整體（CCC 1346）：",
     [("聖道禮儀", True, False), ("——天主聖言的桌子", False, False)],
     [("聖祭禮儀", True, False), ("——主基督身體的桌子", False, False)],
     "「為我們擺設的感恩祭宴席，是天主聖言和主基督身體的雙重桌子。」",
     "正是厄瑪烏的形狀：路上講解聖經，同席時「拿起餅來，祝謝了，擘開，遞給他們」（參 CCC 1347）。"],
    "回答「彌撒為什麼長這樣」——因為厄瑪烏長這樣。兩張桌子，一頓飯，一個敬禮。")

# ============================================================ 18 走一遍彌撒（文字）
content_slide(18, "彌撒", "走一遍彌撒",
    [[("1. 進堂禮", True, False), ("——集合：問候、懺悔禮、光榮頌，成為一個團體", False, False)],
     [("2. 聖道禮儀", True, False), ("——讀經、聖詠、福音、講道、信經、信友禱文；天主說話，我們回應", False, False)],
     [("3. 聖祭禮儀", True, False), ("——奉獻餅酒、感恩經與祝聖、天主經、羔羊頌、領聖體；天上觸及人間", False, False)],
     [("4. 禮成禮", True, False), ("——降福與遣散：「彌撒禮成，你們去吧。」被派遣", False, False)]],
    "慢慢走——多數慕道者望過彌撒，卻沒人為他們講解過。落在關鍵：感恩經之前都是預備，之後都是感恩與使命。遣散不是結束，是派遣。", size=19)

# ============================================================ 19 聖道禮儀（聖瑪竇）
image_slide(19, "彌撒", "guido-matthew.jpg",
    "圭多・雷尼《聖瑪竇與天使》",
    "天使引著聖史的手寫福音——天主說話的樣子",
    "聖道禮儀：讀經、聖詠、福音、講道——天主說話，我們回應。")

# ============================================================ 20 聖祭禮儀（波佐）
image_slide(20, "彌撒", "triumph-of-st-ignatius.jpg",
    "波佐《聖依納爵的勝利》（羅馬聖依納爵堂穹頂，1694）",
    "抬頭仰望，藍天之上基督在光中，聖人天使層層環繞——正是「天上觸及人間」的樣子",
    "聖祭禮儀：奉獻餅酒、感恩經與祝聖、天主經、羔羊頌、領聖體——天上觸及人間。")

# ============================================================ 21 羔羊頌（范艾克）
image_slide(21, "彌撒", "eyck-mystic-lamb.jpg",
    "揚・范艾克《神祕羔羊的欽崇》（根特祭壇畫，1432）",
    "祭台上的羔羊，血流入聖爵，聖人環繞欽崇——「天主的羔羊」",
    "羔羊頌：「除免世罪的天主羔羊，求祢垂憐我們。」——逾越節的羔羊，如今在祭台上。")

# ============================================================ 22 真實臨在
content_slide(22, "教會的教導", "基督真實臨在——簡單說",
    ["祝聖之後，餅酒真正成為耶穌——祂的體和血。",
     "不是象徵，不是紀念：是真真實實的祂。",
     "教會稱這轉變為「實體轉變」（CCC 1376）：餅酒的外形仍在，但其實體已成為基督。",
     "「藉著餅與酒的被祝聖，餅的整個實體，被轉變成為我主基督身體的實體；酒的整個實體，被轉變成為祂寶血的實體。」——CCC 1376"],
    "簡單而肯定：因為祂說「這是我的身體」，教會從一開始就相信。一個專有名詞，一句白話解釋——這個階段夠了。有人追問哲學，以後再談。", size=19)

# ============================================================ 23 領聖體的果效
content_slide(23, "教會的教導", "領聖體在我們內做什麼",
    ["加深與基督的結合。",
     "赦免小罪，堅固我們抵擋將來的大罪。",
     "使我們成為一個身體——「感恩祭建立教會」。",
     "派遣我們走向窮人。"],
    "聖體是食糧：滋養、醫治、結合。兩句要落地：它是罪人的良藥，不是完人的獎品——但正因它是基督，要求我們預備好自己。")

# ============================================================ 24 預備領受（文字）
content_slide(24, "活出來", "預備領受",
    ["「所以人應省察自己，然後纔可以吃這餅，喝這杯。」——格前11:28",
     "自覺有大罪：先辦告解。",
     "守聖體齋（一小時）。",
     "以迎接貴賓的心來——「因為此刻基督要成為我們的貴賓」（CCC 1387）。"],
    "三個具體習慣：省察良心（週六晚上正是時候）、大罪先告解、守齋。說得溫暖：預備不是門檻，是迎接所愛之人的方式。")

# ============================================================ 25 預備領受（浪子回頭）
image_slide(25, "活出來", "rembrandt-prodigal-son.jpg",
    "林布蘭《浪子回頭》(1669)",
    "父親擁抱跪著的兒子——告解就是回家",
    "三個具體習慣：省察良心、大罪先告解、守齋。預備不是門檻，是迎接所愛之人的方式——告解就是回家。")

# ============================================================ 26 從聖體生活（文字）
content_slide(26, "活出來", "從聖體生活",
    ["五個習慣，一週的節奏：",
     [("1. ", True, False), ("好好預備", True, False), ("領聖體", False, False)],
     [("2. ", True, False), ("探訪", True, False), ("明供的聖體", False, False)],
     [("3. ", True, False), ("朝拜聖體", True, False)],
     [("4. ", True, False), ("定期告解", True, False)],
     [("5. ", True, False), ("讀聖人的傳記", True, False), ("——那些深愛聖體的人", False, False)]],
    "具體化：說出本堂朝拜聖體的時間。建議本週一次十五分鐘的探訪。可以提的聖人：聖女大德蘭、聖維雅納、聖小德蘭、真福卡洛・阿庫蒂斯——「聖體聖事是我通往天堂的高速公路」。")

# ============================================================ 27 從聖體生活（三王來朝）
image_slide(27, "活出來", "monaco-magi.jpg",
    "洛倫佐・摩納哥《三王來朝》(1420)",
    "賢士俯伏朝拜聖嬰——朝拜的樣子",
    "朝拜聖體：賢士走了遠路，只為俯伏朝拜。這週，找十五分鐘，去探訪祂。")

# ============================================================ 28 三句話
slide = prs.slides.add_slide(BLANK)
bg(slide, MAROON)
kicker_box(slide, "帶回家")
title_text(slide, "帶回家的三句話", 1.0, size=40, color=WHITE)
items = [
    ("一  ", "聖體聖事是基督寶血所立的新約——逾越節的成全，不是一個象徵。"),
    ("二  ", "教會從宗徒時代就這樣慶祝——主日復主日，不朽之藥。"),
    ("三  ", "基督成為你的貴賓——預備好自己，讓祂使你與祂合而為一。"),
]
tb = textbox(slide, 0.9, 2.4, 11.5, 4.2)
tf = tb.text_frame; tf.word_wrap = True
for j, (num, txt) in enumerate(items):
    p = tf.paragraphs[0] if j == 0 else tf.add_paragraph()
    p.space_after = Pt(18)
    r = p.add_run(); r.text = num
    r.font.size = Pt(30); r.font.bold = True; r.font.color.rgb = GOLD; r.font.name = FONT
    r2 = p.add_run(); r2.text = txt
    r2.font.size = Pt(23); r2.font.color.rgb = WHITE; r2.font.name = FONT
footer(slide, 28, dark=True)
add_notes(slide, "慢慢說，說兩遍也可以。這是給停車場的三句話——請大家寫下一句。")

# ============================================================ 29 反省
content_slide(29, "反省", "反省",
    ["「感恩祭建立教會」——這週我該怎樣對待身邊的人？",
     "聖保祿說「人應省察自己」（格前11:28）——我的週六晚上可以怎樣省察？",
     "這週，哪裡可以安插一次短短的聖體探訪？"],
    "讀出來，靜默兩分鐘——或分組分享。分享要短，最後帶回基督的臨在。")

# ============================================================ 30 結束
slide = prs.slides.add_slide(BLANK)
bg(slide, MAROON_DK)
tb = textbox(slide, 1.3, 1.6, 10.7, 2.6)
tf = tb.text_frame; tf.word_wrap = True
para(tf, "「因為餅只是一個，我們雖多，只是一個身體，因為我們眾人都共享這一個餅。」",
     size=28, italic=True, color=WHITE, align=PP_ALIGN.CENTER, space_after=10, first=True)
para(tf, "——格前 10:17", size=18, color=GOLD_LT, align=PP_ALIGN.CENTER, space_after=30)
para(tf, "謝謝大家", size=36, bold=True, color=WHITE, align=PP_ALIGN.CENTER, space_after=12)
para(tf, "資料：思高聖經・《天主教要理》・教父",
     size=12, color=GOLD_LT, align=PP_ALIGN.CENTER, space_after=0)
footer(slide, 30, dark=True)
add_notes(slide, "以祈禱結束——「基督的靈魂」禱文，或簡單的謝恩。")

out = asset("感恩祭彌撒-慕道班.pptx")
prs.save(out)
print("saved:", out, os.path.getsize(out), "bytes")
print("slides:", len(prs.slides.__iter__.__self__._sldIdLst))
