import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogDescription } from '@/components/ui/dialog';
import { Badge } from '@/components/ui/badge';
import { CalendarIcon, Clock, CheckCircle2, User } from 'lucide-react';
import type { Task } from '@/types';
import { useUsers } from '@/api/queries';
import { getShortId, getInitials, formatDateTime, formatFullDate, cn } from '@/lib/utils';

interface TaskViewDialogProps {
  open: boolean;
  onOpenChange: (open: boolean) => void;
  task?: Task | null;
}

export function TaskViewDialog({ open, onOpenChange, task }: TaskViewDialogProps) {
  const { data: users = [] } = useUsers();
  if (!task) return null;

  const assigneeName = task.assignee_id ? (users.find(u => u.id === task.assignee_id)?.name || 'Unknown') : 'Unassigned';
  const assigneeEmail = task.assignee_id ? (users.find(u => u.id === task.assignee_id)?.email || '') : '';
  const shortId = `TSK-${getShortId(task.id)}`;

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent className="sm:max-w-2xl">
        <DialogHeader className="border-b pb-4 mb-4">
          <div className="flex items-center gap-3 mb-2">
            <span className="text-xs font-mono font-bold text-muted-foreground bg-muted px-2 py-1 rounded">
              {shortId}
            </span>
            <Badge variant="outline" className="uppercase tracking-wider text-[10px]">
              {task.status.replace('_', ' ')}
            </Badge>
            <Badge variant="secondary" className={cn(
              "uppercase tracking-wider text-[10px]",
              task.priority === 'high' ? 'bg-red-500/15 text-red-600' : task.priority === 'medium' ? 'bg-yellow-500/15 text-yellow-600' : 'bg-blue-500/15 text-blue-600'
            )}>
              {task.priority} priority
            </Badge>
          </div>
          <DialogTitle className="text-2xl leading-tight font-bold text-foreground">
            {task.title}
          </DialogTitle>
          <DialogDescription className="hidden">
            Task details for {shortId}
          </DialogDescription>
        </DialogHeader>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          
          {/* Main Content Area */}
          <div className="md:col-span-2 space-y-6">
            <div>
              <h4 className="text-sm font-semibold text-foreground/80 mb-2 uppercase tracking-wide">Description</h4>
              {task.description ? (
                <div className="bg-muted/30 border border-border/50 rounded-md p-4 text-sm text-muted-foreground whitespace-pre-wrap leading-relaxed">
                  {task.description}
                </div>
              ) : (
                <p className="text-sm text-muted-foreground italic">No description provided.</p>
              )}
            </div>
          </div>

          {/* Right Sidebar Metadata Area */}
          <div className="space-y-6">
            
            {/* Assignee Block */}
            <div className="bg-muted/10 border border-border/40 rounded-lg p-4">
              <h4 className="text-xs font-semibold text-muted-foreground mb-3 uppercase tracking-wide">Assignee</h4>
              <div className="flex items-center gap-3">
                <div className="h-10 w-10 rounded-full bg-primary/10 border border-primary/20 flex items-center justify-center shrink-0 overflow-hidden text-primary font-bold text-sm">
                  {task.assignee_id && assigneeName !== 'Unknown' && assigneeName !== 'Unassigned' ? (
                    getInitials(assigneeName)
                  ) : (
                    <User className="h-5 w-5 text-primary/70" />
                  )}
                </div>
                <div className="flex flex-col">
                  <span className="font-semibold text-sm leading-none mb-1">{assigneeName}</span>
                  {assigneeEmail && <span className="text-xs text-muted-foreground truncate max-w-[140px]">{assigneeEmail}</span>}
                </div>
              </div>
            </div>

            {/* Dates Block */}
            <div className="bg-muted/10 border border-border/40 rounded-lg p-4 space-y-4">
              
              {task.due_date && (
                <div>
                  <h4 className="text-xs font-semibold text-muted-foreground mb-1.5 uppercase tracking-wide">Due Date</h4>
                  <div className="flex items-center gap-2 text-sm font-medium text-destructive bg-destructive/10 border border-destructive/20 px-2 py-1.5 rounded-md w-fit">
                    <CalendarIcon className="h-4 w-4" />
                    {formatFullDate(task.due_date)}
                  </div>
                </div>
              )}

              <div>
                <h4 className="text-xs font-semibold text-muted-foreground mb-1.5 uppercase tracking-wide">Created</h4>
                <div className="flex items-center gap-2 text-sm text-foreground/80">
                  <Clock className="h-4 w-4 text-muted-foreground" />
                  {formatDateTime(task.created_at)}
                </div>
              </div>

              {task.updated_at && task.updated_at !== task.created_at && (
                <div>
                  <h4 className="text-xs font-semibold text-muted-foreground mb-1.5 uppercase tracking-wide">Updated</h4>
                  <div className="flex items-center gap-2 text-sm text-foreground/80">
                    <CheckCircle2 className="h-4 w-4 text-muted-foreground" />
                    {formatDateTime(task.updated_at)}
                  </div>
                </div>
              )}

            </div>
          </div>
        </div>

      </DialogContent>
    </Dialog>
  );
}
