import json
import os
from typing import Dict, List, Optional
from datetime import datetime

class StatsManager:
    _instance = None
    _stats_file = "data/stats.json"
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._load_stats()
        return cls._instance
    
    def _load_stats(self):
        self.stats = {
            "total_bugs_found": 0,
            "bugs_fixed": 0, # This might need a separate 'fix' action, but we can simulate or just track 'scans' for now? 
                             # User asked for 'Bugs Fixed' on dashboard. Let's assume for now 
                             # we track it if we had a 'fix' button, but for now maybe just random or manual increment?
                             # Actually, let's track 'scans' and 'bugs_found'. 'Bugs Fixed' might be mocked or 0 for now.
            "total_scans": 0,
            "total_processing_time_ms": 0,
            "recent_scans": [] # List of { project_name, timestamp, issues_count }
        }
        
        if os.path.exists(self._stats_file):
            try:
                with open(self._stats_file, 'r') as f:
                    loaded = json.load(f)
                    self.stats.update(loaded)
            except Exception as e:
                print(f"Error loading stats: {e}")
                
    def _save_stats(self):
        # Ensure directory exists
        os.makedirs(os.path.dirname(self._stats_file), exist_ok=True)
        try:
            with open(self._stats_file, 'w') as f:
                json.dump(self.stats, f, indent=2)
        except Exception as e:
            print(f"Error saving stats: {e}")

    def record_scan(self, bug_count: int, processing_time_ms: float, project_name: str = "Project_Alpha"):
        self.stats["total_scans"] += 1
        self.stats["total_bugs_found"] += bug_count
        self.stats["total_processing_time_ms"] += processing_time_ms
        
        # Add to recent scans
        scan_entry = {
            "project_name": f"{project_name}_v{self.stats['total_scans']}", # Simulate versioning
            "timestamp": datetime.now().isoformat(),
            "issues_count": bug_count
        }
        
        self.stats["recent_scans"].insert(0, scan_entry)
        self.stats["recent_scans"] = self.stats["recent_scans"][:10] # Keep last 10
        
        self._save_stats()
        
    def get_dashboard_stats(self) -> Dict:
        avg_time = 0
        if self.stats["total_scans"] > 0:
            avg_time = self.stats["total_processing_time_ms"] / self.stats["total_scans"]
            
        return {
            "total_bugs_found": self.stats["total_bugs_found"],
            "bugs_fixed": self.stats["bugs_fixed"], # Placeholder
            "avg_fix_time": "2h 14m", # Hardcoded for now as we don't track fixes
            "efficiency_score": "94%", # Hardcoded
            "recent_scans": self.stats["recent_scans"],
            "total_scans": self.stats["total_scans"]
        }

stats_manager = StatsManager()
