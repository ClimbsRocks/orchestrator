import sched
import time


class Orchestrator:

    def __init__(self):
        self.scheduler = sched.scheduler(time.time, time.sleep)
        self.results = {}
        self.nextTaskNum = 0
        

    def makeAPICall(httpAddress, failedAttempts, recurring=False, recurringTime=1000):
        print 'inside makeAPICall'
        # TODO: 
            # reschedule the recurring task
            # make an api call
            # handle failure 
                # if it fails, run this function recursively, increasing failedAttempts
                    # assuming that failedAttempts <=3
                # if it fails 4 times, save the error message into results
            # save what we get back from the API call to results


    def schedule(self, httpAddress, timeDelay, doesRepeat=False, priority=1):
        self.results[self.nextTaskNum] = 'We have not run this task yet'

        scheduler.enter(timeDelay, priority, makeAPICall, (httpAddress, 0, doesRepeat, timeDelay))

        # TODO: 
            # take in the required arguments
            # schedule the task
            # make sure to handle recurring tasks
                # probably just schedule it again when we run it
            # build out functionality to make API calls
            # save results from API call into results dict
            # build out functionality to try again if an API call fails
            # update README with final API

        self.nextTaskNum += 1
        return self.nextTaskNum - 1

    def getResults(self, taskID):
        return self.results[taskID]

    def start(self):
        self.scheduler.run()



# To rapidly test this out:
or1 = Orchestrator()


taskID1 = or1.schedule('http://prestonparry.com',5)
or1.start()
print taskID1

task1Results = or1.getResults(taskID1)
print task1Results