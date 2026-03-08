import subprocess

def find_large_files():
    # Get all objects
    objects_output = subprocess.check_output(['git', 'rev-list', '--objects', '--all']).decode('utf-8')
    object_map = {}
    for line in objects_output.splitlines():
        parts = line.split(maxsplit=1)
        if len(parts) == 2:
            object_map[parts[0]] = parts[1]
            
    # Get object sizes
    batch_input = '\n'.join(object_map.keys()) + '\n'
    cat_output = subprocess.check_output(
        ['git', 'cat-file', '--batch-check=%(objectname) %(objecttype) %(objectsize)'],
        input=batch_input.encode('utf-8')
    ).decode('utf-8')
    
    large_files = []
    for line in cat_output.splitlines():
        parts = line.split()
        if len(parts) == 3 and parts[1] == 'blob':
            size = int(parts[2])
            if size > 50 * 1024 * 1024:  # > 50 MB
                large_files.append((size, object_map[parts[0]]))
                
    large_files.sort(reverse=True)
    for size, path in large_files:
        print(f"{size / 1024 / 1024:.2f} MB - {path}")

if __name__ == '__main__':
    find_large_files()
