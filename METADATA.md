# Skill metadata contract

Every skill has a `metadata.json` with `version`, `author`, `abstract`, `categories`, `rules`, and `sections`. This file is repository catalog metadata; skill discovery uses the `SKILL.md` frontmatter. Follow the installed agent's discovery and installation conventions when distributing skills.

`sections` lists groups of separately maintained rule guides, with a `prefix`, human-readable `name`, and numeric `count`. `categories` equals the number of sections; `rules` equals the sum of section counts. These counts enumerate catalogued rule guides, not the number, quality, or importance of instructions. A skill with guidance only in `SKILL.md` or `references/` legitimately has zero counts and an empty list. References and assets are not counted as rules. For guide-based collections, a topic's `guide.md` counts as one rule; supporting references do not. For flat rule collections, each rule file can be counted under its established section. Preserve original attribution where present.

Skills may refer to other skills in this repository for specialized guidance. Distribute those companion skills together when the workflow needs them; do not assume an agent can resolve a sibling skill installed separately. Core guidance and critical safety constraints should remain in the skill that needs them. External references are supplementary and must not be required to apply a skill's essential instructions.

The Python coding standards `design` section also includes `solid-*` rule files. A section's optional `impact` describes the section as a whole; omit it when the rules have different impact levels. Rule-level impact remains in the rule file.

The repository validator accepts the current, deliberately limited frontmatter format: one unquoted, single-line scalar per top-level key. It is not a general YAML parser. Markdown links are checked for local file existence and heading anchors; templates and generated sample output are excluded because they contain intentional placeholders.
