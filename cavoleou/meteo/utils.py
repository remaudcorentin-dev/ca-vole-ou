
def vent_direction_int_to_enum(vent_direction):
    abbreviations = [
        "N", "NNE", "NE", "ENE",
        "E", "ESE", "SE", "SSE",
        "S", "SSO", "SO", "OSO",
        "O", "ONO", "NO", "NNO"
    ]
    index = int((vent_direction % 360) / 22.5 + 0.5) % 16
    return abbreviations[index].lower()
