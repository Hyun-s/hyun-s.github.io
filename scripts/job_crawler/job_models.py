from dataclasses import dataclass
from typing import Optional

@dataclass
class JobInfo:
    id: str
    title: str
    company: str
    description: str
    deadline: Optional[str]
    link: str
    source: str
    start_date: Optional[str] = None
    end_date: Optional[str] = None
