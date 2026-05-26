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
