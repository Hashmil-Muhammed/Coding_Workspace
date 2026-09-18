import json
import re
import traceback

def parse_markdown(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        
    roadmap_data = []
    current_phase = None
    
    # Stack stores (indentation_level, children_list_reference)
    stack = []
    
    for line in lines:
        if line.startswith('### PHASE '):
            match = re.match(r'### (PHASE \d+):\s*(.*)', line.strip())
            if match:
                current_phase = {
                    "phase": match.group(1),
                    "title": match.group(2),
                    "overview": {
                        "why": "",
                        "duration": ""
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
                roadmap_data.append(current_phase)
                stack = [(-1, current_phase["skills"])]
            continue
            
        if current_phase is not None:
            if not line.startswith(' ') and not line.startswith('-') and line.strip() and not line.startswith('###'):
                # It might be overview text
                if not current_phase["overview"]["why"]:
                    current_phase["overview"]["why"] = line.strip()
                continue
                
            stripped = line.lstrip()
            if stripped.startswith('- '):
                indent = len(line) - len(stripped)
                item_name = stripped[2:].strip()
                
                # Check for project formatting
                # But since projects aren't explicitly delimited in this markdown format, we just treat them as skills
                
                node = {
                    "name": item_name,
                    "children": []
                }
                
                # Pop the stack until we find a parent with a smaller indent
                while len(stack) > 0 and stack[-1][0] >= indent:
                    stack.pop()
                    
                if len(stack) > 0:
                    stack[-1][1].append(node)
                    stack.append((indent, node["children"]))
                else:
                    # Should not happen if stack[-1] is -1 (root)
                    pass

    # Clean up empty children arrays to keep JSON clean
    def clean_empty_children(nodes):
        for node in nodes:
            if 'children' in node and len(node['children']) == 0:
                del node['children']
            elif 'children' in node:
                clean_empty_children(node['children'])
                
    for phase in roadmap_data:
        clean_empty_children(phase["skills"])
        
    return roadmap_data

def update_html(html_path, json_data):
    with open(html_path, 'r', encoding='utf-8') as f:
        html_content = f.read()
        
    json_str = json.dumps(json_data, indent=4)
    
    # Regex to find the roadmapData array assignment
    pattern = re.compile(r'(const\s+roadmapData\s*=\s*)\[[\s\S]*?\];(\s*\/\/ UI Logic)')
    
    def replacer(match):
        return match.group(1) + json_str + ";" + match.group(2)
        
    new_html, count = pattern.subn(replacer, html_content)
    if count == 0:
        print("Could not find const roadmapData in HTML")
    else:
        with open(html_path, 'w', encoding='utf-8') as f:
            f.write(new_html)
        print("HTML updated successfully!")

if __name__ == '__main__':
    txt_path = r'd:\CodingSpace\Hashmil_Workspace\AI_ML-Workspace\AI_ML_Roadmap_Details.txt'
    html_path = r'd:\CodingSpace\Hashmil_Workspace\AI_ML-Workspace\AI-ML_Engineer_roadmap.html'
    
    data = parse_markdown(txt_path)
    print(f"Extracted {len(data)} phases.")
    update_html(html_path, data)
