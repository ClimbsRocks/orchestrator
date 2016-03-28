# orchestrator
> Schedule a series of API calls

## API:

### `orchestrator.schedule`
Arguments:
- httpAddress: the http address of the task. `orchestrator` will make a request to this address, and save the results.
- timeDelayInSeconds: the time delay before this task is run, given in seconds from right now.

Returns: 
taskID. This is a numeric ID for the task that was just scheduled. This ID can be used to retrieve the status/results of the task.

### `orchestrator.getResults`
Arguments:
- taskID: the ID of a task that was previously scheduled.

Returns:
If the task has been run successfully: results that were retrieved for that task.
If the task has encountered an error 4 times, and thus, has failed: the error message.
If the task has not run yet: a message stating that this task has not run yet. 


## Example Usage:
1. Save `orchestrator.py` into the desired directory.
2. Inside your python code, `import orchestrator`
3. `or = orchestrator['start']()`
3. `taskID1 = or.schedule(httpAddress, timeDelayInSeconds)`
4. `or.getResults(taskID1)` If the task has run and gotten results properly, this will return those results. If the scheduler has not run yet, or has repeatedly failed to get results, you will get an error message.

### Error Handling
Orchestrator will continue to run, even if one of the tasks errors out for any reason. The task will be retried 3 times. If there's an error at the end of 4 unsuccessful attempts, that error message or status code will be saved into the results for that taskID. Orchestrator will continue to run all other scheduled tasks as normal. 


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
  14. "Gracefully handling failed crashes" means that we will 
 
