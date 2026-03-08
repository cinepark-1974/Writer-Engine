SYSTEM_PROMPT = """
You are BLUE JEANS WRITER ENGINE.

You are a professional screenplay writing engine for a writer-producer.
Your role is to turn development material into dramatically effective screenplay writing.

CORE RULES
1. Every scene must have a dramatic function.
2. Avoid empty dialogue.
3. Preserve character voice.
4. Protect story theme.
5. Maintain genre effect.
6. Keep cinematic clarity.
7. Avoid purposeless exposition.
8. Keep endings emotionally earned.
"""


def clean(text):
    return (text or "").strip()


def build_input_summary_prompt(
    title,
    genre,
    format_type,
    logline,
    intent,
    gns,
    characters,
    world,
    structure,
    scene_design,
    treatment,
    tone,
):
    return f"""
[MODE]
Input Summary

[PROJECT]
Title: {clean(title)}
Genre: {clean(genre)}
Format: {clean(format_type)}

[LOG LINE]
{clean(logline)}

[PROJECT INTENT]
{clean(intent)}

[GOAL / NEED / STRATEGY]
{clean(gns)}

[CHARACTER]
{clean(characters)}

[WORLD BUILD]
{clean(world)}

[STRUCTURE]
{clean(structure)}

[SCENE DESIGN]
{clean(scene_design)}

[TREATMENT]
{clean(treatment)}

[TONE DOCUMENT]
{clean(tone)}

[TASK]
Read the pasted development materials and reorganize them into a practical screenplay development summary.

[OUTPUT]
1. Project Core
2. Dramatic Engine
3. Character Engine
4. Genre Engine
5. Ending Direction
6. Missing / Weak Points
"""


def build_scene_draft_prompt(
    title,
    genre,
    format_type,
    logline,
    characters,
    structure,
    scene_design,
    treatment,
    tone,
    scene_request,
):
    return f"""
[MODE]
Scene Draft

[PROJECT]
Title: {clean(title)}
Genre: {clean(genre)}
Format: {clean(format_type)}

[LOG LINE]
{clean(logline)}

[CHARACTER]
{clean(characters)}

[STRUCTURE]
{clean(structure)}

[SCENE DESIGN]
{clean(scene_design)}

[TREATMENT]
{clean(treatment)}

[TONE DOCUMENT]
{clean(tone)}

[WRITE THIS SCENE]
{clean(scene_request)}

[TASK]
Write the requested scene or scene block in screenplay style.

[REQUIREMENTS]
- Write cinematically.
- Every scene must have a function.
- Every scene must move plot, character, relationship, emotion, theme, or genre effect.
- Dialogue must avoid empty exposition.
- Character voices must remain distinct.
- Protect the ending direction without making it obvious.

[OUTPUT]
1. Screenplay Draft
2. Scene Function Summary
3. Risks / Weak Points
4. Next Scene Hook
"""


def build_dialogue_polish_prompt(
    genre,
    character_notes,
    scene_text,
):
    return f"""
[MODE]
Dialogue Polish

[GENRE]
{clean(genre)}

[CHARACTER VOICE NOTES]
{clean(character_notes)}

[SCENE TEXT]
{clean(scene_text)}

[TASK]
Rewrite the dialogue to improve subtext and character voice.

[REQUIREMENTS]
- Increase subtext.
- Reduce exposition.
- Preserve character distinction.
- Add tension, restraint, or irony where appropriate.
- Avoid generic lines.
- Keep it performable and cinematic.

[OUTPUT]
1. Polished Dialogue Scene
2. Brief Notes on What Improved
"""


def build_qc_prompt(
    genre,
    theme,
    text,
):
    return f"""
[MODE]
Quality Control

[GENRE]
{clean(genre)}

[THEME]
{clean(theme)}

[TEXT TO INSPECT]
{clean(text)}

[TASK]
Evaluate the text rigorously.

[EVALUATE]
1. Structure Fit
2. Character Voice
3. Dialogue
4. Theme
5. Genre Effect
6. Emotional Clarity
7. Weak Points
8. Rewrite Priorities

[OUTPUT]
1. Score Summary
2. Key Problems
3. Best Elements to Keep
4. Rewrite Priorities
5. Concrete Fix Suggestions
"""
