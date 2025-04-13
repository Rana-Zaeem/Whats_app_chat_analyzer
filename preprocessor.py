import re
import pandas as pd
import streamlit as st

def preprocess(data):
    try:
        pattern = r'\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s(?:AM|PM)\s-\s'
        messages = re.split(pattern, data)[1:]
        dates = re.findall(pattern, data)
        
        if not messages or not dates:
            st.error("No valid messages found in the chat file")
            return None
            
        df = pd.DataFrame({'user_message': messages, 'message_date': dates})
        
        # Try multiple date formats
        date_formats = [
            '%m/%d/%y, %I:%M %p - ',
            '%d/%m/%y, %I:%M %p - ',
            '%m/%d/%Y, %I:%M %p - ',
            '%d/%m/%Y, %I:%M %p - '
        ]
        
        for date_format in date_formats:
            try:
                df['message_date'] = pd.to_datetime(df['message_date'], format=date_format)
                break
            except:
                continue
                
        if pd.api.types.is_datetime64_dtype(df['message_date']) == False:
            st.error("Could not parse message dates")
            return None

        df.rename(columns={'message_date': 'date'}, inplace=True)

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

        df['user'] = users
        df['message'] = messages
        df.drop(columns=['user_message'], inplace=True)

        df['only_date'] = df['date'].dt.date
        df['year'] = df['date'].dt.year
        df['month_num'] = df['date'].dt.month
        df['month'] = df['date'].dt.month_name()
        df['day'] = df['date'].dt.day
        df['day_name'] = df['date'].dt.day_name()
        df['hour'] = df['date'].dt.hour
        df['minute'] = df['date'].dt.minute
        df['am_pm'] = df['date'].dt.strftime('%p')

        period = []
        for hour in df['hour']:
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
            else:
                period.append(f'{hour-12}PM-{hour-11}PM')

        df['period'] = period
        return df
    except Exception as e:
        st.error(f"Error processing chat: {str(e)}")
        return None

