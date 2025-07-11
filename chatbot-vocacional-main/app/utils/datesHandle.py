from datetime import datetime
import pytz

def get_formatted_date():
    ecuador_timezone = pytz.timezone('America/Guayaquil')
    current_date = datetime.now(ecuador_timezone)
    formatted_date = current_date.strftime('%Y-%m-%d %H:%M:%S')
    return formatted_date