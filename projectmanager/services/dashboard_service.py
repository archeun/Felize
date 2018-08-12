import time
from datetime import datetime

from projectmanager.models import Project, Employee, Task, SprintMilestone

TASKS_PENDING_STATUS_NAMES = ['Backlog', 'In Progress', 'On Hold']
MILESTONES_PENDING_STATUS_NAMES = ['Pending', 'In-Progress']


def get_pending_items_panel_data():
    """
    This function returns the information shown in the Dashboard panel, which shows the 'pending' item counts
    :return:
    """
    active_projects_count = Project.objects.filter(status=Project.ACTIVE).count()
    closed_projects_count = Project.objects.filter(status=Project.CLOSED).count()
    all_employees = Employee.objects.filter().all()
    all_employee_count = all_employees.count()
    allocated_employee_count = 0
    for employee in all_employees:
        employee_resources = employee.projectresource_set.all()
        for employee_resource in employee_resources:
            today = datetime.now().date()
            is_allocation_dates_set = employee_resource.allocation_start_date is not None and employee_resource.allocation_end_date is not None
            if is_allocation_dates_set and (employee_resource.allocation_start_date <= today <= employee_resource.allocation_end_date):
                allocated_employee_count += 1
                break
    unallocated_employee_count = all_employee_count - allocated_employee_count
    pending_tasks_count = Task.objects.filter(status__name__in=TASKS_PENDING_STATUS_NAMES).count()
    pending_milestones_count = SprintMilestone.objects.filter(status__in=MILESTONES_PENDING_STATUS_NAMES).count()
    return {
        'active_projects_count': active_projects_count,
        'closed_projects_count': closed_projects_count,
        'unallocated_employee_count': unallocated_employee_count,
        'pending_tasks_count': pending_tasks_count,
        'pending_milestones_count': pending_milestones_count,
    }
