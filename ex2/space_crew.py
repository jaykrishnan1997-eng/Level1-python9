#!/usr/bin/env python3
# ########################################################################### #
#   shebang: 1                                                                #
#                                                          :::      ::::::::  #
#   space_crew.py                                        :+:      :+:    :+:  #
#                                                      +:+ +:+         +:+    #
#   By: jkrishna <jkrishna@student.42.fr>            +#+  +:+       +#+       #
#                                                  +#+#+#+#+#+   +#+          #
#   Created: 2026/07/29 21:46:18 by jay-k               #+#    #+#            #
#   Updated: 2026/07/30 12:11:54 by jkrishna           ###   ########.fr      #
#                                                                             #
# ########################################################################### #

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

    @model_validator(mode='after')
    def check_mission_rules(self) -> 'SpaceMission':
        if not (self.mission_id[0] == 'M'):
            raise ValueError('Mission ID must start with "M"')

        if not any(
            member.rank in (Rank.COMMANDER, Rank.CAPTAIN)
            for member in self.crew
        ):
            raise ValueError(
                'Mission must have at least one Commander or Captain'
            )

        if self.duration_days > 365:
            experienced_count = sum(
                1 for member in self.crew if member.years_experience >= 5
            )
            if experienced_count < len(self.crew) * 0.5:
                raise ValueError(
                    'Long missions need 50% experienced crew (5+ years)'
                )
        if not all(member.is_active for member in self.crew):
            raise ValueError('All crew members must be active')

        return self


def main() -> None:
    try:
        valid_crew = [
            CrewMember(
                member_id="CM001", name="Sarah Connor", rank=Rank.COMMANDER,
                age=42, specialization="Mission Command", years_experience=20,
            ),
            CrewMember(
                member_id="CM002", name="John Smith", rank=Rank.LIEUTENANT,
                age=34, specialization="Navigation", years_experience=8,
            ),
            CrewMember(
                member_id="CM003", name="Alice Johnson", rank=Rank.OFFICER,
                age=29, specialization="Engineering", years_experience=6,
            ),
        ]
        valid_mission = SpaceMission(
            mission_id="M2024_MARS", mission_name="Mars Colony Establishment",
            destination="Mars", duration_days=900, crew=valid_crew,
            budget_millions=2500.0,
        )
        print("Space Mission Crew Validation")
        print("======================================")
        print("Valid mission created:")
        print(f"Mission: {valid_mission.mission_name}")
        print(f"ID: {valid_mission.mission_id}")
        print(f"Destination: {valid_mission.destination}")
        print(f"Duration: {valid_mission.duration_days} days")
        print(f"Budget: ${valid_mission.budget_millions}M")
        print(f"Crew size: {len(valid_mission.crew)}")
        print("Crew members:")
        for member in valid_mission.crew:
            print(
                f"- {member.name} ({member.rank.lower()}) "
                f"- {member.specialization}"
            )
        print("======================================")
        print("Expected validation error:")

        SpaceMission(
            mission_id="M2024_TEST",
            mission_name="Test Mission Without Command",
            destination="Moon", duration_days=30,
            crew=[
                CrewMember(
                    member_id="CM004", name="Bob Ross", rank=Rank.CADET,
                    age=22, specialization="Support", years_experience=2,
                ),
            ],
            budget_millions=50.0,
        )
    except ValidationError as e:
        msg = e.errors()[0]['msg']
        print(msg.removeprefix("Value error, "))


if __name__ == "__main__":
    main()
