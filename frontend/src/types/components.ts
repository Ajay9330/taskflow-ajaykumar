import type { Task, TaskStatus } from './index';

export interface TaskDialogProps {
  open: boolean;
  onOpenChange: (open: boolean) => void;
  task?: Task | null;
  onSave?: (task: Partial<Task>) => void;
}

export interface TaskEditDialogProps {
  open: boolean;
  onOpenChange: (open: boolean) => void;
  task?: Task | null;
  onSave: (task: Partial<Task>) => void;
}

export interface TaskViewDialogProps {
  open: boolean;
  onOpenChange: (open: boolean) => void;
  task?: Task | null;
}

export interface KanbanColumnProps {
  id: TaskStatus;
  title: string;
  tasks: Task[];
  onView: (task: Task) => void;
  onEdit: (task: Task) => void;
  onDelete: (taskId: string) => void;
  onQuickUpdate: (taskId: string, updates: Partial<Task>) => void;
}

export interface TaskCardProps {
  task: Task;
  onView: (task: Task) => void;
  onEdit: (task: Task) => void;
  onDelete: (taskId: string) => void;
  onQuickUpdate: (taskId: string, updates: Partial<Task>) => void;
}
