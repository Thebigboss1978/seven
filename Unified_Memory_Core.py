# seVen_Engine/Engine/Unified_Memory_Core.py
# The "Hippocampus" of Seven - Universal Data Ingestion (Barcelona Data)

import os
import json
import pypdf
from pathlib import Path
from datetime import datetime

class UnifiedMemoryCore:
    def __init__(self, engine_root=None):
        if engine_root is None:
            # Assume we are in seVen_Engine/Sovereign_Backend
            self.engine_root = Path(__file__).parent
        else:
            self.engine_root = Path(engine_root)
            
        self.memory_path = self.engine_root / "Memory_Vault"
        self.barcelona_path = self.engine_root / "Barcelona_Data"
        self.archive_path = self.memory_path / "seVen_archive.json"
        
        self._ensure_paths()
        self.memory_cache = []
        self.load_memories()

    def _ensure_paths(self):
        self.memory_path.mkdir(parents=True, exist_ok=True)
        self.barcelona_path.mkdir(parents=True, exist_ok=True)
        if not self.archive_path.exists():
            with open(self.archive_path, 'w', encoding='utf-8') as f:
                json.dump([], f)

    def load_memories(self, force=False):
        """Consolidates memory from Barcelona_Data and the Archive."""
        if force:
            print("🧠 [seVen Memory] Syncing with Barcelona Data...")
        
        # 1. Load Existing Archive
        try:
            if self.archive_path.exists():
                with open(self.archive_path, 'r', encoding='utf-8') as f:
                    self.memory_cache = json.load(f)
        except Exception as e:
            print(f"⚠️ Archive load error: {e}")
            self.memory_cache = []

        # 2. Ingest Barcelona Data (Recursive Scan)
        self._ingest_barcelona()
        
        if force: print(f"🧠 [seVen Memory] System Synced. {len(self.memory_cache)} nodes alive.")
        # 📂 INGEST BARCELONA DATA
        barcelona_dir = self.engine_root / "Barcelona_Data"
        found_count = 0
        if barcelona_dir.exists():
            for file_path in barcelona_dir.rglob("*"): # Use rglob for recursive scan
                if file_path.is_file():
                    # Skip the archive itself if somehow it's in there
                    if file_path == self.archive_path: continue

                    # Check for Text/Code files
                    if file_path.suffix in ['.txt', '.py', '.js', '.html', '.md', '.css', '.ini', '.json']: # Added .json to text files
                        try:
                            content = file_path.read_text(encoding='utf-8', errors='ignore')
                            if len(content.strip()) < 10: continue
                            if self.add_memory(content, source=f"Barcelona/{file_path.name}", save=False):
                                found_count += 1
                        except Exception as e:
                            print(f"⚠️ Failed to read {file_path}: {e}")
                    
                    # 📄 PDF SUPPORT (V1.2)
                    elif file_path.suffix == '.pdf':
                        try:
                            reader = pypdf.PdfReader(str(file_path))
                            text = ""
                            for page in reader.pages:
                                text += page.extract_text() + "\n"
                            if text.strip():
                                if self.add_memory(f"[PDF_EXTRACTION]:\n{text}", source=f"Barcelona/{file_path.name}", save=False):
                                    found_count += 1
                                    print(f"✅ Ingested PDF: {file_path.name}")
                        except Exception as e:
                            print(f"⚠️ PDF Extraction failed for {file_path}: {e}")
        
        if found_count > 0:
            self._save_archive()

        if force: print(f"🧠 [seVen Memory] System Synced. {len(self.memory_cache)} nodes alive.")

    def _ingest_barcelona(self):
        """
        This function is now largely superseded by the updated load_memories.
        It's kept for potential future specific ingestion logic, but currently
        the main ingestion happens in load_memories.
        """
        # The logic for ingesting Barcelona data has been moved to load_memories
        # to ensure all data sources (archive and Barcelona) are handled in one place
        # during the initial load or forced sync.
        pass


    def add_memory(self, content, role="System", source="Direct", save=True):
        """Adds a new memory fragment if it doesn't already exist."""
        if not content: return False

        # Basic deduplication (content match)
        for mem in self.memory_cache:
            if mem['content'] == content:
                return False

        fragment = {
            "timestamp": datetime.now().isoformat(),
            "role": role,
            "content": content,
            "source": source
        }
        self.memory_cache.append(fragment)
        if save: self._save_archive()
        return True

    def _save_archive(self):
        try:
            with open(self.archive_path, 'w', encoding='utf-8') as f:
                json.dump(self.memory_cache, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"⚠️ Save Failed: {e}")

    def search(self, query, limit=5):
        """Keyword search (most recent first)."""
        if not query: return []
        query = query.lower().strip()
        hits = []
        for mem in reversed(self.memory_cache): 
            if query in mem['content'].lower():
                hits.append(mem)
                if len(hits) >= limit: break
        return hits

    def get_recent_context(self, limit=10):
        return self.memory_cache[-limit:]

# Singleton for the engine
core = UnifiedMemoryCore()
