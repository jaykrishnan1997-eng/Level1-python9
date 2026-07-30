#!/usr/bin/env python3
# ########################################################################### #
#   shebang: 1                                                                #
#                                                          :::      ::::::::  #
#   alien_contact.py                                     :+:      :+:    :+:  #
#                                                      +:+ +:+         +:+    #
#   By: jkrishna <jkrishna@student.42.fr>            +#+  +:+       +#+       #
#                                                  +#+#+#+#+#+   +#+          #
#   Created: 2026/07/30 10:50:46 by jkrishna            #+#    #+#            #
#   Updated: 2026/07/30 10:50:50 by jkrishna           ###   ########.fr      #
#                                                                             #
# ########################################################################### #

from pydantic import BaseModel, Field, ValidationError, model_validator
from datetime import datetime
from enum import Enum


class ContactType(str, Enum):
    RADIO = "radio"
    VISUAL = "visual"
    PHYSICAL = "physical"
    TELEPATHIC = "telepathic"


class AlienContact(BaseModel):
    contact_id: str = Field(min_length=5, max_length=15)
    timestamp: datetime = Field(default_factory=datetime.now)
    location: str = Field(min_length=3, max_length=100)
    contact_type: ContactType
    signal_strength: float = Field(ge=0.0, le=10.0)
    duration_minutes: int = Field(ge=1, le=1440)
    witness_count: int = Field(ge=1, le=100)
    message_received: str | None = Field(default=None, max_length=500)
    is_verified: bool = False

    @model_validator(mode='after')
    def check_business_rules(self) -> 'AlienContact':
        if not (self.contact_id[0] == 'A' and self.contact_id[1] == 'C'):
            raise ValueError('Contact ID must start with "AC"')

        if (
            self.contact_type == ContactType.PHYSICAL
            and not self.is_verified
        ):
            raise ValueError('Physical contact report must be verified')

        if (
            self.contact_type == ContactType.TELEPATHIC
            and self.witness_count < 3
        ):
            raise ValueError(
                'Telepathic contact requires at least 3 witnesses'
            )

        if self.signal_strength > 7.0 and not self.message_received:
            raise ValueError(
                'Strong signals should include a received message'
            )

        return self


def main() -> None:
    valid_contact = AlienContact(
        contact_id="AC_2024_001", contact_type=ContactType.RADIO,
        location="Area 51, Nevada", signal_strength=8.5,
        duration_minutes=45, witness_count=5,
        message_received="Greetings from Zeta Reticuli"
    )
    print("Alien Contact Log Validation")
    print("======================================")
    print("Valid contact report:")
    print(f"ID: {valid_contact.contact_id}")
    print(f"Type: {valid_contact.contact_type.lower()}")
    print(f"Location: {valid_contact.location}")
    print(f"Signal: {valid_contact.signal_strength}/10")
    print(f"Duration: {valid_contact.duration_minutes} minutes")
    print(f"Witnesses: {valid_contact.witness_count}")
    print(f"Message: '{valid_contact.message_received}'")
    print("======================================")
    print("Expected validation error:")
    try:
        AlienContact(
            contact_id="AC_2024_001", contact_type=ContactType.TELEPATHIC,
            location="Area 51, Nevada", signal_strength=8.5,
            duration_minutes=45, witness_count=2,
            message_received="Greetings from Zeta Reticuli"
        )
    except ValidationError as e:
        msg = e.errors()[0]['msg']
        print(msg.removeprefix("Value error, "))


if __name__ == "__main__":
    main()
