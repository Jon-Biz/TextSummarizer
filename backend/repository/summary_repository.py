import os
from typing import List, Optional
from models import Summary
from config import DATA_DIR

class SummaryRepository:
    """Repository for handling summary file operations."""
    
    @staticmethod
    def load_all() -> List[Summary]:
        """Load all summaries from the data directory."""
        summaries = []
        for file_name in os.listdir(DATA_DIR):
            if file_name.endswith(".md"):
                summary_path = os.path.join(DATA_DIR, file_name)
                try:
                    with open(summary_path, "r") as f:
                        summary_content = f.read()
                    title = summary_content.split("\n")[0][2:]
                    content = "\n".join(summary_content.split("\n")[1:])
                    summary = Summary(
                        id=file_name.split(".")[0],
                        title=title,
                        content=content,
                    )
                    summaries.append(summary)
                except Exception as e:
                    print(f"Error loading summary {file_name}: {e}")
        return summaries

    @staticmethod
    def save(title: str, content: str, fallback_id: Optional[str] = None) -> str:
        """Save a summary to file and return the file path."""
        try:
            file_name = f"{title}.md"
            file_path = os.path.join(DATA_DIR, file_name)
            with open(file_path, "w") as f:
                f.write(f"# {title}\n\n{content}")
            return file_path
        except Exception as e:
            print(f"Error saving summary with title {title}: {e}")
            if fallback_id:
                fallback_path = os.path.join(DATA_DIR, f"summary_{fallback_id}.md")
                with open(fallback_path, "w") as f:
                    f.write(f"# {title}\n\n{content}")
                return fallback_path
            raise