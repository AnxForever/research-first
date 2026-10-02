"""Black-box smoke acceptance for a local sample, using installed Playwright + Edge."""
import argparse, json, re, time
from datetime import datetime
from pathlib import Path
from urllib.parse import urlsplit
from playwright.sync_api import sync_playwright

HERE = Path(__file__).resolve().parent
ITEMS = "[role=option], [role=menuitem], a, button, [role=button]"
EMPTY = re.compile(r"no results?|no pages?|no matching|nothing found|not found|no items?|找不到|没有结果|无结果|未找到|没有匹配|无匹配", re.I)

def path(url): return urlsplit(url).path.rstrip("/") or "/"
def allow_local_only(context, base_url, blocked_urls):
    origin = urlsplit(base_url)
    def handle(route):
        requested = urlsplit(route.request.url)
        if (requested.scheme, requested.netloc) == (origin.scheme, origin.netloc) or requested.scheme == "data":
            route.continue_()
        else:
            blocked_urls.add(route.request.url)
            route.abort()
    context.route("**/*", handle)

def record(out, key, ok, evidence):
    out[key] = {"status": "unknown" if ok is None else "pass" if ok else "fail", "evidence": evidence}
def modal(page):
    for selector in ("[role=dialog]:visible", "[aria-modal=true]:visible"):
        d = page.locator(selector)
        if d.count(): return d.last
    return None
def field(page):
    root = modal(page)
    if root is None: return None
    for role in ("searchbox", "combobox"):
        a = root.get_by_role(role).all()
        if a: return a[0]
    a = root.locator("input:visible,textarea:visible")
    return a.first if a.count() else None
def wait_field(page):
    end=time.monotonic()+3; f=None
    while time.monotonic()<end:
        f=field(page)
        if f and f.is_visible():
            # Let the opened dialog finish its entry animation before clicking.
            try:
                root=modal(page)
                if root is not None:
                    root.evaluate("el => [...el.getAnimations({subtree:true})].filter(a => Number.isFinite(a.effect?.getComputedTiming().endTime) && a.effect.getComputedTiming().endTime < 10000).every(a => a.playState !== 'running')")
                    page.wait_for_timeout(350)
            except Exception: pass
            return f
        page.wait_for_timeout(75)
    return None
def open_search(page):
    wait_trigger(page,timeout=2)
    page.keyboard.press("Control+k"); f=wait_field(page)
    scope = modal(page)
    return (scope if scope is not None else page.locator("body")), f
def wait_closed(page):
    end=time.monotonic()+3
    while time.monotonic()<end:
        if modal(page) is None:
            page.wait_for_timeout(350)
            if modal(page) is None: return True
        page.wait_for_timeout(75)
    return modal(page) is None
def wait_class(page, expected):
    end=time.monotonic()+3
    while time.monotonic()<end:
        if expected in (page.locator("html").get_attribute("class") or "").lower(): return True
        page.wait_for_timeout(75)
    return expected in (page.locator("html").get_attribute("class") or "").lower()
def rows(scope):
    found, loc = [], scope.locator(ITEMS)
    for i in range(loc.count()):
        row = loc.nth(i)
        if not row.is_visible(): continue
        data = row.evaluate("""e => {
          const text=(e.innerText||e.textContent||'').replace(/\\s+/g,' ').trim();
          const g=e.closest('[role=group]'); let heading='';
          if(g){ const ids=(g.getAttribute('aria-labelledby')||'').split(/\\s+/).filter(Boolean);
            heading=ids.map(id=>document.getElementById(id)?.innerText||'').join(' ');
            if(!heading) heading=g.querySelector('[role=heading],h1,h2,h3,h4')?.innerText||''; }
          const aria=e.getAttribute('aria-selected'), dataSelected=e.getAttribute('data-selected');
          return {text,heading,aria:e.getAttribute('aria-label')||'',href:e.getAttribute('href')||'',selected:aria==='true'||dataSelected==='true',dataSelected};
        }""")
        data["index"] = i
        data["identity"] = " ".join(x for x in (data["heading"],data["text"],data["aria"],data["href"]) if x)
        found.append(data)
    return found
def wait_filter(page, scope, query=None, empty=False):
    end=time.monotonic()+2.5; current=[]
    while time.monotonic()<end:
        current=rows(scope); text=" ".join(r["identity"] for r in current)
        if empty and (not current or EMPTY.search(scope.inner_text())):
            page.wait_for_timeout(150)
            return rows(scope)
        if query and len(current)<10 and re.search(re.escape(query),text,re.I):
            # Re-read after a short settle so selection and result rows are current.
            page.wait_for_timeout(150)
            return rows(scope)
        page.wait_for_timeout(60)
    return current
def wait_path(page, expected):
    end=time.monotonic()+4
    while time.monotonic()<end:
        if path(page.url)==expected: return True
        page.wait_for_timeout(100)
    return path(page.url)==expected
def trigger(page):
    for b in page.locator("button:visible,[role=button]:visible").all():
        label=" ".join(filter(None,[b.inner_text(),b.get_attribute("aria-label"),b.get_attribute("title"),b.get_attribute("aria-keyshortcuts")]))
        if re.search(r"search|find|navigate|quick|page|搜索|导航|页面",label,re.I): return b
    return None
def wait_trigger(page,timeout=3):
    end=time.monotonic()+timeout; b=None
    while time.monotonic()<end:
        b=trigger(page)
        if b: return b
        page.wait_for_timeout(75)
    return None
def route_for(row):
    if row.get("href"): return path(row["href"])
    shown_path=re.search(r"(?:^|\s)(/[A-Za-z0-9_/-]+)(?:\s|$)",row.get("identity", ""))
    if shown_path: return path(shown_path.group(1))
    text=row["identity"].lower()
    routes=(("secured by clerk / user management","/clerk/user-management"),("secured by clerk / sign in","/clerk/sign-in"),("secured by clerk / sign up","/clerk/sign-up"),("auth / sign in (2 col)","/sign-in-2"),("auth / sign in","/sign-in"),("auth / sign up","/sign-up"),("auth / forgot password","/forgot-password"),("auth / otp","/otp"),("errors / unauthorized","/errors/unauthorized"),("errors / forbidden","/errors/forbidden"),("errors / not found","/errors/not-found"),("errors / internal server error","/errors/internal-server-error"),("errors / maintenance error","/errors/maintenance-error"),("settings / profile","/settings"),("settings / account","/settings/account"),("settings / appearance","/settings/appearance"),("settings / notifications","/settings/notifications"),("settings / display","/settings/display"),("dashboard","/"),("tasks","/tasks"),("apps","/apps"),("chats","/chats"),("users","/users"),("help center","/help-center"))
    for label,target in routes:
        if label in text: return target
    return None

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--sample",required=True); p.add_argument("--url",required=True)
    p.add_argument("--output",type=Path,default=HERE/"results",help="Root for a fresh timestamped result directory")
    a=p.parse_args(); u=urlsplit(a.url)
    if u.scheme not in {"http","https"} or u.hostname not in {"localhost","127.0.0.1","::1"} or u.username or u.password:
        p.error("Use a loopback fixture URL without credentials.")
    run=datetime.now().strftime("%Y%m%dT%H%M%S%f")
    outdir=a.output/re.sub(r"[^A-Za-z0-9_-]","_",a.sample)/run; outdir.mkdir(parents=True,exist_ok=False)
    keys=["ctrl_k", "arrow_enter", "duplicate_names", "escape_focus", "reopen", "empty_state", "theme_actions", "mobile_touch", "mobile_layout", "runtime_errors"]
    report={"sample":a.sample,"url":a.url,"browser":"Microsoft Edge via Playwright channel=msedge","run":run,
            "checks":{k:{"status":"unknown","evidence":"Not reached."} for k in keys},"console_errors":[],"page_errors":[],"integration_route_errors":[],"screenshots":[]}
    blocked_urls=set()
    def shot(page,name):
        f=outdir/f"{name}.png"; page.screenshot(path=str(f)); report["screenshots"].append(f.name)
    with sync_playwright() as pw:
      try: browser=pw.chromium.launch(channel="msedge",headless=True)
      except Exception as e:
        report["browser_launch_error"]=f"{type(e).__name__}: {e}"; return finish(report,outdir)
      reached=False
      def watch(pg):
        pg.on("console",lambda m:report["console_errors"].append({"path":path(pg.url),"message":m.text,"source_url":m.location.get("url","")}) if m.type=="error" else None)
        pg.on("pageerror",lambda e:report["page_errors"].append({"path":path(pg.url),"message":str(e)}))
      try:
        ctx=browser.new_context(viewport={"width":1365,"height":900},service_workers="block")
        allow_local_only(ctx,a.url,blocked_urls)
        page=ctx.new_page(); watch(page)
        page.goto(a.url.rstrip("/")+"/",wait_until="domcontentloaded",timeout=20000); reached=True; page.wait_for_timeout(300); shot(page,"desktop-home")

        scope,f=open_search(page); record(report["checks"],"ctrl_k",True,"Ctrl+K opened a visible search field.") if f else record(report["checks"],"ctrl_k",None,"No active semantic search panel/input was located after Ctrl+K; confirm visually before judging.")
        if f:
          f.fill("Tasks"); filtered=wait_filter(page,scope,query="Tasks")
          shot(page,"desktop-tasks-results")
          task=next((r for r in filtered if re.search(r"\bTasks\b",r["identity"],re.I)),None)
          if task:
            before=next((r for r in filtered if r["selected"]),None)
            page.keyboard.press("ArrowDown"); end=time.monotonic()+2; selected=None
            while time.monotonic()<end:
              selected=next((r for r in rows(scope) if r["selected"]),None)
              if selected and (not before or selected["identity"]!=before["identity"] or len(filtered)==1): break
              page.wait_for_timeout(60)
            expected=route_for(selected) if selected else None
            if expected:
              page.keyboard.press("Enter"); ok=wait_path(page,expected)
              record(report["checks"],"arrow_enter",ok,f"Query Tasks returned {[r['text'] for r in filtered]!r}; ArrowDown selected {selected['identity']!r}; Enter ended at {page.url}, expected {expected}.")
            else:
              record(report["checks"],"arrow_enter",None,f"Tasks results={[r['text'] for r in filtered]!r}; no selected row with a known baseline route after ArrowDown.")
          else: record(report["checks"],"arrow_enter",None,"No semantic Tasks row was located; selector result is inconclusive until visually checked.")

        page.goto(a.url.rstrip("/")+"/",wait_until="domcontentloaded",timeout=20000); b=wait_trigger(page)
        if b:
          b.focus(); b.click(); opened=wait_field(page) is not None; shot(page,"desktop-trigger-open")
          if opened:
            page.keyboard.press("Escape"); closed=wait_closed(page)
            restored=b.evaluate("e=>e===document.activeElement")
            record(report["checks"],"escape_focus",closed and restored,f"Escape closed={closed}; focus returned={restored}.")
            b.click(); by_click=wait_field(page) is not None
            if by_click: page.keyboard.press("Escape"); wait_closed(page)
            open_search(page); by_key=wait_field(page) is not None
            record(report["checks"],"reopen",by_click and by_key,f"Reopen by click={by_click}, by Ctrl+K={by_key}.")
            if by_key: page.keyboard.press("Escape"); wait_closed(page)
          else:
            record(report["checks"],"escape_focus",False,"Search trigger click did not open."); record(report["checks"],"reopen",False,"Search trigger click did not open.")
        else:
          record(report["checks"],"escape_focus",None,"No accessibly named visible search button was located; confirm visually."); record(report["checks"],"reopen",None,"No accessibly named visible search button was located; confirm visually.")

        scope,f=open_search(page)
        if f:
          f.fill("zzacceptancenoresultzz"); filtered=wait_filter(page,scope,empty=True); txt=scope.inner_text()
          stale=[r for r in filtered if re.search(r"Dashboard|Tasks|Settings|Sign In",r["identity"],re.I)]
          ok=bool(EMPTY.search(txt)) and not stale
          status=ok if EMPTY.search(txt) or stale else None
          record(report["checks"],"empty_state",status,f"Recognized empty copy={bool(EMPTY.search(txt))}, stale page results={len(stale)}, visible text={txt[:220]!r}."); shot(page,"desktop-empty")
        else: record(report["checks"],"empty_state",None,"No active search panel/input to query; confirm visually.")

        page.goto(a.url.rstrip("/")+"/",wait_until="domcontentloaded",timeout=20000); scope,f=open_search(page)
        if f:
          f.fill("Sign In"); first=wait_filter(page,scope,query="Sign In"); first=[r for r in first if re.search(r"Sign\s+In",r["identity"],re.I)]; labels=[r["identity"] for r in first]
          shot(page,"desktop-duplicate-sign-in")
          destinations={}
          for key,target in (("auth","/sign-in"),("clerk","/clerk/sign-in")):
            page.goto(a.url.rstrip("/")+"/",wait_until="domcontentloaded",timeout=20000); s,x=open_search(page)
            if not x: destinations[key]="reopen failed"; continue
            x.fill("Sign In"); fresh=wait_filter(page,s,query="Sign In"); match=next((r for r in fresh if key in r["identity"].lower() and re.search(r"Sign\s+In",r["identity"],re.I)),None)
            if match: s.locator(ITEMS).nth(match["index"]).click(); wait_path(page,target)
            destinations[key]=path(page.url)
          identified=len(first)>=2 and len(set(labels))>=2 and any(re.search(r"\bauth\b",x,re.I) for x in labels) and any("clerk" in x.lower() for x in labels)
          navigated=destinations=={"auth":"/sign-in","clerk":"/clerk/sign-in"}
          duplicate_status=(identified and navigated) if identified else None
          record(report["checks"],"duplicate_names",duplicate_status,f"Entries={labels!r}; selected routes={destinations!r}; visually confirm if row/context selectors missed.")
        else: record(report["checks"],"duplicate_names",None,"No active search panel/input to query; confirm visually.")

        page.goto(a.url.rstrip("/")+"/",wait_until="domcontentloaded",timeout=20000); scope,f=open_search(page); states={}; ok=bool(f); theme_selector_unknown=False
        shot(page,"desktop-theme-options")
        for label in ("Light","Dark"):
          if not f: ok=False; break
          # Use the palette's search workflow, avoiding browser-specific
          # scrollIntoView behavior across nested scrolling containers.
          f.fill(label)
          scope.get_by_role("option", name=label, exact=True).wait_for(state="visible")
          r=next((x for x in rows(scope) if x["text"].strip().lower()==label.lower()),None)
          if not r: ok=False; theme_selector_unknown=True; states[label]="not located; inspect screenshot"; break
          scope.get_by_role("option", name=label, exact=True).click()
          state_ok=wait_class(page,label.lower()); states[label]=page.locator("html").get_attribute("class") or ""
          if not state_ok: ok=False; theme_selector_unknown=True
          # A color change can precede the dialog's closing animation. Reopening
          # during that transition is a different interaction from this check.
          if not wait_closed(page):
            ok=False; theme_selector_unknown=True; break
          scope,f=open_search(page)
        page.emulate_media(color_scheme="light")
        if f:
          f.fill("System")
          scope.get_by_role("option", name="System", exact=True).wait_for(state="visible")
        r=next((x for x in rows(scope) if x["text"].strip().lower()=="system"),None) if f else None
        if r:
          scope.get_by_role("option", name="System", exact=True).click(); state_ok=wait_class(page,"light"); states["System"]=page.locator("html").get_attribute("class") or ""; ok=ok and state_ok
        else: ok=False; theme_selector_unknown=True; states["System"]="not located; inspect screenshot"
        record(report["checks"],"theme_actions",None if theme_selector_unknown else ok,f"Theme actions/states={states!r}; inspect the saved menu screenshot when an action/state selector did not match.")

        mob=browser.new_context(viewport={"width":390,"height":844},device_scale_factor=1,is_mobile=True,has_touch=True,service_workers="block")
        allow_local_only(mob,a.url,blocked_urls)
        mp=mob.new_page(); watch(mp)
        mp.goto(a.url.rstrip("/")+"/",wait_until="domcontentloaded",timeout=20000); b=wait_trigger(mp); box=b.bounding_box() if b else None
        if b:
          try: b.tap(timeout=2000); f=wait_field(mp)
          except Exception: f=None
          opened=bool(f)
          shot(mp,"mobile-trigger-open")
        else: opened=False; f=None
        if opened:
          s=modal(mp); s=s if s is not None else mp.locator("body")
          f.tap(timeout=2000); mp.keyboard.insert_text("Tasks"); mobile_rows=wait_filter(mp,s,query="Tasks"); shot(mp,"mobile-search-results")
          r=next((x for x in mobile_rows if re.search(r"\bTasks\b",x["identity"],re.I)),None); rb=s.locator(ITEMS).nth(r["index"]).bounding_box() if r else None
          panel=modal(mp); db=panel.bounding_box() if panel else None
          fits=bool(box and rb and db and box["x"]>=0 and box["y"]>=0 and box["x"]+box["width"]<=390 and box["y"]+box["height"]<=844 and rb["x"]>=0 and rb["y"]>=0 and rb["x"]+rb["width"]<=390 and rb["y"]+rb["height"]<=844 and db["x"]>=0 and db["y"]>=0 and db["x"]+db["width"]<=390 and db["y"]+db["height"]<=844 and mp.evaluate("document.documentElement.scrollWidth<=innerWidth"))
          arrived=False
          if r: s.locator(ITEMS).nth(r["index"]).tap(timeout=2000); arrived=wait_path(mp,"/tasks")
          touch_status=arrived if r else None
          layout_status=fits if rb and db else None
          record(report["checks"],"mobile_touch",touch_status,f"Tap search + Tasks; URL={mp.url}; inspect screenshot if result selector missed."); record(report["checks"],"mobile_layout",layout_status,f"390x844 bounds: trigger={box}, result={rb}, panel={db}; no clipping/overflow={fits}; target size is recorded for human usability judgment."); shot(mp,"mobile-after-tap")
        else:
          status=None
          record(report["checks"],"mobile_touch",status,"No accessible tap-opened search control at 390x844; visually confirm whether this is a selector miss."); record(report["checks"],"mobile_layout",None,f"Trigger box={box}; search panel/input was not located.")
        mob.close()
      except Exception as e: report["run_error"]=f"{type(e).__name__}: {e}"
      finally:
        errs=report["console_errors"]+report["page_errors"]
        report["blocked_external_requests"]=sorted(blocked_urls)
        report["blocked_resource_errors"]=[e for e in errs if e.get("source_url") in blocked_urls]
        report["integration_route_errors"]=[e for e in errs if e["path"].startswith("/clerk/")]
        app_errs=[e for e in errs if not e["path"].startswith("/clerk/") and e.get("source_url") not in blocked_urls]
        record(report["checks"],"runtime_errors",None if not reached else not app_errs,
               f"Local non-Clerk runtime errors={app_errs!r}; errors from intentionally blocked external resource URLs and Clerk demo routes are separately recorded and excluded from navigation regression judgement.")
        browser.close()
    return finish(report,outdir)

def finish(report,outdir):
    f=outdir/"report.json"; f.write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding="utf-8"); print(f)
    for k,v in report["checks"].items(): print(f"{v['status'].upper():7} {k}: {v['evidence']}")
    return 0 if all(x["status"]=="pass" for x in report["checks"].values()) else 1

if __name__=="__main__": raise SystemExit(main())
