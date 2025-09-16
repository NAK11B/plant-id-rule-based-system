from typing import List, Dict, Tuple, Callable

# -------- Knowledge Base (trim for brevity; add more species) ----------
KB: List[Dict] = [
  {"name":"Red Maple","habit":"tree","leaf_type":"simple","arrangement":"opposite",
   "margin":"lobed","lobes":"shallow","venation":"palmate","fruit":"samara","evergreen":False},
  {"name":"Sugar Maple","habit":"tree","leaf_type":"simple","arrangement":"opposite",
   "margin":"lobed","lobes":"deep","venation":"palmate","fruit":"samara","evergreen":False},
  {"name":"White Oak","habit":"tree","leaf_type":"simple","arrangement":"alternate",
   "margin":"lobed","lobes":"deep","venation":"pinnate","fruit":"nut","evergreen":False},
  {"name":"Pin Oak","habit":"tree","leaf_type":"simple","arrangement":"alternate",
   "margin":"lobed","lobes":"deep","venation":"pinnate","fruit":"nut","evergreen":False},
  {"name":"Eastern Redbud","habit":"tree","leaf_type":"simple","arrangement":"alternate",
   "margin":"entire","venation":"palmate","flower_color":"pink","fruit":"pod"},
  {"name":"Flowering Dogwood","habit":"tree","leaf_type":"simple","arrangement":"opposite",
   "margin":"entire","venation":"pinnate","flower_color":"white","fruit":"drupe"},
  {"name":"American Elm","habit":"tree","leaf_type":"simple","arrangement":"alternate",
   "margin":"serrated","venation":"pinnate","fruit":"samara"},
  {"name":"Green Ash","habit":"tree","leaf_type":"compound","arrangement":"opposite",
   "leaflet_count":7,"margin":"serrated","venation":"pinnate"},
  {"name":"Black Walnut","habit":"tree","leaf_type":"compound","arrangement":"alternate",
   "leaflet_count":17,"fruit":"nut","venation":"pinnate"},
  {"name":"Eastern White Pine","habit":"tree","leaf_type":"needle","evergreen":True,"fruit":"cone"},
  {"name":"Eastern Redcedar","habit":"tree","leaf_type":"scale","evergreen":True,"fruit":"cone"},
  {"name":"Poison Ivy","habit":"vine","leaf_type":"compound","leaflet_count":3,"arrangement":"alternate","seasonal_clue":"fall_red"},
  {"name":"Bush Honeysuckle","habit":"shrub","leaf_type":"simple","arrangement":"opposite","margin":"entire","flower_color":"white","fruit":"berry"}
]

# -------- Question set (can be dynamic later) ----------
QUESTIONS = [
  ("habit","Is it a tree, shrub, or vine?", ["tree","shrub","vine"]),
  ("leaf_type","Leaf type?", ["simple","compound","needle","scale"]),
  ("arrangement","Leaf arrangement?", ["opposite","alternate","whorled","unknown"]),
  ("margin","Leaf margin?", ["entire","serrated","lobed","unknown"]),
  ("venation","Leaf venation?", ["palmate","pinnate","unknown"]),
  ("lobes","Lobe depth (if lobed)?", ["none","shallow","deep","unknown"]),
  ("leaflet_count","Leaflet count (if compound)?", ["3","5","7",">7","unknown"]),
  ("flower_color","Flower color (if seen)?", ["white","pink","yellow","red","green","none/unknown"]),
  ("fruit","Fruit/cone type (if seen)?", ["samara","pod","cone","nut","berry","drupe","none/unknown"]),
  ("evergreen","Is it evergreen (keeps leaves/needles year-round)?", ["true","false","unknown"]),
]

Answer = Dict[str,str]
Rule = Callable[[Dict, Answer], Tuple[int,str]]  # (delta, explanation)

def _bool(ans: str):
  return True if ans=="true" else False if ans=="false" else None

# ---- Heuristic rules (add more as you expand) ----
def rule_conifer(species: Dict, a: Answer) -> Tuple[int,str]:
  lt = a.get("leaf_type")
  if lt in {"needle","scale"}:
    if species.get("leaf_type") in {"needle","scale"}:
      return (3,"conifer match")
    else:
      return (-2,"not a conifer")
  return (0,"")

def rule_maple_oak(species: Dict, a: Answer) -> Tuple[int,str]:
  if a.get("margin")=="lobed":
    ven = a.get("venation")
    if ven=="palmate":
      return (2,"lobed+palmate → maple") if "Maple" in species["name"] else (-1,"not maple")
    if ven=="pinnate":
      return (2,"lobed+pinnate → oak") if "Oak" in species["name"] else (-1,"not oak")
  return (0,"")

def rule_opposite(species: Dict, a: Answer) -> Tuple[int,str]:
  if a.get("arrangement")=="opposite":
    families = {"Maple","Ash","Dogwood","Honeysuckle"}
    if any(x in species["name"] for x in families):
      return (2,"opposite leaves family")
    else:
      return (-1,"opposite given, species usually alternate")
  return (0,"")

def rule_poison_ivy(species: Dict, a: Answer) -> Tuple[int,str]:
  if a.get("habit")=="vine" and a.get("leaf_type")=="compound" and a.get("leaflet_count")=="3":
    return (5,"classic poison ivy pattern") if species["name"]=="Poison Ivy" else (-3,"not poison ivy")
  return (0,"")

def rule_evergreen(species: Dict, a: Answer) -> Tuple[int,str]:
  ev = a.get("evergreen")
  if ev in {"true","false"}:
    want = _bool(ev)
    has = species.get("evergreen", False)
    return (2,"evergreen match") if want==has else (-1,"evergreen mismatch")
  return (0,"")

def rule_direct_matches(species: Dict, a: Answer) -> Tuple[int,str]:
  score, hits = 0, []
  for k,v in a.items():
    if v and v not in {"unknown","none/unknown"}:
      if str(species.get(k)) == v:
        score += 1
        hits.append(k)
  return (score, f"direct matches: {', '.join(hits)}") if hits else (0,"")

RULES: List[Rule] = [
  rule_conifer, rule_maple_oak, rule_opposite, rule_poison_ivy, rule_evergreen, rule_direct_matches
]

def ask_user() -> Answer:
  print("Plant ID (rule-based). Press Enter to skip a question.")
  answers: Answer = {}
  for key, prompt, options in QUESTIONS:
    opts = "/".join(options)
    val = input(f"{prompt} [{opts}]: ").strip().lower()
    if val: answers[key] = val
  return answers

def rank_species(answers: Answer):
  results = []
  for sp in KB:
    total, why = 0, []
    for rule in RULES:
      delta, expl = rule(sp, answers)
      total += delta
      if expl: why.append(expl)
    results.append((total, sp["name"], why))
  results.sort(key=lambda x: x[0], reverse=True)
  return results

def main():
  a = ask_user()
  ranked = rank_species(a)
  print("\nTop candidates:")
  for score, name, why in ranked[:5]:
    print(f"  {name:22s}  score={score}  because: {', '.join(why) if why else '—'}")
  if len(ranked)>1 and ranked[0][0]-ranked[1][0] < 3:
    print("\n⚠️ Close call. To break the tie, check: fruit type, leaflet count, and bark texture.")

if __name__ == "__main__":
  main()
