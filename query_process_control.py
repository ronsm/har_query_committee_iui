import numpy as np
import pandas as pd
from sklearn.metrics import mutual_info_score
from colorama import Fore, Style
from time import perf_counter
from time import sleep

from committee_predict import CommitteePredict
from query_select import QuerySelect
from log import Log

class QueryProcessControl(object):
    def __init__(self):
        self.id = 'query_process_control'

        self.logger = Log(self.id)
        self.logger.startup_msg()

        self.max_predictions = 0

        self.committee_predict = CommitteePredict()
        self.query_select = QuerySelect()

        self.logger.log_great('Ready.')

    def run(self):
        self.committee_predict.reset_counter()
        self.max_predictions = self.committee_predict.get_max_predictions()

        for i in range(0, self.max_predictions):
            if i > 0:
                start_time = perf_counter()

            committee_vote_1, committee_vote_2, committee_vote_3, true = self.committee_predict.next_prediction()
            self.query_select.insert_sample(committee_vote_1, committee_vote_2, committee_vote_3, true)

            if i > 0:
                end_time = perf_counter()
                time_taken = end_time - start_time
                delay_time = 1.0 - time_taken

                if delay_time >= 0.0:
                    print('Prediction time was:', time_taken, ', sleeping for:', delay_time, 'seconds')
                    sleep(delay_time)
                else:
                    self.logger.log_warn('Predict/analyse cycle took longer than 1 second! System is not keeping up with real-time.')

if __name__ == '__main__':
    qpc = QueryProcessControl()
    qpc.run()