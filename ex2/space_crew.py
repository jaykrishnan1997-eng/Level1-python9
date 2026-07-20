from pydantic import BaseModel, Field, ValidationError, model_validator
from datetime import datetime
from enum import Enum


class Rank(str, Enum):
    CADET = "cadet"
    OFFICER = "officer"
    LIEUTENANT = "lieutenant"
    CAPTAIN = "captain"
    COMMANDER = "commander"


class CrewMember(BaseModel):
    member_id: str = Field(min_length=3, max_length=10)
    name: str = Field(min_length=2, max_length=50)
    rank: Rank
    age: int = Field(ge=18, le=80)
    specialization: str = Field(min_length=3, max_length=30)
    years_experience: int = Field(ge=0, le=50)
    is_active: bool = True


class SpaceMission(BaseModel):
    crew: list[CrewMember] = Field(min_length=1, max_length=12)
    mission_id: str = Field(min_length=5, max_length=15)
    mission_name: str = Field(min_length=3, max_length=100)
    destination: str = Field(min_length=3, max_length=50)
    launch_date:  datetime = Field(default_factory=datetime.now)
    duration_days: int = Field(ge=1, le=3650)
    mission_status: str = "planned"
    budget_millions: float = Field(ge=1.0, le=10000.0)

# fix below

    @model_validator(mode='after')
    def check_rules(self) -> 'AlienContact':
        if not (self.contact_id[0] == 'A' and self.contact_id[1] == 'C'):
            raise ValueError('Contact ID must start with "AC"')

        if self.contact_type == ContactType.PHYSICAL and not self.is_verified:
            raise ValueError('Physical contact report must be verified')

        if self.contact_type == ContactType.TELEPATHIC and self.witness_count < 3:
            raise ValueError('Telepathic contact requires at least 3 witnesses')

        if self.signal_strength > 7.0 and not self.message_received:
            raise ValueError('Strong signals should include a received message')

        return self


def main() -> None:
    validcontact = AlienContact(
        contact_id="AC_2024_001", contact_type=ContactType.RADIO,
        location="Area 51, Nevada", signal_strength=8.5,
        duration_minutes=45, witness_count=5,
        message_received="Greetings from Zeta Reticuli"
    )
    print("Alien Contact Log Validation")
    print("======================================")
    print("Valid contact report:")
    print(f"ID: {validcontact.contact_id}")
    print(f"Type: {validcontact.contact_type.lower()}")
    print(f"Location: {validcontact.location}")
    print(f"Signal: {validcontact.signal_strength}/10")
    print(f"Duration: {validcontact.duration_minutes} minutes")
    print(f"Witnesses: {validcontact.witness_count}")
    print(f"Message: '{validcontact.message_received}'")
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

#@model_validator(mode='after')
#    def check_mission_rules(self) -> 'SpaceMission':
#        if not self.mission_id.startswith('M'):
#            raise ValueError('Mission ID must start with "M"')
#
#        if not any(member.rank in (Rank.COMMANDER, Rank.CAPTAIN) for member in self.crew):
#            raise ValueError('Mission must have at least one Commander or Captain')
#
#
#        if self.duration_days > 365:
#            experienced_count = sum(1 for member in self.crew if member.years_experience >= 5)
#            if experienced_count < len(self.crew) * 0.5:
#                raise ValueError('Long missions need 50% experienced crew (5+ years)')
#
#        if not all(member.is_active for member in self.crew):
#            raise ValueError('All crew members must be active')
#
#        return self