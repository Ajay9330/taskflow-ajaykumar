import type { TaskStatus, TaskPriority } from '../types';

export const TASK_STATUSES: { id: TaskStatus; label: string }[] = [
  { id: 'todo', label: 'To Do' },
  { id: 'in_progress', label: 'In Progress' },
  { id: 'done', label: 'Done' },
];

export const TASK_PRIORITIES: { id: TaskPriority; label: string }[] = [
  { id: 'low', label: 'Low' },
  { id: 'medium', label: 'Medium' },
  { id: 'high', label: 'High' },
];

export const DASHBOARD_STATS = [
  { id: 'total_projects', label: 'Total Projects' },
  { id: 'projects_owned', label: 'Projects Owned' },
  { id: 'open_tasks', label: 'Open Tasks' },
  { id: 'completed_tasks', label: 'Completed Tasks' },
];
