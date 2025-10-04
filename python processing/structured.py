import os
import re
import pandas as pd

# Patterns to detect any heading including 'المادة' (for rules)
rule_pattern = re.compile(r"\bالمادة\b", re.IGNORECASE)
# Patterns to detect decisions ('مرسوم ملكي', 'قرار مجلس الوزراء') anywhere in heading
decision_pattern = re.compile(r"\b(مرسوم\s+ملكي|قرار\s+مجلس\s+الوزراء)\b", re.IGNORECASE)


def extract_sections(md_text):
    """
    Split markdown into a preamble and list of sections with headings ##–######.
    Returns (preamble, [{level, title, text}, ...]).
    """
    heading_pattern = re.compile(r'^(#{2,6})\s*(.+)$', re.MULTILINE)
    matches = list(heading_pattern.finditer(md_text))
    if matches:
        preamble = md_text[:matches[0].start()].strip()
    else:
        return md_text.strip(), []

    sections = []
    for idx, m in enumerate(matches):
        level = len(m.group(1))
        title = m.group(2).strip()
        start = m.end()
        end = matches[idx+1].start() if idx+1 < len(matches) else len(md_text)
        body = md_text[start:end].strip()
        sections.append({'level': level, 'title': title, 'text': body})
    return preamble, sections


def main():
    md_folder = 'law_documents'
    csv_path = 'saudi_laws.csv'
    out_dir = 'folder'
    os.makedirs(out_dir, exist_ok=True)

    # Load title→URL mapping
    df_titles = pd.read_csv(csv_path, engine='python')
    df_titles.columns = [c.strip().lower().replace("\ufeff", "") for c in df_titles.columns]
    title_to_url = dict(zip(df_titles['title'], df_titles['url']))

    rule_rows = []
    decision_rows = []
    unstructured_rows = []

    for fname in os.listdir(md_folder):
        if not fname.lower().endswith('.md'):
            continue
        law_key = os.path.splitext(fname)[0]
        url = title_to_url.get(law_key, '')
        path = os.path.join(md_folder, fname)
        with open(path, 'r', encoding='utf-8') as f:
            text = f.read()

        preamble, sections = extract_sections(text)
        # always capture preamble as unstructured if exists
        if preamble:
            unstructured_rows.append({
                'law_title': law_key,
                'url': url,
                'heading': None,
                'level': None,
                'text': preamble
            })

        # process sections
        for sec in sections:
            title = sec['title']
            body = sec['text']
            level = sec['level']

            if rule_pattern.search(title):
                rule_rows.append({
                    'law_title': law_key,
                    'url': url,
                    'rule': title,
                    'text': body
                })
            elif decision_pattern.search(title):
                decision_rows.append({
                    'law_title': law_key,
                    'url': url,
                    'decision': title,
                    'text': body
                })
            else:
                unstructured_rows.append({
                    'law_title': law_key,
                    'url': url,
                    'heading': title,
                    'level': level,
                    'text': body
                })

    # Build DataFrames and dedupe
    df_rules = pd.DataFrame(rule_rows).drop_duplicates().reset_index(drop=True)
    df_decisions = pd.DataFrame(decision_rows).drop_duplicates().reset_index(drop=True)
    df_un = pd.DataFrame(unstructured_rows).drop_duplicates().reset_index(drop=True)

    # Save minimal columns with UTF-8 BOM for Excel compatibility
    df_rules[['law_title', 'url', 'rule', 'text']].to_csv(
        os.path.join(out_dir, 'articles_laws.csv'), index=False, encoding='utf-8-sig')
    df_decisions[['law_title', 'url', 'decision', 'text']].to_csv(
        os.path.join(out_dir, 'decisions_laws.csv'), index=False, encoding='utf-8-sig')
    df_un.to_csv(
        os.path.join(out_dir, 'unstructured_laws.csv'), index=False, encoding='utf-8-sig')


if __name__ == '__main__':
    main()
