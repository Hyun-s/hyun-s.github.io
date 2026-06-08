from dataclasses import dataclass, field
from typing import Optional, List

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
    images: List[str] = field(default_factory=list)
