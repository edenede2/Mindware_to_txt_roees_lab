import sqlite3
import datetime
import streamlit

def fetch_boot_time(conn):
    cursor = conn.cursor()
    # Fetch the boot time value where attribute_key equals 0
    cursor.execute("SELECT attribute_value FROM device_attributes WHERE attribute_key = 0")
    boot_time_str = cursor.fetchone()
    if boot_time_str:
        boot_time_str = boot_time_str[0]
        pattern = r"System Boot Time:\s+(\d{2}/\d{2}/\d{4},\s+\d{2}:\d{2}:\d{2})"
        match = re.search(pattern, boot_time_str.decode())
        if match:
            date = match.group(1)
    return date

def extract_events_with_absolute_time(db_path, output_path, file, ecg=None, gsc=None, x_axis=None, y_axis=None, z_axis=None, Israel = None)
    # Connect to the SQLite database
    conn = sqlite3.connect(db_path)
    
    # Fetch the system boot time and convert it to a timestamp
    boot_time_str = fetch_boot_time(conn)
    if boot_time_str:
        # Assuming the date and time are in 'MM/DD/YYYY HH:MM:SS' format, adjust if necessary
        boot_time_format = "%H:%M:%S"
        base_timestamp = datetime.datetime.strptime(boot_time_str.split(',')[1].strip(), boot_time_format).timestamp()

        cursor = conn.cursor()
        if file == 'signals':
          query = """
          SELECT 
        # Query to fetch event data
        query = """
        SELECT e.event_id, es.label, e.event_time
        FROM event e
        JOIN event_source es ON e.event_source_id = es.event_source_id
        ORDER BY e.event_time
        """
        
        try:
            cursor.execute(query)
            events = cursor.fetchall()
            
            # Write the data to a text file, converting event_time
            with open(output_path, 'w') as file:
                file.write("Event ID\tLabel\tEvent Time (Absolute)\n")
                for event_id, label, event_time in events:
                    # Assuming event_time is in milliseconds from base time
                    absolute_time = base_timestamp + (event_time / 1000)

                    # add the 2 hours difference
                    if israel:
                      absolute_time += 7200

                    # Convert timestamp to readable date
                    readable_time = datetime.datetime.fromtimestamp(absolute_time).strftime('%H:%M:%S')
                    file.write(f"{event_id}\t{label}\t{readable_time}\n")
                    
            print(f"Event data has been written to {output_path}")
            
        except sqlite3.Error as error:
            print(f"An error occurred: {error}")
            
        finally:
            # Close the database connection
            conn.close()
    else:
        print("Boot time not found. Check the database or query.")

file_path = st.file_uploader('upload the mwi file here.', accept_multiple_files = True)
if file path is not None:
  for file in file_path:
    st.write(f'the file {file.name} uploaded'}

    subject = st.text_input('enter the subject name')
    
    db_path = file_path


    options = ['absolute_events', 'relative_events', 'signals']
    
    
    absolute_events = st.checkbox('absolute_events')

    relative_events = st.checkbox('relative_events')

    signals = st.checkbox('signals')

    if signals:
      st.write('select the signals that are in your file')

      ecg = st.checkbox('ecg')
      gsc = st.checkbox('GSC')
      x_axis = st.checkbox('Xaxis')
      y_axis = st.checkbox('Yaxis')
      z_axis = st.checkbox('Zaxis')
      output_path = f'{subject}_data'

      extract_events_with_absolute_time(db_path, output_path, 'signals', ecg=ecg, gsc=gsc, x_axis=x_axis, y_axis=y_axis, z_axis=z_axis)

    elif absolute_events:

      israel = st.checkbox('Israel time-zone')

      output_path = f'{subject}_events'

      extract_events_with_absolute_time(db_path, output_path, 'abs', Israel=israel)

    
    elif relative_events:

      output_path = f'{subject}_events'
    
      extract_events_with_absolute_time(db_path, output_path, 'rela')
      
    
    output_path = 'extracted_event_data_absolute_time.txt'
    extract_events_with_absolute_time(db_path, output_path)

    


