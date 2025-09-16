"""
Rule-Based Plant/Tree/Shrub Identifier (Step 3 rubric version)
- Uses input() for user interaction
- Uses if/elif rule logic (no ML, no external libs)
- Outputs a ranked guess + a human explanation of which rules fired
"""

# --- tiny knowledge base (keep it small for the rubric demo) ---
SPECIES = [
    {
        "name": "Red Maple",
        "traits": {
            "habit": "tree", "leaf_type": "simple", "arrangement": "opposite",
            "margin": "lobed", "venation": "palmate", "evergreen": "false", "fruit": "samara"
        }
    },
    {
        "name": "White Oak",
        "traits": {
            "habit": "tree", "leaf_type": "simple", "arrangement": "alternate",
            "margin": "lobed", "venation": "pinnate", "evergreen": "false", "fruit": "nut"
        }
    },
    {
        "name": "Eastern Redbud",
        "traits": {
            "habit": "tree", "leaf_type": "simple", "arrangement": "alternate",
            "margin": "entire", "venation": "palmate", "evergreen": "false", "fruit": "pod",
            "flower_color": "pink"
        }
    },
    {
        "name": "Flowering Dogwood",
        "traits": {
            "habit": "tree", "leaf_type": "simple", "arrangement": "opposite",
            "margin": "entire", "venation": "pinnate", "evergreen": "false", "fruit": "drupe",
            "flower_color": "white"
        }
    },
    {
        "name": "Eastern White Pine",
        "traits": {
            "habit": "tree", "leaf_type": "needle", "evergreen": "true", "fruit": "cone"
        }
    },
    {
        "name": "Eastern Redcedar",
        "traits": {
            "habit": "tree", "leaf_type": "scale", "evergreen": "true", "fruit": "cone"
        }
    },
    {
        "name": "Poison Ivy",
        "traits": {
            "habit": "vine", "leaf_type": "compound", "leaflet_count": "3",
            "arrangement": "alternate", "evergreen": "false"
        }
    },
    {
        "name": "Bush Honeysuckle",
        "traits": {
            "habit": "shrub", "leaf_type": "simple", "arrangement": "opposite",
            "margin": "entire", "evergreen": "false", "fruit": "berry"
        }
    }
]

def ask(prompt, options):
    """Ask a question; allow blank (unknown). Normalize to lowercase."""
    text = input(f"{prompt} {options if options else ''}: ").strip().lower()
    return text if text else "unknown"

def main():
    print("Plant ID (rule-based). Press Enter to skip any question.\n")

    # --- user inputs (kept to the rubric’s spirit: input() + if/elif) ---
    habit         = ask("Is it a tree, shrub, or vine?", "[tree/shrub/vine]")
    leaf_type     = ask("Leaf type?", "[simple/compound/needle/scale]")
    arrangement   = ask("Leaf arrangement?", "[opposite/alternate/whorled]")
    margin        = ask("Leaf margin?", "[entire/serrated/lobed]")
    venation      = ask("Leaf venation?", "[palmate/pinnate]")
    leaflet_count = ask("Leaflet count (if compound)?", "[3/5/7/>7]")
    flower_color  = ask("Flower color (if seen)?", "[white/pink/yellow/red/green/unknown]")
    fruit         = ask("Fruit/cone type (if seen)?", "[samara/pod/cone/nut/berry/drupe/unknown]")
    evergreen     = ask("Is it evergreen year-round?", "[true/false]")

    answers = {
        "habit": habit, "leaf_type": leaf_type, "arrangement": arrangement,
        "margin": margin, "venation": venation, "leaflet_count": leaflet_count,
        "flower_color": flower_color, "fruit": fruit, "evergreen": evergreen
    }

    # --- start with all species as candidates ---
    candidates = SPECIES[:]   # shallow copy
    why = []                  # explanation log (what rules fired)

    # ====== RULES (plain if/elif, each narrows the list or adds explanations) ======

    # 1) Conifer gate: needles/scale -> keep conifers, drop broadleaf; else vice-versa
    if leaf_type in ("needle", "scale"):
        before = len(candidates)
        candidates = [s for s in candidates if s["traits"].get("leaf_type") in ("needle", "scale")]
        why.append(f"Conifer gate: {before}→{len(candidates)} based on leaf_type={leaf_type}")
    elif leaf_type in ("simple", "compound"):
        before = len(candidates)
        candidates = [s for s in candidates if s["traits"].get("leaf_type") in ("simple", "compound")]
        why.append(f"Broadleaf gate: {before}→{len(candidates)} based on leaf_type={leaf_type}")

    # 2) Evergreen sanity: if user answered, enforce it
    if evergreen in ("true", "false"):
        before = len(candidates)
        candidates = [s for s in candidates if s["traits"].get("evergreen", "false") == evergreen]
        why.append(f"Evergreen rule: {before}→{len(candidates)} (evergreen={evergreen})")

    # 3) Vine special for Poison Ivy
    if habit == "vine" and leaf_type == "compound" and leaflet_count == "3":
        before = len(candidates)
        candidates = [s for s in candidates if s["name"] == "Poison Ivy"]
        why.append(f"Poison ivy pattern detected: {before}→{len(candidates)}")

    # 4) Arrangement filter (opposite vs alternate) if provided
    if arrangement in ("opposite", "alternate"):
        before = len(candidates)
        candidates = [s for s in candidates if s["traits"].get("arrangement") in ("unknown", arrangement, None) 
                      or s["traits"].get("arrangement") == arrangement]
        why.append(f"Arrangement filter: kept species with {arrangement} leaves ({before}→{len(candidates)})")

    # 5) Lobed splitter: maple vs oak (uses venation)
    if margin == "lobed" and venation in ("palmate", "pinnate"):
        before = len(candidates)
        if venation == "palmate":
            candidates = [s for s in candidates if "Maple" in s["name"]]
            why.append(f"Lobed+palmate → Maple family ({before}→{len(candidates)})")
        else:
            candidates = [s for s in candidates if "Oak" in s["name"]]
            why.append(f"Lobed+pinnate → Oak family ({before}→{len(candidates)})")

    # 6) Fruit clue
    if fruit != "unknown":
        before = len(candidates)
        if fruit == "samara":
            keep = ("Maple", "Elm")
            candidates = [s for s in candidates if any(k in s["name"] for k in keep)]
        elif fruit == "nut":
            keep = ("Oak", "Walnut", "Hickory")
            candidates = [s for s in candidates if any(k in s["name"] for k in keep)]
        elif fruit == "cone":
            keep = ("Pine", "Cedar", "Spruce")
            candidates = [s for s in candidates if any(k in s["name"] for k in keep)]
        elif fruit == "pod":
            keep = ("Redbud",)
            candidates = [s for s in candidates if any(k in s["name"] for k in keep)]
        elif fruit in ("berry", "drupe"):
            keep = ("Dogwood", "Honeysuckle")
            candidates = [s for s in candidates if any(k in s["name"] for k in keep)]
        why.append(f"Fruit clue ({fruit}): {before}→{len(candidates)}")

    # 7) Flower color clue
    if flower_color != "unknown":
        before = len(candidates)
        if flower_color == "pink":
            candidates = [s for s in candidates if "Redbud" in s["name"]]
        elif flower_color == "white":
            candidates = [s for s in candidates if "Dogwood" in s["name"] or "Honeysuckle" in s["name"]]
        why.append(f"Flower color ({flower_color}): {before}→{len(candidates)}")

    # 8) Final tidy: match any remaining provided traits exactly (light filter)
    for key, val in answers.items():
        if val != "unknown":
            before = len(candidates)
            candidates = [s for s in candidates if s["traits"].get(key, val) == val or s["traits"].get(key) is None]
            if len(candidates) != before:
                why.append(f"Exact trait match on {key}={val}: {before}→{len(candidates)}")

    # --- Results ---
    print("\nExplanation (rules fired):")
    for line in why:
        print(" -", line)

    print("\nLikely matches:")
    if not candidates:
        print("  No strong match. Try providing fruit type, leaflet count, or venation.")
    else:
        for s in candidates[:5]:
            print("  •", s["name"])

        if len(candidates) > 1:
            print("\nClose call? Check tie-breakers: fruit type, leaflet count, lobe depth, bark texture.")

if __name__ == "__main__":
    main()
