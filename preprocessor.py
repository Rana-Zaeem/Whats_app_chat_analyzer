import re
import pandas as pd
import streamlit as st

def preprocess(data):
    """
    Preprocesses WhatsApp chat data and converts it into a structured DataFrame.
    
    Parameters:
    -----------
    data : str
        Raw WhatsApp chat text data
        
    Returns:
    --------
    pd.DataFrame or None
        Processed DataFrame with message details if successful, None if error occurs
    """
    try:
        # SECTION 1: Message Extraction
        # Extract messages and dates using regex pattern
        pattern = r'\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s(?:AM|PM)\s-\s'
        messages = re.split(pattern, data)[1:]
        dates = re.findall(pattern, data)
        
        # SECTION 2: Initial DataFrame Creation
        df = pd.DataFrame({'user_message': messages, 'message_date': dates})
        
        # SECTION 3: Date Parsing
        # Handle multiple date formats
        try:
            df['date'] = pd.to_datetime(df['message_date'], format='%d/%m/%y, %I:%M %p - ')
        except:
            df['date'] = pd.to_datetime(df['message_date'], format='%m/%d/%y, %I:%M %p - ')

        # SECTION 4: Message Component Extraction
        users = []
        messages = []
        for message in df['user_message']:
            entry = re.split('([\\w\\W]+?):\\s', message)
            if entry[1:]:
                users.append(entry[1])
                messages.append(" ".join(entry[2:]))
            else:
                users.append('group_notification')
                messages.append(entry[0])

        # SECTION 5: DataFrame Structure Setup
        # Add extracted components and remove temporary columns
        df['user'] = users
        df['message'] = messages
        df.drop(columns=['user_message', 'message_date'], inplace=True)

        # SECTION 6: Time Component Extraction
        # Extract various date/time components for analysis
        df['only_date'] = df['date'].dt.date
        df['year'] = df['date'].dt.year
        df['month_num'] = df['date'].dt.month
        df['month'] = df['date'].dt.month_name()
        df['day'] = df['date'].dt.day
        df['day_name'] = df['date'].dt.day_name()
        df['hour'] = df['date'].dt.hour
        df['minute'] = df['date'].dt.minute
        df['am_pm'] = df['date'].dt.strftime('%p')

        # SECTION 7: Time Period Classification
        # Create user-friendly time periods
        period = []
        for hour in df['hour']:
            if hour == 11: period.append(f'{hour}AM-12PM')
            elif hour == 23: period.append(f'{hour-12}PM-12AM')
            elif hour == 0: period.append('12AM-1AM')
            elif hour == 12: period.append('12PM-1PM')
            elif hour < 11: period.append(f'{hour}AM-{hour+1}AM')
            else: period.append(f'{hour-12}PM-{hour-11}PM')

        df['period'] = period
        return df
        
    except Exception as e:
        st.error(f"Error processing chat: {str(e)}")
        return None

