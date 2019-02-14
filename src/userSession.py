from datetime import datetime

# create the user session class for the sessionization to manage the sessoin 
# for the new start time
class userSession(object):

    def __init__(self):
        self.user_ip=None
        self.latest_active_tm=None
        self.start_tm=None
        self.doc_num=None

    def __init__(self,ip,ac_tm,start_time,doc):
        self.user_ip=ip
        self.latest_active_tm=ac_tm
        self.start_tm=start_time
        self.doc_num=doc

    def update_doc_num(self, doc):
        """
        :type doc: int
        """
        self.doc_num+=doc

    def update_active_time(self, curr_time):
        """
        :type curr_time: timestamp
        """
        self.latest_active_tm=curr_time

    def idle_interval(self, curr_time):
        """
        :type curr_time: timestamp
        :rtype: int
        """
        delta = curr_time - self.latest_active_tm
        return delta.seconds

    def session_duration(self):
        """
        :type curr_time: timestamp
        :rtype: int
        """
        delta = self.latest_active_tm - self.start_tm
        return delta.seconds+1
