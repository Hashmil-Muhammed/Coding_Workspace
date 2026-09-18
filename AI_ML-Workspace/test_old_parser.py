import re
import json
import codecs

with codecs.open("old_roadmap.txt", "r", encoding="utf-16") as f:
    text = f.read()

phases_raw = re.split(r'(?=^PHASE \d+:)', text, flags=re.MULTILINE)
if len(phases_raw) <= 1:
    phases_raw = re.split(r'(?=^### PHASE \d+:)', text, flags=re.MULTILINE)

roadmap_data = []

for phase_raw in phases_raw:
    if not phase_raw.strip().startswith('PHASE') and not phase_raw.strip().startswith('### PHASE'):
        continue
        
    lines = phase_raw.split('\n')
    header_line = lines[0].strip()
    match = re.search(r'PHASE \d+:\s*(.*)', header_line)
    if not match: continue
    
    title = match.group(1).strip()
    phase_id = header_line.split(':')[0].replace('### ', '').strip()
    
    # Extract overview
    overview_match = re.search(r'Overview:\s*(.*?)(?=\n\n|\nSKILLS:)', phase_raw, re.DOTALL)
    overview_text = overview_match.group(1).strip() if overview_match else ""
    duration = ""
    duration_match = re.search(r'\(Duration:\s*(.*?)\)', overview_text)
    if duration_match:
        duration = duration_match.group(1)
        overview_text = overview_text.replace(duration_match.group(0), "").strip()

    current_phase = {
        "phase": phase_id,
        "title": title,
        "overview": {
            "why": overview_text,
            "duration": duration
        },
        "skills": [],
        "projects": {
            "beginner": [],
            "intermediate": [],
            "advanced": []
        },
        "checklists": {
            "phase": [],
            "skill": [],
            "revision": [],
            "interview": [],
            "portfolio": []
        },
        "resources": []
    }
    
    # Extract SKILLS block
    skills_match = re.search(r'SKILLS:\n([\s\S]*?)(?=PROJECTS:|CHECKLISTS:|RESOURCES:|\Z)', phase_raw)
    if skills_match:
        skills_text = skills_match.group(1)
        
        current_main_skill = None
        current_sub_skill = None
        
        for line in skills_text.split('\n'):
            stripped = line.strip()
            if not stripped: continue
            
            # 1. Main skill
            if re.match(r'^\d+\.\s', stripped):
                skill_name = re.sub(r'^\d+\.\s*', '', stripped)
                current_main_skill = {"name": skill_name, "children": []}
                current_phase["skills"].append(current_main_skill)
                current_sub_skill = None
            
            # A) Sub skill
            elif re.match(r'^[A-Z]\)\s', stripped):
                sub_name = re.sub(r'^[A-Z]\)\s*', '', stripped).rstrip(':').strip()
                current_sub_skill = {"name": sub_name, "children": []}
                if current_main_skill:
                    current_main_skill["children"].append(current_sub_skill)
                else:
                    # Fallback if no main skill
                    current_main_skill = {"name": "General", "children": [current_sub_skill]}
                    current_phase["skills"].append(current_main_skill)
            
            # * Leaf node
            elif stripped.startswith('*'):
                leaf_name = stripped[1:].strip()
                if current_sub_skill:
                    current_sub_skill["children"].append(leaf_name)
                elif current_main_skill:
                    current_main_skill["children"].append(leaf_name)
                else:
                    current_phase["skills"].append(leaf_name)

    # Extract PROJECTS block
    projects_match = re.search(r'PROJECTS:\n([\s\S]*?)(?=CHECKLISTS:|RESOURCES:|\Z)', phase_raw)
    if projects_match:
        current_tier = None
        for line in projects_match.group(1).split('\n'):
            stripped = line.strip()
            if not stripped: continue
            
            if "Beginner:" in stripped: current_tier = "beginner"
            elif "Intermediate:" in stripped: current_tier = "intermediate"
            elif "Advanced:" in stripped: current_tier = "advanced"
            elif stripped.startswith('-') or stripped.startswith('*'):
                proj_text = stripped[1:].strip()
                # Parse uses
                name = proj_text
                uses = []
                u_match = re.search(r'\(Uses:\s*(.*?)\)', proj_text)
                if u_match:
                    name = proj_text.replace(u_match.group(0), "").strip()
                    uses = [u.strip() for u in u_match.group(1).split(',')]
                
                if current_tier:
                    current_phase["projects"][current_tier].append({
                        "name": name,
                        "uses": uses
                    })

    # Extract CHECKLISTS block
    checklists_match = re.search(r'CHECKLISTS:\n([\s\S]*?)(?=RESOURCES:|\Z)', phase_raw)
    if checklists_match:
        current_cat = "phase"
        for line in checklists_match.group(1).split('\n'):
            stripped = line.strip()
            if not stripped: continue
            
            cat_match = re.match(r'^(Phase|Skill|Revision|Interview|Portfolio):', stripped, re.IGNORECASE)
            if cat_match:
                current_cat = cat_match.group(1).lower()
                
                # Check for inline checklists e.g. "Phase: Do X, Do Y"
                inline = stripped.replace(cat_match.group(0), "").strip()
                if inline and inline != "-" and not inline.startswith("-"):
                    current_phase["checklists"][current_cat].extend([i.strip() for i in inline.split(',') if i.strip()])
            elif stripped.startswith('-'):
                # Check for inline cat e.g. "- Phase: Do X"
                if ':' in stripped:
                    parts = stripped[1:].split(':', 1)
                    if parts[0].strip().lower() in current_phase["checklists"]:
                        current_cat = parts[0].strip().lower()
                        current_phase["checklists"][current_cat].extend([i.strip() for i in parts[1].split(',') if i.strip()])
                        continue
                
                current_phase["checklists"][current_cat].append(stripped[1:].strip())

    # Extract RESOURCES block
    resources_match = re.search(r'RESOURCES:\n([\s\S]*?)(?=\Z)', phase_raw)
    if resources_match:
        for line in resources_match.group(1).split('\n'):
            stripped = line.strip()
            if not stripped: continue
            if stripped.startswith('*') or stripped.startswith('-'):
                r_text = stripped[1:].strip()
                parts = r_text.split(':', 1)
                if len(parts) == 2 and 'http' in parts[1]:
                    current_phase["resources"].append({
                        "name": parts[0].strip(),
                        "link": parts[1].strip()
                    })
                else:
                    current_phase["resources"].append({
                        "name": r_text,
                        "link": "#"
                    })

    roadmap_data.append(current_phase)

print(f"Extracted {len(roadmap_data)} phases.")
print(json.dumps(roadmap_data[0], indent=2))
