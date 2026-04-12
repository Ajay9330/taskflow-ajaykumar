import { useState, useEffect } from 'react';
import { useParams } from 'react-router';
import { DragDropContext } from '@hello-pangea/dnd';
import type { DropResult } from '@hello-pangea/dnd';
import { Plus } from 'lucide-react';
import { useProjectDetails, useCreateTask, useUpdateTask, useDeleteTask } from '@/api/queries';
import type { Task, TaskStatus } from '@/types';
import { Button } from '@/components/ui/button';
import { toast } from 'sonner';
import { TaskEditDialog } from '../components/board/task-edit-dialog';
import { TaskViewDialog } from '../components/board/task-view-dialog';
import { KanbanColumn } from '../components/board/kanban-column';
import { TASK_STATUSES } from '../constants';
import { useProjectEvents } from '@/hooks/useProjectEvents';
import {
  AlertDialog,
  AlertDialogAction,
  AlertDialogCancel,
  AlertDialogContent,
  AlertDialogDescription,
  AlertDialogFooter,
  AlertDialogHeader,
  AlertDialogTitle,
} from '@/components/ui/alert-dialog';

export default function ProjectBoard() {
  const { id } = useParams<{ id: string }>();
  
  useProjectEvents(id);
  
  const { data: project, isLoading, isError } = useProjectDetails(id);
  const createTask = useCreateTask(id);
  const updateTask = useUpdateTask(id);
  const deleteTask = useDeleteTask(id);

  // Local state to prevent DnD flicker
  const [localTasks, setLocalTasks] = useState<Task[]>([]);

  // Sync local tasks with remote data
  // eslint-disable-next-line react-hooks/exhaustive-deps
  useEffect(() => {
    if (project?.tasks) {
      setLocalTasks(project.tasks);
    }
  }, [project?.tasks]);

  // Dialog state
  const [isDialogOpen, setIsDialogOpen] = useState(false);
  const [editingTask, setEditingTask] = useState<Task | null>(null);
  const [isViewMode, setIsViewMode] = useState(false);

  // Delete Dialog state
  const [taskToDelete, setTaskToDelete] = useState<string | null>(null);

  if (isError) {
    toast.error('Failed to load project details');
  }

  const handleDragEnd = (result: DropResult) => {
    if (!result.destination) return;

    const { source, destination, draggableId } = result;
    
    if (source.droppableId === destination.droppableId && source.index === destination.index) {
      return;
    }

    const newStatus = destination.droppableId as TaskStatus;

    // Immediately update local UI so it doesn't snap back to original position
    const previousTasks = [...localTasks];
    setLocalTasks(prev => prev.map(t => t.id === draggableId ? { ...t, status: newStatus } : t));

    updateTask.mutate({ taskId: draggableId, updates: { status: newStatus } }, {
      onError: () => {
        // Rollback local state if API fails
        setLocalTasks(previousTasks);
        toast.error('Failed to move task');
      }
    });
  };

  const handleSaveTask = async (taskData: Partial<Task>) => {
    if (editingTask) {
      updateTask.mutate({ taskId: editingTask.id, updates: taskData }, {
        onSuccess: () => {
          toast.success('Task updated');
          setIsDialogOpen(false);
        },
        onError: () => toast.error('Failed to update task')
      });
    } else {
      createTask.mutate(taskData, {
        onSuccess: () => {
          toast.success('Task created');
          setIsDialogOpen(false);
        },
        onError: () => toast.error('Failed to create task')
      });
    }
  };

  const handleQuickUpdate = (taskId: string, updates: Partial<Task>) => {
    updateTask.mutate({ taskId, updates }, {
      onError: () => toast.error('Failed to update task')
    });
  };

  const confirmDeleteTask = () => {
    if (!taskToDelete) return;
    deleteTask.mutate(taskToDelete, {
      onSuccess: () => {
        toast.success('Task deleted');
        setTaskToDelete(null);
      },
      onError: () => {
        toast.error('Failed to delete task');
        setTaskToDelete(null);
      }
    });
  };

  const handleDeleteTask = (taskId: string) => {
    setTaskToDelete(taskId);
  };

  const openCreateDialog = () => {
    setEditingTask(null);
    setIsViewMode(false);
    setIsDialogOpen(true);
  };

  const openEditDialog = (task: Task) => {
    setEditingTask(task);
    setIsViewMode(false);
    setIsDialogOpen(true);
  };

  const openViewDialog = (task: Task) => {
    setEditingTask(task);
    setIsViewMode(true);
    setIsDialogOpen(true);
  };

  if (isLoading) {
    return (
      <div className="flex flex-col h-[calc(100vh-3.5rem)] overflow-hidden p-6 gap-6">
        <div className="flex justify-between items-start">
          <div>
            <div className="h-8 w-[250px] mb-2 bg-slate-200 animate-pulse rounded" />
            <div className="h-4 w-[400px] bg-slate-200 animate-pulse rounded" />
          </div>
          <div className="h-10 w-[120px] bg-slate-200 animate-pulse rounded" />
        </div>
        <div className="flex gap-6 h-full items-start">
          <div className="w-80 h-full rounded-xl bg-slate-200 animate-pulse" />
          <div className="w-80 h-full rounded-xl bg-slate-200 animate-pulse" />
          <div className="w-80 h-full rounded-xl bg-slate-200 animate-pulse" />
        </div>
      </div>
    );
  }

  if (!project) return <div className="text-center py-10">Project not found</div>;

  return (
    <div className="flex flex-col h-[calc(100vh-3.5rem)] overflow-hidden">
      {/* Project Header */}
      <div className="border-b bg-background px-6 py-4 flex justify-between items-start shrink-0">
        <div>
          <h1 className="text-2xl font-bold">{project.name}</h1>
          {project.description && (
            <p className="text-muted-foreground mt-1">{project.description}</p>
          )}
        </div>
        <Button onClick={openCreateDialog}>
          <Plus className="mr-2 h-4 w-4" />
          Add Task
        </Button>
      </div>

      {/* Board */}
      <div className="flex-1 overflow-x-auto overflow-y-hidden bg-muted/20 p-6">
        <DragDropContext onDragEnd={handleDragEnd}>
          <div className="flex gap-6 h-full items-start">
            {TASK_STATUSES.map(column => (
              <KanbanColumn
                key={column.id}
                id={column.id}
                title={column.label}
                tasks={localTasks.filter(t => t.status === column.id)}
                onView={openViewDialog}
                onEdit={openEditDialog}
                onDelete={handleDeleteTask}
                onQuickUpdate={handleQuickUpdate}
              />
            ))}
          </div>
        </DragDropContext>
      </div>

      <TaskEditDialog
        open={isDialogOpen && !isViewMode}
        onOpenChange={(val) => { if (!val) setIsDialogOpen(false); }}
        task={editingTask}
        onSave={handleSaveTask}
      />

      <TaskViewDialog
        open={isDialogOpen && isViewMode}
        onOpenChange={(val) => { if (!val) setIsDialogOpen(false); }}
        task={editingTask}
      />

      <AlertDialog open={!!taskToDelete} onOpenChange={() => setTaskToDelete(null)}>
        <AlertDialogContent className="sm:max-w-106.25">
          <AlertDialogHeader>
            <AlertDialogTitle>Are you absolutely sure?</AlertDialogTitle>
            <AlertDialogDescription>
              This action cannot be undone. This will permanently delete the task and remove its data from our servers.
            </AlertDialogDescription>
          </AlertDialogHeader>
          <AlertDialogFooter>
            <AlertDialogCancel>Cancel</AlertDialogCancel>
            <AlertDialogAction className="bg-destructive text-destructive-foreground hover:bg-destructive/90" onClick={confirmDeleteTask}>
              Continue
            </AlertDialogAction>
          </AlertDialogFooter>
        </AlertDialogContent>
      </AlertDialog>
    </div>
  );
}
