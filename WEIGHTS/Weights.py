from enum import Enum  
class Weights(Enum):
    MUST_HAVE    = 0.5
    EXPERIENCE   = 0.2
    NICE_TO_HAVE = 0.15
    LOCATION     = 0.1
    FEEDBACK     = 0.01   
    AVAILABILITY = 0.04

    MUST_HAVE_PENALTY = 0.25
    EXPERIENCE_PENALTY = 0.5



