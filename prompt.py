SYSTEM_PROMPT = """
You are BLUE JEANS WRITER ENGINE.

You are a professional screenplay writing engine.

Core rules:
- Every scene must have a dramatic function
- Avoid empty dialogue
- Preserve character voice
- Protect story theme
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
PROJECT
{title}

GENRE
{genre}

FORMAT
{format_type}

LOG LINE
{clean(logline)}

PROJECT INTENT
{clean(intent)}

GOAL NEED STRATEGY
{clean(gns)}

CHARACTER
{clean(characters)}

WORLD
{clean(world)}

STRUCTURE
{clean(structure)}

SCENE DESIGN
{clean(scene_design)}

TREATMENT
{clean(treatment)}

TONE
{clean(tone)}

TASK
Summarize the development material for screenplay writing.
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
PROJECT
{title}

GENRE
{genre}

LOG LINE
{clean(logline)}

CHARACTERS
{clean(characters)}

STRUCTURE
{clean(structure)}

SCENE DESIGN
{clean(scene_design)}

TREATMENT
{clean(treatment)}

TONE
{clean(tone)}

WRITE THIS SCENE
{clean(scene_request)}

TASK
Write the scene in screenplay style.
"""


def build_dialogue_polish_prompt(
    genre,
    character_notes,
    scene_text,
):
    return f"""
GENRE
{genre}

CHARACTER VOICE
{clean(character_notes)}

SCENE
{clean(scene_text)}

TASK
Rewrite the dialogue to improve subtext and character voice.
"""


def build_qc_prompt(
    genre,
    theme,
    text,
):
    return f"""
GENRE
{genre}

THEME
{clean(theme)}

TEXT
{clean(text)}

TASK
Evaluate the text.

Check:
- structure
- character voice
- dialogue
- theme
"""
