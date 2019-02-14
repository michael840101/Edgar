#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
from io import open as ioopen
from datetime import datetime
from userSession import userSession


# Main function to write the sesseionization info to output file

def session_producer():

    # take the sys arguments as the input and output file path and names

    input_log_file = sys.argv[1]
    input_inactivity_file = sys.argv[2]
    output_file_uri = sys.argv[3]

    output_file = open(output_file_uri, 'w')
    with open(input_inactivity_file,'r') as interval:
        inactive_interval=int(interval.read()[0])

    with ioopen(input_log_file, encoding='utf-8') as csvfile:

        # read the csvfile first line and parsing header info for each of fields

        lines = csvfile.readlines()
        field_index = lines[0].split(',')

        for i in field_index:
            if 'ip' in i:
                ip_index = field_index.index(i)
                print ip_index
            if 'date' in i:
                date_index = field_index.index(i)
                print date_index
            if 'time' in i:
                time_index = field_index.index(i)
                print time_index
            if 'cik' in i:
                cik_index = field_index.index(i)
                print cik_index
            if 'accession' in i:
                accession_index = field_index.index(i)
                print accession_index
            if 'extention' in i:
                extention_index = field_index.index(i)
                print extention_index

        rest_lines = lines[1:]
        user_sessions = {}
        curr_time = None
        # read the csvfile line by line and parsing each line of data into
        # a session object
        for line in rest_lines:
            fields = line.split(',')
            ip = fields[ip_index]
            date = fields[date_index]
            time = fields[time_index]
            cik = fields[cik_index]
            timestamp = datetime.strptime((date + '' + time).strip(' '
                    ), '%Y-%m-%d%H:%M:%S')
            #check all the seesions in the map once time reflected,detact the end
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


        print(list(user_sessions))
        for i in user_sessions.keys():
            print(i)
        for i in user_sessions.values():
            print (i.user_ip, i.start_tm, i.latest_active_tm,
                   i.session_duration(), i.doc_num)
            line = ','.join([i.user_ip, datetime.strftime(i.start_tm,
                            '%Y-%m-%d %H:%M:%S'),
                            datetime.strftime(i.latest_active_tm,
                            '%Y-%m-%d %H:%M:%S'),
                            str(i.session_duration()), str(i.doc_num)])
            output_file.write(line + '\n')

    csvfile.close()
    output_file.close()


# run the analysis function if the file been triggered directly

if __name__ == '__main__':
    session_producer()
