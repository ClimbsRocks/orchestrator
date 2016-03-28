# orchestrator
> Schedule a series of API calls

## Installation
`pip install -r requirements.txt`

## API

### `orchestrator.schedule`
Arguments:
- http_address: the http address of the task. `orchestrator` will make a request to this address, and save the results.
- time_delay: the time delay before this task is run, given in seconds from when `orchestrator.start()` is invoked.
- does_repeat: boolean value representing whether this task should repeat or not. If it does repeat, we assume it will repeat on a pattern following the same delay given in time_delay.

Returns: 
taskID. This is a numeric ID for the task that was just scheduled. This ID can be used to retrieve the status/results of the task.

### `orchestrator.getResults`
Arguments:
- taskID: the ID of a task that was previously scheduled.

Returns:
A list of results showing the full status of each attempt. This starts with a note saying the task was scheduled, and includes the error or results for each time we attempted to run this task. 

### `orchestrator.start`
Arguments: None
Returns: None
This method simply states that we have scheduled our tasks, and are ready to begin running them, after the given delays. This is when the clock starts. 

## Example Usage
1. Save `orchestrator.py` into the desired directory.
2. Inside your python code, 
```python
from orchestrator import Orchestrator

or1 = Orchestrator()

# attempt a failure case- this URL has a typo
taskID1 = or1.schedule('http://presotnparry.com',2)
taskID2 = or1.schedule('http://github.com/climbsrocks',1)

or1.start()
print taskID1

task1Results = or1.get_results(taskID1)
print task1Results

```


### Error Handling
Orchestrator will continue to run, even if one of the tasks errors out for any reason. A failing task will be retried 3 times. Any errors that are encountered, whether the eventual result is a success or not, will be saved into the results for that task. This gives the user an accurate log, which might be useful to figure out where to put in some maintenance work. Orchestrator will continue to run all other scheduled tasks as normal. 


#### Assumptions

If we were in-person and could go back and forth on this rapidly, I would phrase these as questions and test how well we can collaborate. Instead, they will simply be design decisions that could be relatively easily modified if design requirements change. 

  1. The user will give us a time (in seconds), representing how far in the future they would like the given task to be run. 
  2. The user will give us the http address of the API endpoint as one of the inputs to the orchestrator.
  3. Each API request should be a GET request.
  4. Recurring requests will take in a time (in seconds) between executions of the given task (even though a cron job is mostly likely better suited for this). 
  5. Recurring tasks will recur forever on that same fixed interval.
  6. A task cannot be canceled once scheduled. 
  7. There is no way to access all tasks at once.
  8. The user can come back to ask orchestrator for the results of a task. In this way, we avoid introducing asynchronicity to the Python codebase, which likely doesn't have much asynch code yet. If this were in JS, we'd definitely be going asynch and returning promises! 
  9. The http address given by the user will represent the full URL, without needing to add in query parameters or anything else.
  10. A task that fails will retry 3 times before admitting total defeat. We will save an error message as the "result" for this task.
  11. We are going to assume the user is smart enough to use this in a thread they are not running anything else in, as orchestrator will be blocking in that thread. We could redesign it to be non-blocking, but for now we are deciding that is not in the MVP scope. 
  12. The user will schedule all of their tasks at once.
  13. All API calls will be GETs. 
  14. The "results" of a successfully completed task is the text of the response, while the "results" for a failed task is information about the error. 
 
