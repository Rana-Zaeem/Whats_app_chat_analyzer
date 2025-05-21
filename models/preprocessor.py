import re
import pandas as pd
import streamlit as st
import time
import traceback


# =============================================
# SECTION 1: MAIN PREPROCESSING FUNCTION
# =============================================

def preprocess(data):
    """
    Preprocesses WhatsApp chat data and converts it into a structured DataFrame.
    Supports multiple WhatsApp chat formats.
    
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
        # =============================================
        # SECTION 2: FORMAT DETECTION
        # =============================================
        
        # First, detect which format this chat uses by checking the first few lines
        sample_data = "\n".join(data.split("\n")[:10])  # Use first 10 lines as a sample
        
        # Check various date patterns
        pattern_12h_1 = r'\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s(?:AM|PM)\s-\s'  # MM/DD/YY, hh:mm AM/PM -
        pattern_12h_2 = r'\d{1,2}/\d{1,2}/\d{2,4}\s\d{1,2}:\d{2}\s(?:AM|PM)\s-\s'   # MM/DD/YY hh:mm AM/PM -
        pattern_24h_1 = r'\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s-\s'             # MM/DD/YY, HH:MM -
        pattern_24h_2 = r'\d{1,2}/\d{1,2}/\d{2,4}\s\d{1,2}:\d{2}\s-\s'              # MM/DD/YY HH:MM -
        pattern_24h_3 = r'\[\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}:\d{2}\]\s'      # [MM/DD/YY, HH:MM:SS]
        pattern_24h_4 = r'\d{1,2}/\d{1,2}/\d{4},\s\d{1,2}:\d{2}\s-\s'               # DD/MM/YYYY, HH:MM -
        pattern_iso = r'\d{4}-\d{2}-\d{2}\s\d{1,2}:\d{2}:\d{2}\s-\s'                # YYYY-MM-DD HH:MM:SS -
        pattern_euro = r'\d{1,2}\.\d{1,2}\.\d{2,4},\s\d{1,2}:\d{2}\s-\s'            # DD.MM.YYYY, HH:MM -
        
        # Try to detect which pattern matches
        date_patterns = [
            (pattern_12h_1, '%m/%d/%y, %I:%M %p - ', 'US 12h comma'),
            (pattern_12h_1, '%d/%m/%y, %I:%M %p - ', 'UK 12h comma'),
            (pattern_12h_2, '%m/%d/%y %I:%M %p - ', 'US 12h no comma'),
            (pattern_12h_2, '%d/%m/%y %I:%M %p - ', 'UK 12h no comma'),
            (pattern_24h_1, '%m/%d/%y, %H:%M - ', 'US 24h comma'),
            (pattern_24h_1, '%d/%m/%y, %H:%M - ', 'UK 24h comma'),
            (pattern_24h_1, '%d/%m/%Y, %H:%M - ', 'UK 24h comma full year'),
            (pattern_24h_2, '%m/%d/%y %H:%M - ', 'US 24h no comma'),
            (pattern_24h_2, '%d/%m/%y %H:%M - ', 'UK 24h no comma'),
            (pattern_24h_3, '[%m/%d/%y, %H:%M:%S] ', 'Bracketed with seconds'),
            (pattern_24h_4, '%d/%m/%Y, %H:%M - ', 'DD/MM/YYYY format'),
            (pattern_iso, '%Y-%m-%d %H:%M:%S - ', 'ISO format'),
            (pattern_euro, '%d.%m.%y, %H:%M - ', 'European format'),
        ]
        
        detected_pattern = None
        detected_format = None
        detected_name = None
        
        for pattern, date_format, pattern_name in date_patterns:
            if re.search(pattern, sample_data):
                detected_pattern = pattern
                detected_format = date_format
                detected_name = pattern_name
                break
        
        # If no pattern was detected, try a more generic approach
        if detected_pattern is None:
            st.warning("""
            Chat format not automatically recognized. Attempting to process with generic pattern.
            If analysis fails, please ensure your chat export is in a standard WhatsApp format.
            """)
            # Fall back to most common format
            detected_pattern = pattern_12h_1
            detected_format = '%m/%d/%y, %I:%M %p - '
            detected_name = 'Generic fallback'
        else:
            time.sleep(5)
            st.success(f"Chat uploaded successfully!")

        # =============================================
        # SECTION 3: MESSAGE EXTRACTION
        # =============================================

        # Extract messages and dates using the detected pattern
        messages = re.split(detected_pattern, data)[1:]
        dates = re.findall(detected_pattern, data)
        
        # Handle empty result
        if not messages or not dates:
            st.error("No messages could be extracted. The chat format may not be supported.")
            # Try alternative approach - more permissive pattern
            generic_pattern = r'[\[\(]?(?:\d{1,4}[\/\.-]){2}\d{1,4}(?:[,\s])+\d{1,2}:\d{1,2}(?::\d{1,2})?(?:\s*[aApP][mM])?[\]\)]?\s*[^\n]+'
            message_blocks = re.findall(generic_pattern, data)
            
            if not message_blocks:
                return None
                
            # Process message blocks
            dates = []
            messages = []
            for block in message_blocks:
                # Split at the dash after timestamp
                parts = block.split(' - ', 1)
                if len(parts) == 2:
                    dates.append(parts[0] + ' - ')
                    messages.append(parts[1])
        
        # =============================================
        # SECTION 4: INITIAL DATAFRAME CREATION
        # =============================================
        
        df = pd.DataFrame({'user_message': messages, 'message_date': dates})
        
        # =============================================
        # SECTION 5: DATE PARSING
        # =============================================
        
        # Try multiple date formats with error handling
        df['date'] = None
        successful_parse = False
        
        for pattern, date_format, pattern_name in date_patterns:
            try:
                df['date'] = pd.to_datetime(df['message_date'], format=date_format)
                successful_parse = True
                break
            except:
                continue
        
        # If all formats failed, try flexible parsing
        if not successful_parse:
            try:
                df['date'] = pd.to_datetime(df['message_date'], infer_datetime_format=True, errors='coerce')
                # Drop rows where date parsing failed
                df = df.dropna(subset=['date'])
                if len(df) > 0:
                    successful_parse = True
            except Exception as e:
                st.error(f"Could not parse dates with any known format: {str(e)}")
                return None
        
        if not successful_parse or len(df) == 0:
            st.error("Failed to parse message dates. Chat format may not be supported.")
            return None
        
        # =============================================    
        # SECTION 6: USER AND MESSAGE EXTRACTION
        # =============================================
        
        users = []
        messages = []
        
        # Try multiple user extraction patterns
        for message in df['user_message']:
            # Try standard pattern (name: message)
            entry = re.split('([\\w\\W]+?):\\s', message)
            if entry[1:]:  # If pattern matched
                users.append(entry[1])
                messages.append(" ".join(entry[2:]))
            else:
                # Try alternative pattern (sometimes messages have different separator)
                alt_entry = re.split('([\\w\\W]+?)\\s[-–—]\\s', message)
                if len(alt_entry) > 1:
                    users.append(alt_entry[1])
                    messages.append(" ".join(alt_entry[2:]))
                else:
                    # If no user pattern matches, treat as system message
                    users.append('group_notification')
                    messages.append(message.strip())
        
        # =============================================
        # SECTION 7: DATAFRAME STRUCTURE SETUP
        # =============================================
        
        df['user'] = users
        df['message'] = messages
        df.drop(columns=['user_message', 'message_date'], inplace=True)
        
        # Fix phone number formats in user names if present
        df['user'] = df['user'].apply(lambda x: re.sub(r'^\+\d+\s', '', str(x)))
        
        # =============================================
        # SECTION 8: TIME COMPONENT EXTRACTION
        # =============================================
        
        df['only_date'] = df['date'].dt.date
        df['year'] = df['date'].dt.year
        df['month_num'] = df['date'].dt.month
        df['month'] = df['date'].dt.month_name()
        df['day'] = df['date'].dt.day
        df['day_name'] = df['date'].dt.day_name()
        df['hour'] = df['date'].dt.hour
        df['minute'] = df['date'].dt.minute
        df['am_pm'] = df['date'].dt.strftime('%p')
        
        # =============================================
        # SECTION 9: TIME PERIOD CLASSIFICATION
        # =============================================
        
        period = []
        for hour in df['hour']:
            if hour == 11: period.append(f'{hour}AM-12PM')
            elif hour == 23: period.append(f'{hour-12}PM-12AM')
            elif hour == 0: period.append('12AM-1AM')
            elif hour == 12: period.append('12PM-1PM')
            elif hour < 11: period.append(f'{hour}AM-{hour+1}AM')
            else: period.append(f'{hour-12}PM-{hour-11}PM')
        
        df['period'] = period
        
        # =============================================
        # SECTION 10: DATA VALIDATION AND CLEANUP
        # =============================================
        
        # Remove rows with NaN dates or messages
        df = df.dropna(subset=['date', 'message'])
        
        # Verify we have enough data
        if len(df) < 2:
            st.error("Too few valid messages found after processing. Please check the chat file format.")
            return None
            
        # Print some diagnostics about the results
        
        return df
        
    except Exception as e:
        st.error(f"Error processing chat: {str(e)}")
        # Include a more detailed error report
        st.error(f"Detailed error: {traceback.format_exc()}")
        return None

