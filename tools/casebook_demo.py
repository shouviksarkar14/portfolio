"""Builds the public Casebook Studio demo: the original engine, with three
cases written for this demo instead of the 251 casebook-derived ones."""
import json, sys

SRC, OUT = sys.argv[1], sys.argv[2]
src = open(SRC, encoding="utf-8").read()
start = src.index("const DATA = ") + len("const DATA = ")
data, end = json.JSONDecoder().raw_decode(src, start)

def N(id, parent, label, detail, type, refs, **kw):
    n = {"id": id, "parent": parent, "label": label, "detail": detail, "type": type, "turn_refs": refs}
    n.update(kw)
    return n

def T(*pairs):
    return [{"speaker": s, "text": t} for s, t in pairs]

I, C = "Interviewer", "Candidate"
SRC_LABEL = "Original demo case, written for this portfolio"

rca = {
  "id": "demo_rca_upi_success_drop",
  "source": SRC_LABEL, "page_range": "-",
  "title": "UPI Payment Success Rate Drop",
  "company": "Not specified (fictional)",
  "industry": "Fintech / Payments",
  "prompt": "UPI payment success rate on our app fell from 94% to 88% over the last week. Find out why.",
  "clarifying_questions": [
    {"q": "How is success rate defined: completed payments over initiated, or over attempts reaching the bank?", "a": "Completed over initiated, measured in-app."},
    {"q": "Was the drop sudden or gradual?", "a": "Sudden. It started on Tuesday afternoon."},
    {"q": "Any releases, partner changes or outages that week?", "a": "We shipped app version 6.2 on Tuesday morning. Nothing else that we know of."},
  ],
  "framework_used": "Root cause: clarify, split internal vs external, segment, isolate, validate",
  "decision_tree": [
    N("n1", None, "UPI success rate 94% to 88% in a week", "A six-point drop in a core payments metric. Treat it as an incident before a strategy question.", "context", [0]),
    N("n2", "n1", "Clarify the metric and timing", "Completed over initiated, in-app. Sudden onset on Tuesday afternoon, same day as release 6.2.", "context", [1, 2, 3, 4]),
    N("n3", "n1", "External causes", "Check what we do not control before blaming our own release.", "segment", [5]),
    N("n4", "n3", "Bank or PSP downtime", "NPCI and partner bank status, failure codes from the switch.", "option", [5, 6]),
    N("n5", "n3", "Seasonality or demand mix", "Festive spikes or a promo pulling in new, less reliable payers.", "option", [5, 6]),
    N("n6", "n1", "Internal causes", "Things we changed: release 6.2, backend config, risk rules.", "segment", [5]),
    N("n7", "n6", "Segment the drop", "Cut by app version, OS, bank, amount band and new vs returning users.", "decision", [7, 8]),
    N("n8", "n7", "Only version 6.2 on Android drops", "iOS and older Android versions hold at 94%. The drop lives in one build.", "metric", [8], value="6.2 Android: 81%"),
    N("n9", "n8", "Funnel inside 6.2", "Initiated, PIN screen shown, PIN entered, bank response, success screen.", "decision", [9]),
    N("n10", "n9", "Users drop at the PIN screen", "PIN-screen-shown to PIN-entered fell sharply; bank responses look normal.", "metric", [10], value="PIN entry -9 pts"),
    N("n11", "n10", "Hypothesis: new PIN screen breaks on some keyboards", "6.2 redesigned the PIN entry. Third-party keyboards may not open the numeric pad.", "decision", [11]),
    N("n12", "n11", "Validate with session data and a repro", "Check device and keyboard logs, reproduce on two popular keyboards, read support tickets.", "decision", [12]),
    N("n13", "n1", "Recommendation", "Roll back the PIN screen behind a flag today; fix and re-release with keyboard coverage tests.", "decision", [13], result=True),
    N("n14", "n13", "Watch: success rate by version, hourly", "Confirms the rollback worked and catches a repeat.", "metric", [13]),
    N("n15", "n13", "Risk: lost trust from failed payments", "Users who failed may switch apps. Consider a nudge or cashback for affected users.", "risk", [13]),
  ],
  "recommendation": [
    "Roll back the redesigned PIN screen behind a feature flag today; that recovers most of the drop if the hypothesis holds.",
    "Fix keyboard handling, add device and keyboard coverage to release testing, and re-release with a staged rollout.",
    "Reach out to users who failed a payment this week, since a failed payment costs more trust than a slow one.",
  ],
  "metrics": ["Payment success rate by app version and OS, hourly", "PIN-screen-shown to PIN-entered conversion", "Repeat payment rate of users who failed this week"],
  "risks": [
    "The keyboard hypothesis may only explain part of the drop; keep checking bank failure codes in parallel.",
    "A rollback can reintroduce whatever the redesign fixed; check what 6.2 was meant to solve.",
  ],
  "interviewer_pushbacks": [
    {"pushback": "Why not start with the banks? Bank downtime is the usual cause.", "handling": "Ruled it out quickly with data: the drop is confined to one app build, and bank responses are normal. Segmenting first saved chasing the wrong cause."},
    {"pushback": "Would you roll back without being sure?", "handling": "Yes, behind a flag. A payments failure is expensive for users, and a flag makes the rollback cheap to reverse."},
  ],
  "transcript": T(
    (I, "UPI payment success rate on our app fell from 94% to 88% over the last week. Find out why."),
    (C, "First, how do we define success rate: completed over initiated, or over requests that reached the bank?"),
    (I, "Completed over initiated, measured in-app."),
    (C, "Was it sudden or gradual, and did anything change that week: a release, a partner, an outage?"),
    (I, "Sudden, from Tuesday afternoon. We shipped app version 6.2 on Tuesday morning."),
    (C, "I'll split causes into external, like bank or PSP downtime and demand mix, and internal, like our release, config or risk rules. The timing points inside, but I want data to rule the banks out."),
    (I, "Bank status pages were green and failure codes from the switch look normal."),
    (C, "Then I'd segment the drop by app version, OS, bank, amount band and new versus returning users."),
    (I, "Only version 6.2 on Android is down, at about 81%. iOS and older Android builds are still at 94%."),
    (C, "Inside 6.2, I'd walk the funnel: payment initiated, PIN screen shown, PIN entered, bank response, success screen."),
    (I, "The big fall is between PIN screen shown and PIN entered."),
    (C, "6.2 redesigned the PIN screen. My hypothesis is that on some third-party keyboards the numeric pad doesn't open, so users give up."),
    (C, "I'd validate with device and keyboard logs, reproduce it on the two most common keyboards, and read support tickets from this week."),
    (C, "Recommendation: roll back the PIN screen behind a flag today, fix it with keyboard coverage tests, re-release in stages, and watch success rate by version hourly. I'd also reach out to users who failed a payment."),
  ),
  "key_takeaway": "Segment before you theorise. One cut by app version turned a vague six-point drop into a single broken screen.",
  "extraction_notes": "Written for this demo. Numbers are illustrative.",
  "facets": {"case_type": "Root Cause Analysis", "industry": "Fintech / Payments", "geography": "India", "emphasis": ["Metrics/Measurement", "Funnel analysis"], "moves": ["Incident diagnosis"], "difficulty": "Foundational", "product_form": "Digital"},
  "subtopics": ["Internal vs external split", "Segment by version", "Funnel isolation", "Rollback behind a flag"],
  "framework_mapping": [
    {"stage": "Clarify", "generic": "Pin down the metric definition and the timeline.", "specific": "Completed over initiated; sudden drop on release day."},
    {"stage": "Internal vs external", "generic": "List causes you control and causes you don't.", "specific": "Banks and demand mix vs release 6.2 and config."},
    {"stage": "Segment", "generic": "Cut the metric until the drop concentrates.", "specific": "Only 6.2 on Android is down."},
    {"stage": "Isolate", "generic": "Walk the funnel inside the affected segment.", "specific": "Drop sits at PIN entry."},
    {"stage": "Validate and act", "generic": "Prove the cause, fix it, and set guardrails.", "specific": "Repro on keyboards, rollback behind a flag, hourly monitoring."},
  ],
}

design = {
  "id": "demo_pd_stale_applications",
  "source": SRC_LABEL, "page_range": "-",
  "title": "Stale Job Applications",
  "company": "Not specified (fictional)",
  "industry": "Consumer / Careers",
  "prompt": "Job seekers on our app apply to dozens of roles and then lose track of them. Design a feature that helps.",
  "clarifying_questions": [
    {"q": "Who are our users: students, early-career, or senior professionals?", "a": "Mostly people with 1 to 6 years of experience switching jobs."},
    {"q": "What does the business care about: retention, or something like placements?", "a": "Retention first. People churn once their search goes quiet."},
    {"q": "Do we see their applications today?", "a": "Only the ones they apply to through us. Most applications happen elsewhere."},
  ],
  "framework_used": "Product design: user, pain, solutions, prioritise, measure",
  "decision_tree": [
    N("n1", None, "Help job seekers keep track of applications", "Retention problem: users churn when their search goes quiet and messy.", "context", [0]),
    N("n2", "n1", "Scope", "Switchers with 1 to 6 years of experience; retention is the goal; we only see in-app applications.", "context", [1, 2, 3, 4]),
    N("n3", "n1", "Segments", "Who loses track, and why.", "segment", [5]),
    N("n4", "n3", "High-volume appliers", "Apply to 30+ roles, mostly one-click; can't recall which CV went where.", "segment", [5]),
    N("n5", "n3", "Referral-led searchers", "Fewer applications, more people involved; lose track of who promised what.", "segment", [5]),
    N("n6", "n3", "Target: high-volume appliers", "Biggest group, and the one whose search goes stale fastest.", "decision", [6]),
    N("n7", "n6", "Pain: applications live outside our app", "Confirmation emails are the only complete record.", "context", [7]),
    N("n8", "n6", "Pain: no signal on when to follow up", "Silence after applying is ambiguous: still in review, or rejected?", "context", [7]),
    N("n9", "n6", "Option: import from email", "Read application confirmations from the user's inbox, with consent, to build the list automatically.", "option", [8]),
    N("n10", "n6", "Option: follow-up nudges", "Nudge at 7 days of silence, suggest closing at 21.", "option", [8]),
    N("n11", "n6", "Option: CV-per-application log", "Record which CV version each application used; show which converts.", "option", [8]),
    N("n12", "n6", "Prioritise by value and effort", "Email import unlocks the other two but needs trust and consent work.", "decision", [9, 10]),
    N("n13", "n12", "Ship nudges and CV log first, email import as a beta", "Quick wins on in-app data now; test consent appetite with an opt-in beta.", "decision", [10], result=True),
    N("n14", "n1", "Success metrics", "Did the search stay alive?", "metric", [11]),
    N("n15", "n14", "Weekly active searchers; follow-ups sent per user", "Leading signals of an active search.", "metric", [11]),
    N("n16", "n1", "Risk: inbox access feels invasive", "Read only application emails, show what was read, and make it one-tap to disconnect.", "risk", [12]),
  ],
  "recommendation": [
    "Target high-volume appliers: the largest group and the one whose search goes stale fastest.",
    "Ship follow-up nudges and a CV-per-application log on in-app data first; run email import as an opt-in beta.",
    "Measure weekly active searchers and follow-ups sent, with uninstall rate after inbox consent as a guardrail.",
  ],
  "metrics": ["Weekly active searchers", "Follow-ups sent per user", "Share of applications with a logged outcome", "Guardrail: disconnects and uninstalls after granting inbox access"],
  "risks": [
    "Inbox access is a trust jump; a bad first impression can sink the whole feature.",
    "Nudges that fire too often become noise; cap them and let users snooze.",
  ],
  "interviewer_pushbacks": [
    {"pushback": "Email import is the most powerful idea. Why not lead with it?", "handling": "It is, but it depends on users trusting us with their inbox. Shipping value on our own data first earns that trust and tells us who would opt in."},
    {"pushback": "How do you know nudges at 7 and 21 days are right?", "handling": "They're starting guesses. I'd test the timing against reply rates and adjust."},
  ],
  "transcript": T(
    (I, "Job seekers on our app apply to dozens of roles and then lose track of them. Design a feature that helps."),
    (C, "Who are the users, and what does the business want: retention or placements?"),
    (I, "Mostly switchers with 1 to 6 years of experience. Retention first, because people churn when their search goes quiet."),
    (C, "Do we see all their applications?"),
    (I, "Only the ones made through us. Most happen elsewhere."),
    (C, "Two segments lose track: high-volume appliers who one-click 30+ roles and can't recall which CV went where, and referral-led searchers juggling people more than postings."),
    (C, "I'll focus on high-volume appliers. They're the biggest group and their search goes stale fastest."),
    (C, "Their pains: the full record lives in confirmation emails, not in our app, and silence after applying gives no signal on when to follow up."),
    (C, "Options: import applications from email with consent; nudge at 7 days of silence and suggest closing at 21; and log which CV each application used so users see what converts."),
    (I, "How would you prioritise?"),
    (C, "Email import unlocks the rest but needs trust. So I'd ship nudges and the CV log on in-app data now, and run email import as an opt-in beta."),
    (C, "Success is weekly active searchers and follow-ups sent per user."),
    (C, "The main risk is that inbox access feels invasive, so I'd read only application emails, show exactly what was read, and make disconnecting one tap."),
  ),
  "key_takeaway": "Sequence by trust, not by power. The strongest feature waits until cheaper ones have earned the user's permission.",
  "extraction_notes": "Written for this demo; inspired by the problem behind Switch Board.",
  "facets": {"case_type": "Product Design", "industry": "Consumer / Careers", "geography": "India", "emphasis": ["Segmentation/Targeting", "Prioritization", "Trust/Privacy"], "moves": ["Feature design"], "difficulty": "Intermediate", "product_form": "Digital"},
  "subtopics": ["Segment by behaviour", "Sequencing by trust", "Consent design", "Leading metrics"],
  "framework_mapping": [
    {"stage": "Scope", "generic": "Clarify the user and the goal.", "specific": "Switchers, retention."},
    {"stage": "Segment", "generic": "Choose whom to serve.", "specific": "High-volume appliers."},
    {"stage": "Pains", "generic": "Name the needs.", "specific": "Record lives in email; no follow-up signal."},
    {"stage": "Solutions", "generic": "Generate options per pain.", "specific": "Email import, nudges, CV log."},
    {"stage": "Prioritise and measure", "generic": "Rank, then define success.", "specific": "Nudges and CV log first; weekly active searchers."},
  ],
}

guess = {
  "id": "demo_gs_qcommerce_orders",
  "source": SRC_LABEL, "page_range": "-",
  "title": "Quick-Commerce Orders in Bengaluru",
  "company": "Not specified (fictional)",
  "industry": "Consumer / Quick commerce",
  "prompt": "Estimate how many quick-commerce grocery orders are placed in Bengaluru on a typical weekday.",
  "clarifying_questions": [
    {"q": "All quick-commerce apps combined, or one player?", "a": "All combined."},
    {"q": "Groceries only, or everything these apps sell?", "a": "Everything they sell."},
  ],
  "framework_used": "Guesstimate: population, segment, frequency, sanity check",
  "decision_tree": [
    N("n1", None, "Weekday quick-commerce orders, Bengaluru", "Demand-side estimate across all apps.", "context", [0]),
    N("n2", "n1", "Scope: all apps, all categories", "Avoids double-counting debates between players.", "context", [1, 2]),
    N("n3", "n1", "Households", "Assume about 1.4 crore people and 3.5 people per household.", "metric", [3], value="~40 lakh"),
    N("n4", "n3", "Households in serviceable areas", "Assume 80% live within dark-store coverage.", "metric", [4], value="~32 lakh"),
    N("n5", "n4", "Households that use quick commerce", "Assume 45% have ordered in the last month.", "metric", [4], value="~14.4 lakh"),
    N("n6", "n5", "Segment by frequency", "Users differ hugely in how often they order.", "segment", [5]),
    N("n7", "n6", "Heavy users: 30%, 4 orders a week", "~4.3 lakh households × 4 / 7 ≈ 2.5 lakh a day.", "option", [5], value="~2.5 lakh"),
    N("n8", "n6", "Regular users: 40%, 1.5 a week", "~5.8 lakh × 1.5 / 7 ≈ 1.2 lakh a day.", "option", [5], value="~1.2 lakh"),
    N("n9", "n6", "Occasional users: 30%, 2 a month", "~4.3 lakh × 2 / 30 ≈ 0.3 lakh a day.", "option", [5], value="~0.3 lakh"),
    N("n10", "n1", "Total ≈ 4 lakh orders a weekday", "2.5 + 1.2 + 0.3 lakh. Weekdays run a little below weekends.", "decision", [6], result=True, value="~4 lakh"),
    N("n11", "n10", "Sanity check from supply", "At ~300 dark stores, that's ~1,300 orders per store per day, plausible for busy stores.", "metric", [7]),
    N("n12", "n10", "Swing assumption: heavy-user share", "If 10 points of heavy users are really regular users, the total falls by about 13%.", "risk", [8]),
  ],
  "recommendation": [
    "About 4 lakh quick-commerce orders on a typical weekday in Bengaluru, across all apps.",
    "The estimate is most sensitive to the share of heavy users; that's the assumption to test first.",
  ],
  "metrics": ["Orders per serviceable household per week", "Orders per dark store per day"],
  "risks": ["Every input is an assumption; the structure matters more than the number.", "Store-count sanity checks depend on how many stores are actually live."],
  "interviewer_pushbacks": [
    {"pushback": "Why segment by frequency instead of using one average?", "handling": "Quick commerce is driven by a heavy-user core. One average hides that and makes the estimate fragile."},
  ],
  "transcript": T(
    (I, "Estimate how many quick-commerce grocery orders are placed in Bengaluru on a typical weekday."),
    (C, "All apps combined, and everything they sell, not just groceries?"),
    (I, "Yes, all apps and all categories."),
    (C, "I'll start from households. Assume about 1.4 crore people at 3.5 per household, so roughly 40 lakh households."),
    (C, "Assume 80% are in serviceable areas, about 32 lakh, and 45% of those ordered in the last month, about 14.4 lakh households."),
    (C, "Split by frequency: 30% heavy users at 4 orders a week give about 2.5 lakh a day; 40% regular users at 1.5 a week give about 1.2 lakh; 30% occasional users at 2 a month give about 0.3 lakh."),
    (C, "That totals about 4 lakh orders on a weekday."),
    (C, "Sanity check from supply: with around 300 dark stores, that's about 1,300 orders per store per day, which is plausible for busy stores."),
    (C, "The swing assumption is the heavy-user share. If 10 points of heavy users are really regular users, the total falls by about 13%, so that's what I'd validate first."),
  ),
  "key_takeaway": "Segment by behaviour, then sanity-check from the other side of the market.",
  "extraction_notes": "Written for this demo. All inputs are stated assumptions, not data.",
  "facets": {"case_type": "Guesstimate", "industry": "Consumer / Quick commerce", "geography": "India", "emphasis": ["Estimation", "Sanity checks"], "moves": ["Market sizing"], "difficulty": "Foundational", "product_form": "Digital + physical"},
  "subtopics": ["Household base", "Frequency segments", "Supply-side sanity check", "Sensitivity"],
  "framework_mapping": [
    {"stage": "Base", "generic": "Start from a population you can defend.", "specific": "~40 lakh households."},
    {"stage": "Filter", "generic": "Narrow to the addressable group.", "specific": "Serviceable and active: ~14.4 lakh."},
    {"stage": "Frequency", "generic": "Segment by behaviour.", "specific": "Heavy, regular, occasional."},
    {"stage": "Check", "generic": "Cross-check from another angle.", "specific": "Orders per dark store."},
  ],
}

# Arithmetic check for the guesstimate (fail the build if the numbers drift).
hh = 1.4e7 / 3.5; act = hh * 0.8 * 0.45
daily = act * .3 * 4 / 7 + act * .4 * 1.5 / 7 + act * .3 * 2 / 30
assert round(hh / 1e5) == 40 and round(act / 1e4) == 144, (hh, act)
assert 3.8e5 < daily < 4.2e5, daily
assert 1250 < daily / 300 < 1400, daily / 300
low = act * .2 * 4 / 7 + act * .5 * 1.5 / 7 + act * .3 * 2 / 30
assert 0.12 < 1 - low / daily < 0.14, 1 - low / daily  # "about 13%"

cases = [design, rca, guess]
pm = data["disciplines"][0]
pm.update({
  "subtitle": "3 demo cases written for this portfolio. The full library is private.",
  "source": "demo",
  "intro": {"id": "pm_overview", "page_range": "-", "title": "Product Management: case methods",
            "definition": "Each case is a decision tree you click through: clarify, structure, decide, defend.",
            "steps": [{"step": "Product Design", "detail": "Design or improve a product for a chosen user."},
                      {"step": "Root Cause Analysis", "detail": "Find why a metric moved before fixing it."},
                      {"step": "Guesstimate", "detail": "Estimate a number from defensible assumptions."}]},
  "frameworks": [
    {"id": "fw_design", "name": "Product design", "source": "General method", "page": "", "when_to_use": "Design or improve product X.", "steps": ["Scope", "Segment", "Pains", "Solutions", "Prioritise", "Measure"]},
    {"id": "fw_rca", "name": "Root cause", "source": "General method", "page": "", "when_to_use": "Metric X moved. Why?", "steps": ["Clarify", "Internal vs external", "Segment", "Isolate", "Validate", "Act"]},
    {"id": "fw_guess", "name": "Guesstimate", "source": "General method", "page": "", "when_to_use": "How many X?", "steps": ["Base", "Filter", "Frequency", "Sanity check"]},
  ],
  "coverage": {"built": 3, "flagged": 0, "by_type": {"Product Design": 1, "Root Cause Analysis": 1, "Guesstimate": 1}},
  "cases": cases,
})
data["disciplines"] = [pm]
data["subtitle"] = "Interview cases as click-through decision trees. Public demo: 3 original cases."

out = src[:start] + json.dumps(data, ensure_ascii=False) + src[end:]
out = out.replace('· pp. ${esc((c.page_range||"").split(" ")[0])} ', "", 1)
out = out.replace("IIM Ahmedabad Consult Club prep book.", "Consulting cases.").replace(" — 6 sources.\"", ".\"")
analytics = '<script defer src="/_vercel/insights/script.js"></script>'
out = out.replace("<title>Casebook Studio</title>", "<title>Casebook Studio · demo</title>", 1)
footer = ('<p style="text-align:center;font-size:12px;color:var(--ink-3);padding:0 16px 32px">'
          'Built by <a href="/" style="color:inherit">Shouvik Sarkar</a> · Demo with 3 original cases. '
          'The full 251-case library is private.</p>')
out = out.replace("</body>", footer + "</body>", 1) if out.count("</body>") else out + footer
i = out.rfind("</body>")
out = out[:i] + analytics + "\n" + out[i:]
open(OUT, "w", encoding="utf-8").write(out)
print("ok", len(out), "daily", round(daily), "per store", round(daily / 300), "drop", round(1 - low / daily, 3))
