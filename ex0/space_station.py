#!/usr/bin/env python3
# ########################################################################### #
#   shebang: 1                                                                #
#                                                          :::      ::::::::  #
#   space_station.py                                     :+:      :+:    :+:  #
#                                                      +:+ +:+         +:+    #
#   By: jkrishna <jkrishna@student.42.fr>            +#+  +:+       +#+       #
#                                                  +#+#+#+#+#+   +#+          #
#   Created: 2026/07/20 14:18:19 by jkrishna            #+#    #+#            #
#   Updated: 2026/07/20 14:27:31 by jkrishna           ###   ########.fr      #
#                                                                             #
# ########################################################################### #

from pydantic import BaseModel, Field, ValidationError
from datetime import datetime


class SpaceStation(BaseModel):
    station_id: str = Field(min_length=3, max_length=10)
    name: str = Field(min_length=1, max_length=50)
    crew_size: int = Field(ge=1, le=20)
    power_level: float = Field(ge=0.0, le=100.0)
    oxygen_level: float = Field(ge=0.0, le=100.0)
    last_maintenance: datetime = Field(default_factory=datetime.now)
    is_operational: bool = True
    notes: str | None = Field(default=None, max_length=200)


def main() -> None:
    valid_station = SpaceStation(
        station_id="ISS001", name="International Space Station",
        crew_size=6, power_level=85.5, oxygen_level=92.3,
        is_operational=True
    )
    print("Space Station Data Validation")
    print("========================================")
    print("Valid station created:")
    print(f"ID: {valid_station.station_id}")
    print(f"Name: {valid_station.name}")
    print(f"Crew: {valid_station.crew_size} people")
    print(f"Power: {valid_station.power_level}%")
    print(f"Oxygen: {valid_station.oxygen_level}%")
    if valid_station.is_operational:
        print("Status: Operational")
    else:
        print("Status: Not Operational")
    print()
    print("========================================")
    print("Expected validation error:")
    try:
        SpaceStation(
            station_id="ISS002", name="Space Station",
            crew_size=25, power_level=50.5, oxygen_level=64.3
        )
    except ValidationError as e:
        print(f"{e.errors()[0]['msg']}")


if __name__ == "__main__":
    main()
