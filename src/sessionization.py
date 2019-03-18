"""
The sessionization functiones that produce the new csv file tracking
how long a particular user spends on EDGAR during a visit and
how many documents that user requested during the session
"""
import sys
from io import open as ioopen
from datetime import datetime
from userSession import userSession


# Main function to write the sesseionization info to output file

def session_producer(input_log_file, input_inactivity_file, output_file_uri):
    """
    The function that take the input log file and input inactive_interval file location
    to caculate the time spends and file requested per user session
    and write the result into output file location
    :type input_log_file: string
    :type input_inactivity_file: string
    :type output_file_uri: string

    :rtype :
    """
    # read the csvfile first line and parsing header info for each of fields
    fields_idx=header_parser(input_log_file)
    #open the output file for writing output
    output_file = open(output_file_uri, 'w')

    #read the idle_interval parameter from input_inactivity_file
    with open(input_inactivity_file,'r') as interval:
        inactive_interval=int(interval.read()[0])

    # read the csvfile line by line and parsing each line of data into
    # a session object
    with ioopen(input_log_file, encoding='utf-8') as csvfile:
        lines = csvfile.readlines()
        rest_lines = lines[1:]
        user_sessions = {}
        curr_time = None

        for line in rest_lines:
            fields = line.split(',')
            ip = fields[fields_idx[ip_index]]
            date = fields[fields_idx[date_index]]
            time = fields[fields_idx[time_index]]
            cik = fields[fields_idx[cik_index]]
            timestamp = datetime.strptime((date + '' + time).strip(' '
                    ), '%Y-%m-%d%H:%M:%S')
            #first check all the seesions in the dictionary once time reflected,detact the end
            #session and pop it to ouput file
            if curr_time is None or timestamp > curr_time:
                curr_time = timestamp
                print curr_time
                for user in user_sessions.values():
                    if user.idle_interval(curr_time) > inactive_interval:
                        u_ip = user.user_ip
                        end_session = user_sessions.pop(u_ip)

                        line = ','.join([end_session.user_ip,
                                datetime.strftime(end_session.start_tm,
                                '%Y-%m-%d %H:%M:%S'),
                                datetime.strftime(end_session.latest_active_tm,
                                '%Y-%m-%d %H:%M:%S'),
                                str(end_session.session_duration()),
                                str(end_session.doc_num)])
                        output_file.write(line + '\n')

            #processing the curr line and check with user_sessions for insert or update
            if ip in user_sessions.keys():
                user_sessions[ip].update_active_time(timestamp)
                user_sessions[ip].update_doc_num(1)
            else:
                new_session = userSession(ip, timestamp, timestamp, 1)
                print(new_session.user_ip)
                user_sessions[ip] = new_session

            #append the rest of the remaining sessoins into the output file once reach the last line
            line = ','.join([i.user_ip, datetime.strftime(i.start_tm,
                            '%Y-%m-%d %H:%M:%S'),
                            datetime.strftime(i.latest_active_tm,
                            '%Y-%m-%d %H:%M:%S'),
                            str(i.session_duration()), str(i.doc_num)])
            output_file.write(line + '\n')

    csvfile.close()
    output_file.close()


def header_parser(input_log_file):
    """
    The function parsing the header of csv file and
    return the dictionary of field as key and index of field as value
    :type input_log_file: string
    :rtype fields: dictionary
    """
    fields={}
    with ioopen(input_log_file, encoding='utf-8') as csvfile:

        line_1 = csvfile.readline()
        field_index = line_1.split(',')

        for i in field_index:
            if 'ip' in i:
                fields[ip_index] = field_index.index(i)
            if 'date' in i:
                fields[date_index] = field_index.index(i)
            if 'time' in i:
                fields[time_index] = field_index.index(i)
            if 'cik' in i:
                fields[cik_index] = field_index.index(i)
            if 'accession' in i:
                fields[accession_index] = field_index.index(i)
            if 'extention' in i:
                fields[extention_index] = field_index.index(i)

    return fields

# run the analysis function if the file been triggered directly
if __name__ == '__main__':

    # take the sys arguments as the input and output file path and names
    input_log_file = sys.argv[1]
    input_inactivity_file = sys.argv[2]
    output_file_uri = sys.argv[3]
    # run the session producer function
    session_producer(input_log_file, input_inactivity_file, output_file_uri)
