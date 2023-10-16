from dataclasses import dataclass
from datetime import datetime


@dataclass
class RegisterDateData:
    title           :str=""
    start_datetime  :datetime=None
    end_datetime    :datetime=None