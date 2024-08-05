

class TaskQueue(object):
    """
    !!!! IMPORTANT !!!!
    Make sure to update the celery Q PROCESS when adding a new queue in here

    """

    DEFAULT = 'default'  # When a queue is not specified .. Ideally nothing should go in this bucket

    LG_HIGH = 'high_priority_lg'  # Critical tasks that require a large machine (1G)
    SM_HIGH = 'high_priority_sm'  # Critical tasks that can be done on smaller machines (200Mib)
    LG_LOW = 'low_priority_lg'    # NON critical tasks for large machines (1G)
    SM_LOW = 'low_priority_sm'    # NON critical tasks for smaller machines (200Mib)

    DEBUG = 'debug'  # debug / testing / temporary queue .. So that we don't mess with product queues
