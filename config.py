"""Static configuration for the speaker schedule optimizer."""

# Define speakers and their allowed number of assignments
speakers = [
    'HC1', 'HC2', 'HC3', 'HC4', 'HC5', 'HC6', 'HC7', 'HC8', 'HC9', 'SSP', 'YMP',
    'SS',  'YM',
    'YW', 'RS', 'PRI'
]

speaker_count = {
    'HC1': 3, 'HC2': 3, 'HC3': 3, 'HC4': 3, 'HC5': 3, 'HC6': 3, 'HC7': 3, 'HC8': 3, 'HC9': 3, 'SSP': 3, 'YMP': 3,
    'YM': 2, 'SS': 2,
    'YW': 4, 'RS': 4, 'PRI': 4
}

speaker_interval = {
    'HC6': 4, 'HC7': 4, 'HC8': 3, 'HC9': 3, 'SSP': 4, 'YMP': 4,
    'HC1': 3, 'HC2': 3, 'HC3': 3, 'HC4': 3, 'HC5': 3,
    'YM': 6, 'SS': 6,
    'YW': 3, 'RS': 3, 'PRI': 3
}

# Define units and their available months
units = {
    'Durham 5th': ['Jan', 'Feb', 'March', 'April', 'May', 'June', 'July', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
    'Roxboro': ['Jan', 'Feb', 'March', 'April', 'May', 'June', 'July', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
    'Durham YSA': ['June', 'Sep', 'Dec'],
    'Chapel Hill 1st': ['June', 'Sep', 'Dec'],
    'Chapel Hill 2nd': ['April', 'July', 'Oct'],
    'Durham 1st': ['May', 'Aug', 'Nov'],
    'Durham 2nd': ['June', 'Sep', 'Dec'],
    'Hillsborough': ['May', 'Aug', 'Nov'],
    'Mebane': ['April', 'July', 'Oct'],
    'FSLG-CH1': ['Jan', 'April', 'July', 'Oct']
}

# Month-to-quarter lookup
month_to_quarter = {
    **dict.fromkeys(['Jan', 'Feb', 'March'], 1),
    **dict.fromkeys(['April', 'May', 'June'], 2),
    **dict.fromkeys(['July', 'Aug', 'Sep'], 3),
    **dict.fromkeys(['Oct', 'Nov', 'Dec'], 4),
}


def get_quarter(month):
    """Return the quarter (1-4) for a given month."""
    return month_to_quarter[month]


def build_unit_month_pairs(units):
    """Build list of (unit, month) pairs and their quarter mappings."""
    unit_month_pairs = []
    quarter_map = {}
    for unit, months in units.items():
        for month in months:
            unit_month_pairs.append((unit, month))
            quarter_map[(unit, month)] = get_quarter(month)
    return unit_month_pairs, quarter_map
