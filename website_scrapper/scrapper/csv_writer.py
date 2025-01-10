import csv
from typing import List, Dict
import pandas as pd

class CSVWriter:
    def __init__(self, file_path: str):
        self.file_path = file_path

    def save_to_csv(self, data: List[Dict[str, any]]):
        rows = []
        for entry in data:
            rows.append({
                "Header": entry['heading'],
                "Text": "\n".join(entry['text']),
                "Links": "\n".join(entry['links'])
            })

        df = pd.DataFrame(rows, columns=["Header", "Text", "Links"])
        df.to_csv(self.file_path, index=False)
