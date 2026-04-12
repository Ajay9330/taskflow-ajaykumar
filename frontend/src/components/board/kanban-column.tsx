import { Droppable, Draggable } from '@hello-pangea/dnd';
import type { Task, TaskStatus } from '@/types';
import { Badge } from '@/components/ui/badge';
import { TaskCard } from './task-card';

interface KanbanColumnProps {
  id: TaskStatus;
  title: string;
  tasks: Task[];
  onView: (task: Task) => void;
  onEdit: (task: Task) => void;
  onDelete: (taskId: string) => void;
  onQuickUpdate: (taskId: string, updates: Partial<Task>) => void;
}

export function KanbanColumn({ id, title, tasks, onView, onEdit, onDelete, onQuickUpdate }: KanbanColumnProps) {
  return (
    <div className="shrink-0 w-[340px] flex flex-col h-full bg-muted/30 border border-border/40 rounded-xl overflow-hidden">
      {/* Column Header */}
      <div className="flex items-center justify-between p-4 bg-muted/40 border-b border-border/40 shrink-0">
        <h3 className="font-bold text-sm text-foreground/80 tracking-wide uppercase">{title}</h3>
        <Badge variant="secondary" className="font-semibold">{tasks.length}</Badge>
      </div>
      
      {/* Droppable Area */}
      <Droppable droppableId={id}>
        {(provided, snapshot) => (
          <div
            {...provided.droppableProps}
            ref={provided.innerRef}
            className={`flex-1 overflow-y-auto p-3 min-h-37.5 transition-colors ${
              snapshot.isDraggingOver ? 'bg-primary/5' : ''
            }`}
          >
            {tasks.map((task, index) => (
              <Draggable key={task.id} draggableId={task.id} index={index}>
                {(provided, snapshot) => (
                  <div
                    ref={provided.innerRef}
                    {...provided.draggableProps}
                    {...provided.dragHandleProps}
                    className={snapshot.isDragging ? 'shadow-lg ring-1 ring-primary rounded-xl' : ''}
                  >
                    <TaskCard 
                      task={task}
                      onView={onView}
                      onEdit={onEdit} 
                      onDelete={onDelete} 
                      onQuickUpdate={onQuickUpdate}
                    />
                  </div>
                )}
              </Draggable>
            ))}
            {provided.placeholder}
          </div>
        )}
      </Droppable>
    </div>
  );
}
