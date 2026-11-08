from pathlib import Path
p = Path("RanobeSaver/app/src/main/java/app/ranobe/MainActivity.kt")
s = p.read_text(encoding="utf-8")

old = """var head=(document.title||'')+' '+(document.body?(document.body.innerText||'').slice(0,300):'');
var bodyLen=document.body?T(document.body).length:0;
if(/just a moment|verify you are human|are you human|captcha|checking your browser|attention required|не робот|проверка безопасности/i.test(head)||(document.querySelector('#challenge-form,#cf-challenge-running,.cf-turnstile,.g-recaptcha,.h-captcha,iframe[src*="captcha"],iframe[src*="challenges.cloudflare"]')&&bodyLen<600))return JSON.stringify({captcha:true});"""
new = """var head=(document.title||'')+' '+(document.body?(document.body.innerText||'').slice(0,3000):'');
var capText=/just a moment|verify you are human|are you human|complete the (security )?check|checking your browser|attention required|human verification|security verification|captcha challenge|не робот|проверка безопасности/i.test(head);
var capNodes=document.querySelectorAll('#challenge-form,#cf-challenge-running,.cf-turnstile,.g-recaptcha,.h-captcha,[class*="captcha"],[id*="captcha"],iframe[src*="captcha"],iframe[src*="turnstile"],iframe[src*="challenges.cloudflare"]');
var capVisible=false;
for(var ci=0;ci<capNodes.length;ci++){var ce=capNodes[ci],cr=ce.getBoundingClientRect(),cs=getComputedStyle(ce);if(cr.width>0&&cr.height>0&&cs.display!=='none'&&cs.visibility!=='hidden'&&Number(cs.opacity||1)>0.05){capVisible=true;break}}
if(capText||capVisible)return JSON.stringify({captcha:true});"""
assert old in s
s=s.replace(old,new)

s=s.replace("    private lateinit var statusB: TextView\n", "    private lateinit var statusB: TextView\n    private lateinit var pauseB: Button\n")
old='''        c.addView(row(btn("◀", false) { if (web.canGoBack()) web.goBack() }, btn("Продолжить") { resume() },
            btn("Эта страница → ссылка", false) { urlE.setText(web.url ?: ""); showTab(0) }))'''
new='''        pauseB = btn("Ⅱ Пауза", false) { togglePause() }
        c.addView(row(btn("◀", false) { if (web.canGoBack()) web.goBack() }, pauseB, btn("Продолжить") { resume() },
            btn("Эта страница → ссылка", false) { urlE.setText(web.url ?: ""); showTab(0) }))'''
assert old in s
s=s.replace(old,new)
s=s.replace("                if (running && !waiting) { gen++; lastLen = -1; val t = gen; h.postDelayed({ poll(t, 0) }, 800) }",
            "                if (running && !waiting && !paused) { gen++; lastLen = -1; val t = gen; h.postDelayed({ poll(t, 0) }, 800) }")
s=s.replace("        running = true; paused = false\n        window.addFlags", "        running = true; paused = false; pauseB.text = \"Ⅱ Пауза\"\n        window.addFlags")
s=s.replace("        running = false; paused = false; waiting = false; gen++", "        running = false; paused = false; waiting = false; gen++\n        if (::pauseB.isInitialized) pauseB.text = \"Ⅱ Пауза\"")
old='''    private fun resume() {
        if (!running || !paused) { toast("Продолжать нечего"); return }
        paused = false; waiting = false; gen++; lastLen = -1; val t = gen
        setStatus("Продолжаю…"); poll(t, 0)
    }'''
new='''    private fun togglePause() {
        if (!running) { toast("Сначала начните копирование"); return }
        if (paused) { resume(); return }
        paused = true; gen++
        pauseB.text = "▶ На паузе"
        setStatus("⏸ Копирование приостановлено. Страница сохранена; нажмите «Продолжить», когда будете готовы.")
    }
    private fun resume() {
        if (!running || !paused) { toast("Продолжать нечего"); return }
        paused = false; waiting = false; gen++; lastLen = -1; val t = gen
        pauseB.text = "Ⅱ Пауза"
        setStatus("Продолжаю…"); poll(t, 0)
    }'''
assert old in s
s=s.replace(old,new)
s=s.replace("        if (t != gen || !running) return\n        web.evaluateJavascript", "        if (t != gen || !running || paused) return\n        web.evaluateJavascript")
old='''                o != null && o.optBoolean("captcha") -> {
                    if (!paused) { paused = true; showTab(1) }
                    setStatus("Нужна проверка «я не робот». Пройдите её в этом окне — копирование продолжится само (или нажмите «Продолжить»).")
                    h.postDelayed({ poll(t, 0) }, 3000)
                }'''
new='''                o != null && o.optBoolean("captcha") -> {
                    if (!paused) { paused = true; gen++; pauseB.text = "▶ На паузе"; showTab(1) }
                    setStatus("⏸ Обнаружена капча. Копирование остановлено на этой главе. Пройдите проверку в окне браузера и нажмите «Продолжить». Следующая глава не будет открыта до вашего действия.")
                }'''
assert old in s
s=s.replace(old,new)
s=s.replace("        gen++; waiting = true; paused = false\n", "        gen++; waiting = true; paused = false; pauseB.text = \"Ⅱ Пауза\"\n")
p.write_text(s, encoding="utf-8")
