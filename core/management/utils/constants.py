from enum import Enum


class ElectionType(Enum):
    """Enum for election types"""
    ONLINE_OFFSITE = 'online_offsite'  # Can be used by any institution
    ONLINE_ONSITE = 'online_onsite'  # In the case of SHSs, this is the only option
