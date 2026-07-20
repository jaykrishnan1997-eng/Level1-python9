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

from pydantic import BaseModel, field_validator

class Space_station(BaseModel):
    station_id: str
    name: str
    crew_size: int
    power_level: float
    oxygen_level: float
    last_maintainance: str  # check its time statamp here
    is_operational: bool
    notes: str

    @field_validator(mode='id')
    def check_id(cls, mode):
        if len(mode) not in range(3, 11):
            raise ValueError('station_id length must be between 3 and 10')
        return mode

    @field_validator(mode='name')
    def check_id(cls, mode):
        if len(mode) not in range(1, 51):
            raise ValueError('name length must be between 1 and 50')
        return mode

    @field_validator(mode='crew_size')
    def check_id(cls, mode):
        if mode not in range(1, 21):
            raise ValueError('Crew size must be between 1 and 20')
        return mode

    @field_validator(mode='power_level')
    def check_id(cls, mode):
        if mode not in range(1, 21):
            raise ValueError('Crew size must be between 1 and 20')
        return mode


if __name__ == "__main__":
    cadet1 = Space_station(
        station_id="ISS001", name="International Space Station",
        crew_size=6, power_level=85.5, oxygen_level=92.3, is_operational=True
    )
