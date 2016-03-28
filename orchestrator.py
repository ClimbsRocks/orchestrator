import sched
import time
import requests


class Orchestrator:

    def __init__(self):
        self.scheduler = sched.scheduler(time.time, time.sleep)
        self.results = {}
        self.next_task_num = 0
        

    def __make_api_call(self, http_address, failed_attempts, taskID, recurring=False, recurring_time=1000):

        # reschedule the recurring task
        if recurring:
            self.scheduler.enter(recurring_time, 1, self.__make_api_call, (http_address, 0, taskID, recurring, recurring_time))


        # make an api call
        try:
            r = requests.get(http_address)

            if r.status_code == requests.codes.ok:
                # save what we get back from the API call to results
                self.results[taskID].append( r.text )
            else:
                __handle_request_failure(http_address, failed_attempts + 1, taskID, r.status_code)

        except Exception as e:
            self.__handle_request_failure(http_address, failed_attempts + 1, taskID, e)


    def __handle_request_failure(self, http_address, failed_attempts, taskID, status_code):

        # save the error message no matter what, so the user can see an accurate log of what transpired
        self.results[taskID].append( status_code )

        if failed_attempts < 4:
            # we do not want to reschedule the tasks again
            self.__make_api_call( http_address, failed_attempts, taskID)


    def schedule(self, http_address, time_delay, does_repeat=False, priority=1):
        # for each task, we will have a list of all the responses associated with that task (the initial scheduling message, any errors collected, and for any recurring tasks, the full text response for each time that task is run)
        self.results[self.next_task_num] = ['This task has been scheduled']

        self.scheduler.enter(time_delay, priority, self.__make_api_call, (http_address, 0, self.next_task_num, does_repeat, time_delay))

        self.next_task_num += 1
        return self.next_task_num - 1


    def get_results(self, taskID):
        return self.results[taskID]


    def start(self):
        self.scheduler.run()
