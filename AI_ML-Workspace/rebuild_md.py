import re

old_file = r'd:\CodingSpace\Hashmil_Workspace\AI_ML-Workspace\old_roadmap.txt'
new_file = r'd:\CodingSpace\Hashmil_Workspace\AI_ML-Workspace\AI_ML_Roadmap_Details.txt'

with open(old_file, 'r', encoding='utf-16') as f:
    old_content = f.read()

phases_old = old_content.split("PHASE ")[1:]
phase_data = {}

for p in phases_old:
    match = re.search(r'^(\d+):', p)
    if not match: continue
    phase_num = match.group(1)
    
    projects_match = re.search(r'PROJECTS:\n([\s\S]*?)(?:CHECKLISTS:|---|\n\n\n|$)', p)
    checklists_match = re.search(r'CHECKLISTS:\n([\s\S]*?)(?:RESOURCES:|---|\n\n\n|$)', p)
    resources_match = re.search(r'RESOURCES:\n([\s\S]*?)(?:---|\n\n\n|$)', p)
    
    projects_text = projects_match.group(1) if projects_match else ""
    checklists_text = checklists_match.group(1) if checklists_match else ""
    resources_text = resources_match.group(1) if resources_match else ""
    
    md_projects = ""
    if projects_text.strip():
        md_projects += "    - Projects\n"
        for line in projects_text.split('\n'):
            line = line.rstrip()
            if not line: continue
            if 'Beginner:' in line: md_projects += "      - Beginner\n"
            elif 'Intermediate:' in line: md_projects += "      - Intermediate\n"
            elif 'Advanced:' in line: md_projects += "      - Advanced\n"
            elif line.strip().startswith('*') or line.strip().startswith('-'):
                proj_text = line.strip()[1:].strip()
                md_projects += f"        - {proj_text}\n"
                
    md_checklists = ""
    if checklists_text.strip():
        md_checklists += "    - Checklists\n"
        for line in checklists_text.split('\n'):
            line = line.rstrip()
            if not line: continue
            stripped = line.strip()
            if stripped in ['Phase:', 'Skill:', 'Revision:', 'Interview:', 'Portfolio:']:
                md_checklists += f"      - {stripped}\n"
            elif stripped.startswith('-') and ':' in stripped:
                # E.g. "- Phase: Do X"
                parts = stripped[1:].split(':', 1)
                md_checklists += f"      - {parts[0].strip()}:\n"
                for item in parts[1].split(','):
                    if item.strip():
                        md_checklists += f"        - {item.strip()}\n"
            elif stripped.startswith('-') or stripped.startswith('*'):
                md_checklists += f"        - {stripped[1:].strip()}\n"
                
    md_resources = ""
    if resources_text.strip():
        md_resources += "    - Resources\n"
        for line in resources_text.split('\n'):
            line = line.rstrip()
            if not line: continue
            if line.strip().startswith('*') or line.strip().startswith('-'):
                md_resources += f"      - {line.strip()[1:].strip()}\n"

    phase_data[phase_num] = md_projects + md_checklists + md_resources

with open(new_file, 'r', encoding='utf-8') as f:
    new_content = f.read()

parts = re.split(r'(### PHASE \d+:)', new_content)
final_content = parts[0]
current_phase = None

for i in range(1, len(parts)):
    part = parts[i]
    if part.startswith("### PHASE"):
        match = re.search(r'### PHASE (\d+):', part)
        if match: current_phase = match.group(1)
        final_content += part
    else:
        if current_phase and current_phase in phase_data:
            clean_part = part.rstrip()
            final_content += clean_part + "\n" + phase_data[current_phase] + "\n\n  "
        else:
            final_content += part

with open(new_file, 'w', encoding='utf-8') as f:
    f.write(final_content)

print("Properly rebuilt Markdown file with Projects, Checklists, and Resources!")
