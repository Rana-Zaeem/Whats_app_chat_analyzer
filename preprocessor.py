import re
import pandas as pd
from datetime import datetime

def preprocess(data):
    try:
        # Validate input data
        if not isinstance(data, str) or not data.strip():
            raise ValueError("Invalid input data. Please provide a valid WhatsApp chat export file.")

        pattern = r'\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s(?:AM|PM)\s-\s'
        
        messages = re.split(pattern, data)[1:]
        dates = re.findall(pattern, data)
        
        if not messages or not dates:
            raise ValueError("No valid messages found in the chat file. Please check the file format.")
        
        if len(messages) != len(dates):
            raise ValueError("Message and date mismatch. The chat file might be corrupted.")

        df = pd.DataFrame({'user_message': messages, 'message_date': dates})
        
        # Handle date parsing with error checking
        try:
            df['message_date'] = pd.to_datetime(df['message_date'], format='%m/%d/%y, %I:%M %p - ')
        except (ValueError, TypeError):
            try:
                # Try alternate date format
                df['message_date'] = pd.to_datetime(df['message_date'], format='%d/%m/%y, %I:%M %p - ')
            except (ValueError, TypeError):
                raise ValueError("Unable to parse message dates. Please ensure the chat export format is correct.")

        df.rename(columns={'message_date': 'date'}, inplace=True)

        users = []
        messages = []
        for message in df['user_message']:
            entry = re.split('([\\w\\W]+?):\\s', message)
            if entry[1:]:  # user name
                users.append(entry[1])
                messages.append(" ".join(entry[2:]))
            else:
                users.append('group_notification')
                messages.append(entry[0])

        df['user'] = users
        df['message'] = messages
        df.drop(columns=['user_message'], inplace=True)

        # Add date-related columns with error handling
        df['only_date'] = df['date'].dt.date
        df['year'] = df['date'].dt.year
        df['month_num'] = df['date'].dt.month
        df['month'] = df['date'].dt.month_name()
        df['day'] = df['date'].dt.day
        df['day_name'] = df['date'].dt.day_name()
        df['hour'] = df['date'].dt.hour
        df['minute'] = df['date'].dt.minute
        df['am_pm'] = df['date'].dt.strftime('%p')

        # Create period with validation
        period = []
        for hour in df['hour']:
            if not isinstance(hour, (int, float)) or hour < 0 or hour > 23:
                period.append('Unknown')
                continue
                
            if hour == 11:
                period.append(f'{hour}AM-12PM')
            elif hour == 23:
                period.append(f'{hour-12}PM-12AM')
            elif hour == 0:
                period.append('12AM-1AM')
            elif hour == 12:
                period.append('12PM-1PM')
            elif hour < 11:
                period.append(f'{hour}AM-{hour+1}AM')
            elif hour < 23:
                period.append(f'{hour-12}PM-{hour-11}PM')

        df['period'] = period

        # Validate the final DataFrame
        if df.empty:
            raise ValueError("No valid data could be extracted from the chat file.")

        return df

    except Exception as e:
        # Wrap any other exceptions with a more user-friendly message
        raise ValueError(f"Error processing chat file: {str(e)}")

