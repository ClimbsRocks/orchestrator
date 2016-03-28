import sched
import time
import requests


class Orchestrator:

    def __init__(self):
        self.scheduler = sched.scheduler(time.time, time.sleep)
        self.results = {}
        self.next_task_num = 0
        

    def make_api_call(self, http_address, failed_attempts, taskID, recurring=False, recurring_time=1000):

        # make an api call
        try:
            r = requests.get(http_address)

            if r.status_code == requests.codes.ok:
                # save what we get back from the API call to results
                self.results[taskID] = r.text
            else:
                handle_http_failure(http_address, failed_attempts + 1, taskID, r.status_code)

        except Exception as e:
            self.handle_http_failure(http_address, failed_attempts + 1, taskID, e)

        # TODO: 
            # reschedule the recurring task


    # handle failure 
        # if it fails, run make_api_call, increasing failed_attempts
            # assuming that failed_attempts <=3
        # if it fails 4 times, save the error message into results
    def handle_http_failure(self, http_address, failed_attempts, taskID, status_code):
        if failed_attempts == 3:
            self.results[taskID] = status_code
        else:
            # we do not want to reschedule the tasks again
            self.make_api_call( http_address, failed_attempts, taskID)


    def schedule(self, http_address, time_delay, does_repeat=False, priority=1):
        self.results[self.next_task_num] = 'We have not run this task yet'

        self.scheduler.enter(time_delay, priority, self.make_api_call, (http_address, 0, self.next_task_num, does_repeat, time_delay))

        # TODO: 
            # take in the required arguments
            # schedule the task
            # make sure to handle recurring tasks
                # probably just schedule it again when we run it
            # build out functionality to make API calls
            # save results from API call into results dict
            # build out functionality to try again if an API call fails
            # update README with final API

        self.next_task_num += 1
        return self.next_task_num - 1

    def get_results(self, taskID):
        return self.results[taskID]

    def start(self):
        self.scheduler.run()



# To rapidly test this out:
or1 = Orchestrator()


taskID1 = or1.schedule('http://presotnparry.com',1)
taskID2 = or1.schedule('http://github.com/climbsrocks',2)
or1.start()
print taskID1

task1Results = or1.get_results(taskID1)
print task1Results
