from collections import defaultdict
from lagent.actions import BaseAction, tool_api


class JobSchedulingFIFO(BaseAction):
    '''Job Scheduling using First-In-First-Out (FIFO) Strategy

    This class provides a simple FIFO scheduling algorithm for job processing across multiple machines.
    '''

    @tool_api
    def schedule_jobs(self, num_machines, num_jobs, flat_processing_times):
        '''Schedules jobs on machines using FIFO strategy

        Args:
            num_machines (int): Number of machines available for processing.
            num_jobs (int): Number of jobs to be processed.
            flat_processing_times (list): A flat list of processing times for each job on each machine, ordered by job and machine.

        Returns:
            tuple: A tuple containing the formatted schedule for each machine and the total processing time for all jobs.
        '''
        # Initialize machines
        machines_schedule = defaultdict(lambda: {'current_time': 0, 'jobs': []})
        total_processing_time = 0

        # Decode the flat list into job processing times
        processing_times = [flat_processing_times[i * num_machines:(i + 1) * num_machines] for i in range(num_jobs)]

        # Schedule jobs based on processing times
        for job_id, times in enumerate(processing_times, start=1):
            for machine_id, time in enumerate(times, start=1):
                start_time = machines_schedule[machine_id]['current_time']
                end_time = start_time + time
                machines_schedule[machine_id]['jobs'].append((f"J{job_id}", start_time, end_time))
                machines_schedule[machine_id]['current_time'] = end_time
                total_processing_time = max(total_processing_time, end_time)

        # Return formatted schedule and total processing time
        formatted_schedule = {}
        for machine_id in range(1, num_machines + 1):
            formatted_schedule[f"M{machine_id}"] = [(job[0], job[1], job[2]) for job in
                                                    machines_schedule[machine_id]['jobs']]
        return formatted_schedule, total_processing_time


from collections import defaultdict
from lagent.actions import BaseAction, tool_api


class JobSchedulingFIFO(BaseAction):
    '''使用先进先出（FIFO）策略进行车间调度

    本类提供了一个简单的FIFO调度算法，用于跨多台机器进行作业处理。
    '''

    @tool_api
    def schedule_jobs(self, num_machines, num_jobs, flat_processing_times):
        '''使用FIFO策略在机器上调度作业

        参数:
            num_machines (int): 可用于处理的机器数量。
            num_jobs (int): 需要处理的作业数量。
            flat_processing_times (list): 每个作业在每台机器上的处理时间的扁平列表，按作业和机器的顺序排列。

        返回值:
            tuple: 包含每台机器的格式化调度和所有作业的总处理时间的元组。
        '''
        # 初始化机器
        machines_schedule = defaultdict(lambda: {'current_time': 0, 'jobs': []})
        total_processing_time = 0

        # 将扁平列表解码成作业处理时间
        processing_times = [flat_processing_times[i * num_machines:(i + 1) * num_machines] for i in range(num_jobs)]

        # 根据处理时间调度作业
        for job_id, times in enumerate(processing_times, start=1):
            for machine_id, time in enumerate(times, start=1):
                start_time = machines_schedule[machine_id]['current_time']
                end_time = start_time + time
                machines_schedule[machine_id]['jobs'].append((f"J{job_id}", start_time, end_time))
                machines_schedule[machine_id]['current_time'] = end_time
                total_processing_time = max(total_processing_time, end_time)

        # 返回格式化调度和总处理时间
        formatted_schedule = {}
        for machine_id in range(1, num_machines + 1):
            formatted_schedule[f"M{machine_id}"] = [(job[0], job[1], job[2]) for job in
                                                    machines_schedule[machine_id]['jobs']]
        return formatted_schedule, total_processing_time


jobscheduling= JobSchedulingFIFO()
print(jobscheduling.description)