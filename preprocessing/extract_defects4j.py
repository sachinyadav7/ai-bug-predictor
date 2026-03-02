import subprocess
import json
import os
from pathlib import Path
from backend.app.core.preprocessor import CodePreprocessor # Reusing the preprocessor

PROJECTS = ['Chart', 'Cli', 'Closure', 'Codec', 'Collections', 
            'Compress', 'Csv', 'Gson', 'JacksonCore', 'JacksonDatabind',
            'JacksonXml', 'Jsoup', 'Lang', 'Math', 'Mockito', 'Time']

def extract_bug_pairs(project):
    """Extract buggy and fixed versions for each bug"""
    # Placeholder for getting bug IDs (would need defects4j command availability)
    bugs = get_bug_ids(project) 
    pairs = []
    
    for bug_id in bugs:
        # Checkout buggy version
        buggy_dir = f"/tmp/{project}_{bug_id}_buggy"
        fixed_dir = f"/tmp/{project}_{bug_id}_fixed"
        
        # Commands require Defects4J specific environment
        try:
            subprocess.run([
                'defects4j', 'checkout', 
                '-p', project, 
                '-v', f"{bug_id}b",  # 'b' = buggy
                '-w', buggy_dir
            ], check=True)
            
            subprocess.run([
                'defects4j', 'checkout',
                '-p', project,
                '-v', f"{bug_id}f",  # 'f' = fixed
                '-w', fixed_dir
            ], check=True)
            
            # Get modified files
            modified_files = get_modified_files(project, bug_id)
            
            preprocessor = CodePreprocessor('java')

            for file_path in modified_files:
                buggy_code = preprocessor.extract_functions((Path(buggy_dir) / file_path).read_text())
                fixed_code = preprocessor.extract_functions((Path(fixed_dir) / file_path).read_text())
                
                # Match functions before/after
                pairs.extend(match_functions(buggy_code, fixed_code, project, bug_id))
                
        except Exception as e:
            print(f"Error processing {project} bug {bug_id}: {e}")
    
    return pairs

def get_bug_ids(project):
    # Dummy implementation - in real usage, query defects4j
    return range(1, 4) # Assuming first 3 bugs

def get_modified_files(project, bug_id):
    # Dummy implementation - would parse defects4j query -p project -q -f ...
    return [] 

def match_functions(buggy_funcs, fixed_funcs, project, bug_id):
    """Match functions by name to create labeled pairs"""
    pairs = []
    fixed_names = {f['name']: f for f in fixed_funcs}
    
    for buggy in buggy_funcs:
        name = buggy['name']
        if name in fixed_names:
            fixed = fixed_names[name]
            if buggy['code'] != fixed['code']:  # Actually changed
                pairs.append({
                    'project': project,
                    'bug_id': bug_id,
                    'function_name': name,
                    'buggy_code': buggy['code'],
                    'fixed_code': fixed['code'],
                    'label': 1,  # Buggy
                    'language': 'java',
                    'source': 'defects4j'
                })
                # Add the fixed version as negative sample
                pairs.append({
                    'project': project,
                    'bug_id': bug_id,
                    'function_name': name,
                    'buggy_code': fixed['code'],  # The clean version
                    'fixed_code': fixed['code'],
                    'label': 0,  # Clean
                    'language': 'java',
                    'source': 'defects4j'
                })
    
    return pairs

if __name__ == "__main__":
    # Run extraction
    all_data = []
    for project in PROJECTS:
        print(f"Processing {project}...")
        pairs = extract_bug_pairs(project)
        all_data.extend(pairs)

    # Save
    with open('data/defects4j_pairs.jsonl', 'w') as f:
        for item in all_data:
            f.write(json.dumps(item) + '\n')
