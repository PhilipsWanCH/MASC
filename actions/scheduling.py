from collections import defaultdict


def fifo_scheduling_custom_v3(num_machines, num_jobs, flat_processing_times):
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


# Example usage

# 帮我求解一个车间调度问题，机器数为2，工件数为2，每个工件在每个机器上的处理时间为[3, 2, 2, 1]
# num_machines = 2
# num_jobs = 2
# flat_processing_times = [3, 2, 2, 1]  # Flattened list of processing times

num_machines = 3
num_jobs = 2
flat_processing_times = [3, 2, 2, 1, 3, 2]  # Flattened list of processing times

# Schedule jobs and calculate total processing time
schedule_v3, total_time_v3 = fifo_scheduling_custom_v3(num_machines, num_jobs, flat_processing_times)

# Print the schedule and total processing time
print(schedule_v3, total_time_v3)
