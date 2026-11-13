from markdown.extensions.toc import slugify as markdown_slugify

from teaching_hub.slugs import ALIAS_CLASS, add_anchor_aliases, heading_ids, slugify


def test_polish_letters_keep_their_base_letter_in_heading_ids():
    assert slugify("Materiały do zajęć", "-") == "materialy-do-zajec"
    assert slugify("Łódź", "-") == "lodz"


def test_ids_without_l_stroke_stay_as_published():
    # Every other Polish letter already had its base letter, so these ids must not change.
    for text in ("Zestawy zadań", "Jak zacząć", "Treści dydaktyczne", "Czego te licencje nie obejmują", "Źrebię, żaba, ósmy"):
        assert slugify(text, "-") == markdown_slugify(text, "-"), text


def alias(anchor: str) -> str:
    return f'<span id="{anchor}" class="{ALIAS_CLASS}"></span>'


def test_heading_ids_follow_the_renderer():
    text = "# Materiały do zajęć\n\n## [Dla słuchaczy](../courses/)\n\n### Zadanie {#lab-01}\n\n## Materiały\n\n## Materiały\n"
    assert [i for _, _, i in heading_ids(text)] == ["materialy-do-zajec", "dla-sluchaczy", "lab-01", "materialy", "materialy_1"]


def test_code_blocks_and_front_matter_are_not_headings():
    text = "---\n# a YAML comment\ntitle: x\n---\n```bash\n# Materiały\n```\n\n~~~\n## Łódź\n~~~\n## Jak zacząć\n"
    assert [i for _, _, i in heading_ids(text)] == ["jak-zaczac"]


def test_alias_keeps_a_published_anchor_on_its_heading():
    text = "# Materiały do zajęć\n\nTekst.\n\n## Wykorzystywane materiały\n"
    aliases = {"materialy-do-zajec": ["materiay-do-zajec"], "wykorzystywane-materialy": ["wykorzystywane-materiay"]}
    assert add_anchor_aliases(text, aliases) == (
        f"# {alias('materiay-do-zajec')}Materiały do zajęć\n\nTekst.\n\n"
        f"## {alias('wykorzystywane-materiay')}Wykorzystywane materiały\n"
    )


def test_headings_without_aliases_are_left_alone():
    text = "## Materiały\n\n### Tytuł zadania {#lab-02}\n"
    assert add_anchor_aliases(text, {"jak-zaczac": ["old"]}) == text


def test_alias_of_a_repeated_heading_goes_to_the_right_one():
    text = "## Materiały\n\n## Materiały\n"
    assert add_anchor_aliases(text, {"materialy_1": ["materiay_1"]}) == f"## Materiały\n\n## {alias('materiay_1')}Materiały\n"
