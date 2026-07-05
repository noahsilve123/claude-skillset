import json, os, re, sys

ROOT = os.path.dirname(os.path.abspath(__file__))
SKILLS = os.path.join(ROOT, "skills")

try:
    import yaml  # type: ignore
    HAVE_YAML = True
except Exception:
    HAVE_YAML = False


def parse_frontmatter(text):
    m = re.match(r"^---\s*\n(.*?)\n---\s*\n", text, re.S)
    if not m:
        return {}
    block = m.group(1)
    if HAVE_YAML:
        try:
            data = yaml.safe_load(block) or {}
            if isinstance(data, dict):
                return data
        except Exception:
            pass
    # fallback: naive key: value (single line) parse
    out, key, buf = {}, None, []
    for line in block.splitlines():
        km = re.match(r"^([A-Za-z0-9_-]+):\s*(.*)$", line)
        if km:
            if key:
                out[key] = " ".join(buf).strip()
            key, buf = km.group(1), [km.group(2)]
        elif key:
            buf.append(line.strip())
    if key:
        out[key] = " ".join(buf).strip()
    return out


def clean(s):
    s = (s or "").strip().strip('"').strip("'").strip()
    s = re.sub(r"\s+", " ", s)
    return s


skills = []
for name in sorted(os.listdir(SKILLS)):
    d = os.path.join(SKILLS, name)
    sk = os.path.join(d, "SKILL.md")
    if not os.path.isdir(d) or not os.path.isfile(sk):
        continue
    with open(sk, encoding="utf-8") as f:
        fm = parse_frontmatter(f.read())
    desc = clean(fm.get("description")) or f"{name} skill."
    skills.append({
        "name": clean(fm.get("name")) or name,
        "path": f"skills/{name}/SKILL.md",
        "description": desc,
        "version": "1.0.0",
    })

index = {
    "skillset_name": "Gurta Agent Skillset",
    "description": "Curated Gamut-ready skillset for the Gurta project: official Anthropic skills, orchestration/planning (superpowers), browser + testing (playwright/puppeteer/pytest/vitest), scraping (firecrawl), RAG/embeddings (huggingface), and a custom gurta-context skill with repo conventions and safety rules.",
    "version": "2.0.0",
    "skills": skills,
}

with open(os.path.join(ROOT, "index.json"), "w", encoding="utf-8") as f:
    json.dump(index, f, indent=2, ensure_ascii=False)
    f.write("\n")

print(f"Wrote index.json with {len(skills)} skills")
for s in skills:
    print(" -", s["name"])
