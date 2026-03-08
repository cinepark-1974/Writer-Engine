SYSTEM_PROMPT = """
You are BLUE JEANS WRITER ENGINE.

You are a high-level screenplay writing engine for a professional writer-producer.
Your job is not to produce empty volume. Your job is to turn development material into dramatically effective, cinematic screenplay writing.

CORE PRINCIPLES
1. Every scene must have a dramatic function.
2. Every scene must move plot, character, relationship, emotion, theme, or genre effect.
3. Dialogue must contain tension, desire, concealment, conflict, reversal, irony, or subtext.
4. Avoid empty exposition and generic lines.
5. Character voices must remain distinct.
6. Genre must create actual audience effect, not surface labeling.
7. The ending direction must be protected from early stages.
8. No purposeless scenes.
9. No fake sophistication.
10. Every evaluation score must use a 10-point scale only.

VISIBLE WRITING STRUCTURE
- Input
- Write
- Polish
- QC

INVISIBLE STORY CONTROL
- 3-act structure
- 16-beat progression
- character arc
- hero journey when relevant
- genre rule pack
- theme/message control
- ending payoff control
- nonsense filter

GENRE EFFECT RULES
- Comedy must be funny through situation, contradiction, escalation, timing, character flaw, and status play.
- Thriller must create pressure, uncertainty, dread, forward momentum, and asymmetry of information.
- Melodrama/Romance must create longing, ache, emotional asymmetry, restraint, and payoff.
- Horror must create anticipation, dread, violation of safety, and memorable unease.
- Action must create tactical clarity, consequence, escalation, and emotional stake.

ENDING RULES
- The ending must feel earned.
- The protagonist transformation must be visible through action.
- The final image must leave a residue.
- Major setups should be paid off.
- The ending should be emotionally precise, not vague.

SAFETY RULES
- Fictional depictions of crime, murder, drugs, terrorism, violence, or explosions may appear when narratively justified.
- Do not provide operational real-world instructions, tactical procedures, step-by-step harmful guidance, or highly actionable details.
- Avoid gratuitous gore unless specifically required by the user's story purpose.
"""


def _clean(text: str) -> str:
    return (text or "").strip()


def build_input_summary_prompt(
    title: str,
    genre: str,
    format_type: str,
    logline: str,
    project_intent: str,
    gns: str,
    characters: str,
    world_build: str,
    structure: str,
    scene_design: str,
    treatment: str,
    tone_document: str,
) -> str:
    return f"""
[MODE]
Input Summary

[PROJECT]
Title: {_clean(title)}
Genre: {_clean(genre)}
Format: {_clean(format_type)}

[LOG LINE]
{_clean(logline)}

[PROJECT INTENT]
{_clean(project_intent)}

[GOAL / NEED / STRATEGY]
{_clean(gns)}

[CHARACTER]
{_clean(characters)}

[WORLD BUILD]
{_clean(world_build)}

[STRUCTURE]
{_clean(structure)}

[SCENE DESIGN]
{_clean(scene_design)}

[TREATMENT]
{_clean(treatment)}

[TONE DOCUMENT]
{_clean(tone_document)}

[TASK]
Read the pasted development materials and reorganize them into a concise screenplay development summary.

[REQUIREMENTS]
- Preserve the original project identity.
- Identify what is already strong.
- Identify what is still missing.
- Clarify dramatic engine, character engine, genre engine, and ending direction.
- Keep the summary practical for the next writing step.

[OUTPUT]
1. Project Core
2. Dramatic Engine
3. Character Engine
4. Genre Engine
5. Ending Direction
6. Missing / Weak Points
"""


def build_story_matrix_prompt(
    title: str,
    genre: str,
    format_type: str,
    logline: str,
    theme: str,
    gns: str,
    characters: str,
    structure: str,
    treatment: str,
) -> str:
    return f"""
[MODE]
Story Matrix

[PROJECT]
Title: {_clean(title)}
Genre: {_clean(genre)}
Format: {_clean(format_type)}

[LOG LINE]
{_clean(logline)}

[THEME]
{_clean(theme)}

[GOAL / NEED / STRATEGY]
{_clean(gns)}

[CHARACTER]
{_clean(characters)}

[STRUCTURE]
{_clean(structure)}

[TREATMENT]
{_clean(treatment)}

[TASK]
Build the internal story matrix for this project.

[INCLUDE]
- 3-act structure
- 16-beat progression
- protagonist arc
- hero journey relevance
- genre rule pack
- theme/message control
- ending payoff logic
- nonsense filter risks

[SCORING RULE]
Every evaluation score must use 10-point scale only.

[OUTPUT]
1. Core Story Engine
2. 3-Act Control Map
3. 16-Beat Control Map
4. Character Arc Map
5. Genre Effect Control
6. Theme / Message Control
7. Ending Payoff Logic
8. Nonsense Risks
"""


def build_scene_draft_prompt(
    title: str,
    genre: str,
    format_type: str,
    logline: str,
    characters: str,
    structure: str,
    scene_design: str,
    treatment: str,
    tone_document: str,
    target_scene: str,
) -> str:
    return f"""
[MODE]
Scene Draft

[PROJECT]
Title: {_clean(title)}
Genre: {_clean(genre)}
Format: {_clean(format_type)}

[LOG LINE]
{_clean(logline)}

[CHARACTER]
{_clean(characters)}

[STRUCTURE]
{_clean(structure)}

[SCENE DESIGN]
{_clean(scene_design)}

[TREATMENT]
{_clean(treatment)}

[TONE DOCUMENT]
{_clean(tone_document)}

[TARGET SCENE / REQUEST]
{_clean(target_scene)}

[TASK]
Write the requested scene or scene block in screenplay form.

[REQUIREMENTS]
- Write cinematically.
- Every scene must have a function.
- Every scene must move plot, character, relationship, emotion, theme, or genre effect.
- Dialogue must avoid empty exposition.
- Character voices must remain distinct.
- Protect the ending direction without making it obvious.
- Avoid purposeless lines and dead scenes.

[OUTPUT]
1. Screenplay Draft
2. Scene Function Summary
3. Risks / Weak Points
4. Next Scene Hook
"""


def build_section_screenplay_prompt(
    title: str,
    genre: str,
    act_label: str,
    unit_no: int,
    section_no: int,
    section_goal: str,
    previous_context: str,
    character_notes: str,
    tone_notes: str,
    genre_rule: str,
    theme_line: str,
    ending_line: str,
) -> str:
    return f"""
[MODE]
Section Draft

[PROJECT]
Title: {_clean(title)}
Genre: {_clean(genre)}
Act: {_clean(act_label)}
Unit: {unit_no}
Section: {section_no}

[SECTION GOAL]
{_clean(section_goal)}

[PREVIOUS CONTEXT]
{_clean(previous_context)}

[CHARACTER NOTES]
{_clean(character_notes)}

[TONE NOTES]
{_clean(tone_notes)}

[GENRE RULE]
{_clean(genre_rule)}

[THEME LINE]
{_clean(theme_line)}

[ENDING LINE]
{_clean(ending_line)}

[TASK]
Write this section in screenplay form.

[REQUIREMENTS]
- Write cinematically.
- Use clear scene writing.
- Every scene must have a function.
- Every scene must move plot, character, relationship, emotion, theme, or genre effect.
- Dialogue must avoid empty exposition.
- Dialogue must contain subtext or tension when possible.
- Character voices must remain distinct.
- Protect the ending direction without making it obvious.
- Avoid purposeless lines and dead scenes.

[OUTPUT FORMAT]
Act -> Unit -> Section -> Scene

[ADDITIONAL INSTRUCTION]
After the screenplay section, include:
1. Section Function Summary
2. Risks / Weak Points
3. Next Section Hook
"""


def build_dialogue_polish_prompt(
    genre: str,
    character_voice_notes: str,
    scene_text: str,
) -> str:
    return f"""
[MODE]
Dialogue Polish

[GENRE]
{_clean(genre)}

[CHARACTER VOICE NOTES]
{_clean(character_voice_notes)}

[SCENE TEXT]
{_clean(scene_text)}

[TASK]
Polish the dialogue only.

[REQUIREMENTS]
- Increase subtext.
- Reduce exposition.
- Preserve the strengths of the current material.
- Keep voices distinct.
- Add tension, wit, restraint, or irony where appropriate.
- Avoid generic lines.
- Keep it performable and cinematic.

[OUTPUT]
1. Polished Dialogue Scene
2. Brief Notes on What Improved
"""


def build_structure_polish_prompt(
    genre: str,
    logline: str,
    structure_text: str,
    treatment_text: str,
) -> str:
    return f"""
[MODE]
Structure Polish

[GENRE]
{_clean(genre)}

[LOG LINE]
{_clean(logline)}

[STRUCTURE]
{_clean(structure_text)}

[TREATMENT]
{_clean(treatment_text)}

[TASK]
Tighten and improve the structure without changing the core identity of the project.

[REQUIREMENTS]
- Strengthen causality.
- Strengthen turning points.
- Improve midpoint, all is lost, and climax logic.
- Protect character arc and ending payoff.
- Identify weak or redundant blocks.
- Keep the advice practical.

[OUTPUT]
1. Structural Diagnosis
2. Revised Structural Flow
3. Weaknesses to Fix
4. Priority Rewrite Order
"""


def build_ending_control_prompt(
    title: str,
    theme: str,
    protagonist_arc: str,
    setup_payoffs: str,
    desired_emotion: str,
    ending_type: str,
) -> str:
    return f"""
[MODE]
Ending Control

[PROJECT]
Title: {_clean(title)}
Theme: {_clean(theme)}
Protagonist Arc: {_clean(protagonist_arc)}
Setup / Payoffs: {_clean(setup_payoffs)}
Desired Final Emotion: {_clean(desired_emotion)}
Ending Type: {_clean(ending_type)}

[TASK]
Design and validate the ending.

[CHECK]
- Is the ending earned?
- Is the protagonist transformation visible through action?
- Are major setups paid off?
- Is the final emotional landing correct?
- Is the final image memorable?
- Is the ending inevitable but not flat?

[SCORING RULE]
Every score must use 10-point scale only.

[OUTPUT]
1. Ending Design
2. Payoff Checklist
3. Emotional Landing Check
4. Final Image Check
5. Ending Weaknesses
6. Ending Scores (/10)
"""


def build_qc_prompt(
    genre: str,
    theme: str,
    scene_or_section_text: str,
) -> str:
    return f"""
[MODE]
Quality Control

[GENRE]
{_clean(genre)}

[THEME]
{_clean(theme)}

[TEXT TO INSPECT]
{_clean(scene_or_section_text)}

[TASK]
Evaluate the text rigorously.

[SCORING RULE]
Every score must use 10-point scale only.

[EVALUATE]
1. Structure Fit
2. Scene Function
3. Character Voice
4. Dialogue Subtext
5. Genre Pleasure
6. Emotional Shift
7. Theme Consistency
8. Originality
9. Ending Connection
10. Nonsense Risk

[ALSO IDENTIFY]
- weak scenes
- purposeless dialogue
- genre failure points
- exposition overload
- tone drift
- missing payoff
- flat or generic writing

[OUTPUT]
1. Score Table (/10)
2. Key Problems
3. Best Elements to Keep
4. Rewrite Priorities
5. Concrete Fix Suggestions
"""
