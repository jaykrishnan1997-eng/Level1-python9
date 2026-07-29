#!/usr/bin/env python3
# ########################################################################### #
#   shebang: 1                                                                #
#                                                          :::      ::::::::  #
#   space_station.py                                     :+:      :+:    :+:  #
#                                                      +:+ +:+         +:+    #
#   By: jay-k <jay-k@student.42.fr>                  +#+  +:+       +#+       #
#                                                  +#+#+#+#+#+   +#+          #
#   Created: 2026/07/20 14:18:19 by jkrishna            #+#    #+#            #
#   Updated: 2026/07/29 23:18:28 by jay-k              ###   ########.fr      #
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
    valid_station = SpaceStation.model_validate({
        "station_id": "ISS001", "name": "International Space Station",
        "crew_size": 6, "power_level": 85.5, "oxygen_level": 92.3,
        "last_maintenance": "2026-06-15T09:30:00",
        "is_operational": True, "notes": "Routine inspection completed",
    })
    print("Space Station Data Validation")
    print("========================================")
    print("Valid station created:")
    print(f"ID: {valid_station.station_id}")
    print(f"Name: {valid_station.name}")
    print(f"Crew: {valid_station.crew_size} people")
    print(f"Power: {valid_station.power_level}%")
    print(f"Oxygen: {valid_station.oxygen_level}%")
    print(f"Last maintenance: {valid_station.last_maintenance}")
    print(f"Notes: {valid_station.notes}")
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
# python3 -m venv venv
# source venv/bin/activate
# pip install pydantic
# deactivate
# rm -rf venv
