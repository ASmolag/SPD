from __future__ import print_function

import collections

# Import Python wrapper for or-tools CP-SAT solver.
from ortools.sat.python import cp_model


def MinimalJobshopSat(jobs_data):
    """Minimal jobshop problem."""
    # Create the model.
    model = cp_model.CpModel()

    #jobs_data = [  # task = (machine_id, processing_time).
    #    [(0, 3), (1, 2), (2, 2)],  # Job0
    #    [(0, 2), (2, 1), (1, 4)],  # Job1
    #    [(1, 4), (2, 3)]  # Job2
    #]

    #liczba maszyn
    machines_count = 1 + max(task[0] for job in jobs_data for task in job)
    all_machines = range(machines_count)

    #Maksymalny czas trwania jako suma wszystkich czasów wykonywania
    horizon = sum(task[1] for job in jobs_data for task in job)

    # Named tuple to store information about created variables.
    task_type = collections.namedtuple('task_type', 'start end interval')
    # Named tuple to manipulate solution information.
    assigned_task_type = collections.namedtuple('assigned_task_type',
                                                'start job index duration')

    #Stworzenie intrwałów pracy i dodanie ich na odpowiednie maszyny
    all_tasks = {}
    machine_to_intervals = collections.defaultdict(list)

    for job_id, job in enumerate(jobs_data):
        for task_id, task in enumerate(job):
            machine = task[0] #nr maszyny
            duration = task[1] #czas trwania
            suffix = '_%i_%i' % (job_id, task_id)
            start_var = model.NewIntVar(0, horizon, 'start' + suffix)
            end_var = model.NewIntVar(0, horizon, 'end' + suffix)
            interval_var = model.NewIntervalVar(start_var, duration, end_var,
                                                'interval' + suffix)
            all_tasks[job_id, task_id] = task_type(
                start=start_var, end=end_var, interval=interval_var)
            machine_to_intervals[machine].append(interval_var)

    #  Dodanie ograniczenia o nieprzerywaniu interwału na wszystkich maszynach
    for machine in all_machines:
        model.AddNoOverlap(machine_to_intervals[machine])

    # Rozpoczęcie kolejnej operacji w ramach tego samego zadania może rozpocząć się dopiero po zakończeniu się poprzedniej operacji
    for job_id, job in enumerate(jobs_data):
        for task_id in range(len(job) - 1):
            model.Add(all_tasks[job_id, task_id +
                                1].start >= all_tasks[job_id, task_id].end)

    # Cmax jako funkcja kryterialna
    obj_var = model.NewIntVar(0, horizon, 'makespan')
    model.AddMaxEquality(obj_var, [ #Wybierz ostani czas zakonczenia ze wszystkich maszyn
        all_tasks[job_id, len(job) - 1].end
        for job_id, job in enumerate(jobs_data)
    ])
    model.Minimize(obj_var) #Minimalizuj Cmax

    # Solve model.
    solver = cp_model.CpSolver()
    status = solver.Solve(model)

    if status == cp_model.OPTIMAL: #Jeśli rozwiązanie optymalne -> wypisz schemat rozwiązania
        # Lista zadań w obrębie jednej maszyny
        assigned_jobs = collections.defaultdict(list)
        for job_id, job in enumerate(jobs_data):
            for task_id, task in enumerate(job):
                machine = task[0]
                assigned_jobs[machine].append(
                    assigned_task_type(
                        start=solver.Value(all_tasks[job_id, task_id].start),
                        job=job_id,
                        index=task_id,
                        duration=task[1]))

        # Wypisanie zadań dla 1 maszyny
        output = ''
        for machine in all_machines:
            # Sort by starting time.
            assigned_jobs[machine].sort()
            sol_line_tasks = 'Machine ' + str(machine) + ': '
            sol_line = '           '

            for assigned_task in assigned_jobs[machine]:
                name = 'job_%i_%i' % (assigned_task.job, assigned_task.index)
                # Add spaces to output to align columns.
                sol_line_tasks += '%-10s' % name

                start = assigned_task.start
                duration = assigned_task.duration
                sol_tmp = '[%i,%i]' % (start, start + duration)
                # Add spaces to output to align columns.
                sol_line += '%-10s' % sol_tmp

            sol_line += '\n'
            sol_line_tasks += '\n'
            output += sol_line_tasks
            output += sol_line

        # Rozwiązanie optymalne - wypisz
        print('Optimal Schedule Length: %i' % solver.ObjectiveValue())
        print(output)

def GetINSAdataFromFile(filePath):
    plik = open(filePath)
    zawartosc = plik.read()
    dane = list(map(int, zawartosc.split()))  # zmiana string na int
    liczbaZadan = dane[0]
    liczbaMaszyn = dane[1]
    liczbaOperacji = dane[2]
    dane.pop(0)
    dane.pop(0)
    dane.pop(0)
    job = []
    jobs_data = []
    for i in range(liczbaZadan):
        liczbaOperacjiZadania = dane[0]
        dane.pop(0)
        for j in range(liczbaOperacjiZadania):
            job.append([dane[0]-1, dane[1]])
            dane.pop(0)
            dane.pop(0)
        jobs_data.append(0)
        jobs_data[i] = job[:]
        for k in range(len(job)):
            job.pop()

    return jobs_data



#MinimalJobshopSat()

if __name__ == '__main__':
    file_paths = ["jobshop.txt"]

    for i in range(len(file_paths)):
        jobs = GetINSAdataFromFile(file_paths[i])
        MinimalJobshopSat(jobs)


