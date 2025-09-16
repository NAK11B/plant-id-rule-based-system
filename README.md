# plant-id-rule-based-system
Rule-based AI system for identifying plants, trees, and shrubs.

Part 1: Prompting the AI for Project Ideas
Begin by asking an AI assistant (e.g., ChatGPT) to suggest ideas for rule-based systems. Use a prompt similar to this:
"I am working on a Python project to create a simple AI system based on rules or heuristics. This is for an assignment where I need to understand how AI worked before machine learning. Could you suggest some project ideas for a rule-based AI system? Please include examples like chatbots, recommendation systems, or diagnostic tools."
•	Write down at least three project ideas suggested by the AI.
•	For each idea, briefly describe:
o	What the system does (e.g., a chatbot for restaurant recommendations).

o	How it would work using rules (e.g., predefined responses based on keywords).
•	Select the project idea that most interests you and provide a 2-3 sentence justification for your choice.

•	Project Idea #1: Rule-Based Chatbot for Restaurant Recommendations
What it does: A chatbot that suggests restaurants based on user preferences (e.g., cuisine type, price range, or location).
How it works using rules: The system uses if/then logic. For example: If cuisine = “Italian” and budget = “low,” then recommend local pizza places. The rules map user responses to a list of restaurant categories.

•	Project Idea #2: Rule-Based Troubleshooting Assistant (Tech Support)
What it does: A simple assistant that helps users troubleshoot common computer or phone issues (e.g., Wi-Fi not working, screen frozen).
How it works using rules: The system follows a decision tree. For example: If Wi-Fi issue = “can’t connect” and router lights = off, then suggest “check power.” If router lights = on but no internet, then suggest “restart router.”

•	Project Idea #3: Rule-Based Plant/Tree/Shrub Identifier
What it does: Helps users identify plants, trees, or shrubs based on visible traits (leaf shape, arrangement, bark type, etc.).
How it works using rules: The system uses logical rules to eliminate or rank species. For example: If leaf type = needle and evergreen = true, then suggest Pine or Cedar. Users answer trait questions, and the system narrows down possible matches.
Selected Project: Plant/Tree/Shrub Identifier

I chose the plant/tree/shrub identifier because it’s a practical and unique application of rule-based AI. It mirrors how botanists use field guides and dichotomous keys, making it a perfect example of pre–machine learning AI. It also feels useful and interesting — something people could actually use in their daily lives when exploring nature.


Part 2: Designing Your Rule-Based System
Once you’ve chosen your project idea, prompt the AI to help you design the rules or heuristics for the system. Use a prompt like this:
"I want to create a [insert your system idea here]. The system will be rule-based. Can you help me outline the rules and logic needed to make this work? For example, what conditions or keywords should I check for, and what responses or actions should my system take?"
•	Write down the rules and logic suggested by the AI.
•	Organize the rules into a clear list (e.g., IF-THEN statements or pseudocode).

Prompted Design (Plant/Tree/Shrub Identifier — Rule-Based)
Conditions / “keywords” to check (user inputs):
•	habit: tree | shrub | vine
•	leaf_type: simple | compound | needle | scale
•	arrangement: opposite | alternate | whorled
•	margin: entire | serrated | lobed
•	venation: palmate | pinnate
•	lobes: none | shallow | deep
•	leaflet_count: 3 | 5 | 7 | >7 (if compound)
•	flower_color: white | pink | yellow | red | green | none/unknown
•	fruit: samara | pod | cone | nut | berry | drupe | none/unknown
•	evergreen: true | false
•	seasonal_clue: spring_blooms | fall_red | evergreen | none
Rules / logic (IF–THEN):
1.	Conifer gate:
o	IF leaf_type ∈ {needle, scale} THEN boost conifers; penalize broadleaf species.
o	IF leaf_type ∈ {simple, compound} THEN penalize conifers.
2.	Evergreen sanity:
o	IF evergreen = true THEN boost pines/cedars; ELSE penalize them.
3.	Vine special:
o	IF habit = vine AND leaf_type = compound AND leaflet_count = 3
THEN heavy-boost Poison Ivy; penalize others.
4.	Lobed splitter (family ID):
o	IF margin = lobed AND venation = palmate THEN boost Maples, penalize Oaks.
o	IF margin = lobed AND venation = pinnate THEN boost Oaks, penalize Maples.
5.	Opposite arrangement families:
o	IF arrangement = opposite THEN boost {Maple, Ash, Dogwood, Honeysuckle}; penalize alternates.
6.	Fruit clues:
o	IF fruit = samara → boost Maple/Elm.
o	IF fruit = nut → boost Oak/Hickory/Walnut.
o	IF fruit = cone → boost Pine/Cedar/Spruce.
o	IF fruit = pod → boost Redbud/legumes.
o	IF fruit = drupe or berry → boost Dogwood/Honeysuckle (and any others you include).
7.	Exact-match bonus:
o	For every trait where user_value == species_value, add +1.
o	Strong contradictions (e.g., needles vs broadleaf) get small penalties (−1/−2).
Actions / responses:
•	Compute a score per species (sum of rule contributions).
•	Return Top 3 candidates with explanations (which rules fired + matched traits).
•	If the top two scores are close (≤2 points), ask a tie-breaker question targeting the trait with the most disagreement (e.g., fruit type, leaflet count, lobe depth, bark).
•	Show a short “What to check next” tip list to guide the user.


Part 3: Coding Your Rule-Based System
Now it’s time to implement the system. Use the AI to assist with writing and debugging the Python code. Here’s an example of an initial prompt:
"I need help writing Python code for a rule-based system. The system I want to build is a [insert your project idea here], and here are the rules I’ve outlined: [list your rules]. Could you help me write the Python code for this?"
As you interact with the AI:
•	Collaboratively build the code.
•	Refine the code based on feedback or errors encountered.
•	Ensure the AI helps you understand the code and its functionality.
Requirements for Your Code:
1.	The system should include:
•	User input (e.g., input() function).
•	Rule-based decision-making using conditionals (if-elif-else statements).
•	Outputs based on the rules (e.g., text responses or recommendations).
2.	Include comments explaining how the rules are implemented.
3.	Test the system with multiple user inputs to ensure it works as intended.

   
Input 1 
Is it a tree, shrub, or vine? vine  
Leaf type? simple  
Leaf arrangement? whorled  
Leaf margin? lobed  
Leaf venation? pinnate  
Leaflet count? 7  
Flower color? green  
Fruit/cone type? pod  
Is it evergreen? false  

Explanation (rules fired):  
- Broadleaf gate: 8→6 based on leaf_type=simple  
- Fruit clue (pod): 1→0  
- Evergreen rule: 2→0 (evergreen=false)  
- Lobed+pinnate → Oak family (6→1)  
- Flower color (green): 0→0  

Likely matches:  
No strong match. Try providing fruit type, leaflet count, or venation.


Input 2
 Is it a tree, shrub, or vine? tree  
Leaf type? needle  
Leaf arrangement? opposite  
Leaf margin? entire  
Leaf venation? palmate  
Leaflet count? 3  
Flower color? yellow  
Fruit/cone type? cone  
Is it evergreen? false  

Explanation (rules fired):  
- Conifer gate: 8→2 based on leaf_type=needle  
- Evergreen rule: 2→0 (evergreen=false)  
- Arrangement filter: kept species with opposite leaves (0→0)  
- Fruit clue (cone): 0→0  
- Flower color (yellow): 0→0  

Likely matches:  
No strong match. Try providing fruit type, leaflet count, or venation.


Input 3
 Is it a tree, shrub, or vine? shrub  
Leaf type? compound  
Leaf arrangement? alternate  
Leaf margin? entire  
Leaf venation? pinnate  
Leaflet count? 7  
Flower color? red  
Fruit/cone type? berry  
Is it evergreen? true  

Explanation (rules fired):  
- Broadleaf gate: 8→6 based on leaf_type=compound  
- Evergreen rule: 6→0 (evergreen=true)  
- Arrangement filter: kept species with alternate leaves (0→0)  
- Fruit clue (berry): 0→0  
- Flower color (red): 0→0  

Likely matches:  
No strong match. Try providing fruit type, leaflet count, or venation.


Part 4: Reflection and Submission
Write a brief reflection (around 300 words) addressing the following:
1.	How does your rule-based system work?
2.	What challenges did you encounter while prompting the AI to assist with the design and code?
3.	Reflection

  My rule-based system is designed to identify plants, trees, or shrubs based on a series of questions about their visible features. When a user runs the program, it asks them to describe characteristics such as whether the plant is a tree, shrub, or vine, what type of leaves it has, the arrangement of the leaves, margin shape, venation, and so on. Each answer is compared against a set of predefined rules stored in the system’s knowledge base. For example, if the plant has needle leaves and is evergreen, the rules increase the likelihood that it might be a pine or cedar. The system uses a scoring method where matches between the user’s input and the plant database increase the score for certain species. At the end, it outputs the top candidates along with explanations of why they matched. This mirrors the way early AI systems worked—logic written out as “if this, then that” rules, rather than relying on training data or probabilities.
  While building this project, one of the biggest challenges I faced was figuring out how to turn broad plant characteristics into usable rules. For instance, many trees share features like “lobed leaves,” but the system needs more detail—like whether the venation is palmate or pinnate—to narrow it down. Prompting the AI assistant helped me refine these rules, but I also had to adjust the code myself when outputs didn’t make sense. Another challenge was keeping the system human-readable. Since part of the assignment required comments and explanations, I had to strike a balance between writing code that worked and making sure each rule was clear to someone reading it for the first time. Overall, this project gave me a better understanding of how rule-based systems operate and why they were such an important stepping stone before modern machine learning.

