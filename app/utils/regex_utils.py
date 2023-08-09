"""This module sets the several regural expressions used for validation."""

# Allowed letters to use in simple strings through the app.
ALLOWED = r"a-zA-Z\u00C0-\u00D6\u00D8-\u00F6"

# Regular expression used to validate the names of Users.
NAME_REGEX = fr"^([{ALLOWED}]+([ \-']{{0,1}}[{ALLOWED}]+)*){{1,2}}$"

# Regular expression used to validate the names of cities
CITY_REGEX = r"^([a-zA-Z\u0080-\u024F]+(?:. |-| |'))*[a-zA-Z\u0080-\u024F]*$"
