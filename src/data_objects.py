""" This file holds data objects and enums that used across the project. """

from typing import List

import enum
from dataclasses import dataclass

class LinkType(enum.Enum):
    SCRIPT = "Script"
    IMAGE = "Image"
    OTHER_LINK = "Other Link"
    LINK = "Link"
    EMAIL = "Email"
    TELEPHONE = "Telephone"

@dataclass
class LinkRecord:
    """ This is the main data object holding information about a link found in a webpage. """
    link: str
    resource_type: LinkType
    found_in_page: List[str]
    status_code: int
