import os
import sqlite3

def check_proj_db(path):
    if not os.path.exists(path):
        return None
    try:
        conn = sqlite3.connect(path)
        cursor = conn.cursor()
        cursor.execute("SELECT value FROM metadata WHERE key = 'DATABASE.LAYOUT.VERSION.MINOR'")
        row = cursor.fetchone()
        conn.close()
        return row[0] if row else "Unknown"
    except Exception as e:
        return f"Error: {e}"

def find_proj_dbs():
    print("Searching for proj.db files...")
    search_paths = [
        os.path.join(os.environ['USERPROFILE'], 'AppData', 'Roaming', 'Python'),
        os.path.join(os.environ['USERPROFILE'], 'AppData', 'Local', 'Programs', 'Python'),
        r"C:\Program Files",
    ]
    
    found = []
    for root_search in search_paths:
        if not os.path.exists(root_search):
            continue
        print(f"Checking {root_search}...")
        for root, dirs, files in os.walk(root_search):
            if 'proj.db' in files:
                path = os.path.join(root, 'proj.db')
                version = check_proj_db(path)
                found.append((path, version))
                print(f"Found: {path} (Minor Version: {version})")
    return found

if __name__ == "__main__":
    results = find_proj_dbs()
    print("\nSummary of found proj.db files:")
    for path, version in results:
        print(f"{version} : {path}")
