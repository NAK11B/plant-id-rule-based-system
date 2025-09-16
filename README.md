# Plant ID Rule-Based System 🌱

A rule-based AI system for identifying plants, trees, and shrubs.  
This project demonstrates how **expert systems** worked before modern machine learning by using **if–then rules** to match plant traits to possible species.

---

## 📌 Project Overview
The goal of this project was to build a simple expert system that takes user input (leaf type, arrangement, margin, fruit, etc.) and uses logical rules to suggest the most likely plant types.  

This mirrors how botanists use **field guides and dichotomous keys**, making it a perfect example of pre–machine learning AI.

---

## 💡 Project Ideas Considered
1. **Chatbot for Restaurant Recommendations**  
   - Suggests restaurants based on cuisine, budget, and location.  
   - Example rule: `IF cuisine = "Italian" AND budget = "low" → Recommend pizza places.`  

2. **Rule-Based Troubleshooting Assistant**  
   - Helps users fix computer/phone issues.  
   - Example rule: `IF wifi_issue = "can't connect" AND router_light = off → Suggest check power.`  

3. **Plant/Tree/Shrub Identifier (Chosen)**  
   - Identifies plants based on traits like leaves, bark, and fruit.  
   - Example rule: `IF leaf_type = needle AND evergreen = true → Suggest Pine or Cedar.`  

✅ I selected **Plant/Tree/Shrub Identifier** because it’s practical, unique, and closely resembles how early expert systems were applied in real-world fields.

---

## ⚙️ System Design

### Inputs (user traits checked)
- habit: tree | shrub | vine  
- leaf_type: simple | compound | needle | scale  
- arrangement: opposite | alternate | whorled  
- margin: entire | serrated | lobed  
- venation: palmate | pinnate  
- leaflet_count: 3 | 5 | 7 | >7  
- flower_color: white | pink | yellow | red | green | none  
- fruit: samara | pod | cone | nut | berry | drupe | none  
- evergreen: true | false  
- seasonal clues: spring_blooms | fall_red | evergreen  

### Rules (examples)
```text
IF leaf_type IN {needle, scale} → boost conifers, penalize broadleaf species  
IF evergreen = true → boost pines/cedars  
IF habit = vine AND leaf_type = compound AND leaflet_count = 3 → heavy boost Poison Ivy  
IF margin = lobed AND venation = palmate → boost Maples, penalize Oaks  
IF fruit = cone → boost Pine/Cedar/Spruce  

Scoring

Each matching rule increases a species’ score.

Contradictions lower the score.

Final output = Top 3 candidates with explanations.

🖥️ Example Runs
Input 1:

habit = vine
leaf_type = simple
arrangement = whorled
margin = lobed
venation = pinnate
leaflet_count = 7
flower_color = green
fruit = pod
evergreen = false
Result: No strong match. Suggested tie-breaker traits: fruit type, leaflet count, venation.

Input 2:

habit = tree
leaf_type = needle
arrangement = opposite
margin = entire
venation = palmate
leaflet_count = 3
flower_color = yellow
fruit = cone
evergreen = false
Result: No strong match. Suggested tie-breaker traits: evergreen status, leaflet count, fruit type.

Input 3:

habit = tree
leaf_type = needle
arrangement = opposite
margin = entire
venation = palmate
leaflet_count = 3
flower_color = yellow
fruit = cone
evergreen = false
Result: No strong match. Suggested tie-breaker traits: arrangement, evergreen, fruit.

📝 Reflection

My system works by applying if–then rules to user input. Each trait boosts or penalizes candidate species until a short list of likely matches remains. This mirrors how early expert systems functioned before ML.

Challenges

Translating vague plant features into strict rules.

Balancing human-readable code with accurate logic.

Refining the rules when early outputs didn’t make sense.

Lessons Learned

Rule-based systems are easy to interpret but hard to scale.

They break down when the domain has too many overlapping traits (like plants).

Still, they are excellent for teaching the foundations of AI.

🚀 Future Improvements

Add more plant species and traits.

Replace hardcoded rules with a database lookup.

