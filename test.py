
# Function to get custom color based on rainfall value
def get_custom_color(rf):
    if 1 < rf <= 64.4:
        return '#98FB98'
    elif 64.5 <= rf <= 115.5:
        return '#FFFF00'
    elif 115.6 <= rf <= 204.4:
        return '#FFA500'
    elif rf > 204.4:
        return '#FF0000'
    else:
        return 'white'

colors = [get_custom_color(rf) for rf in date_data['RF']]
print(colors)