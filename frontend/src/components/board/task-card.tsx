import { useState } from 'react';
import { CalendarIcon, Edit2, Trash2, Clock, User, Check, Eye } from 'lucide-react';
import { type TaskStatus, type TaskPriority } from '@/types';
import { TASK_STATUSES, TASK_PRIORITIES } from '@/constants/index';
import { Card, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { Popover, PopoverContent, PopoverTrigger } from '@/components/ui/popover';
import { Command, CommandEmpty, CommandGroup, CommandInput, CommandItem, CommandList } from '@/components/ui/command';
import { useUsers } from '@/hooks/api/useQueries';
import { cn, getShortId, getInitials, formatCompactDate, formatDateTime } from '@/lib/utils';
import type { TaskCardProps } from '@/types/components';

export function TaskCard({ task, onView, onEdit, onDelete, onQuickUpdate }: TaskCardProps) {
  const { data: users = [] } = useUsers();
  const [assigneeOpen, setAssigneeOpen] = useState(false);
  const [isEditingTitle, setIsEditingTitle] = useState(false);
  const [tempTitle, setTempTitle] = useState(task.title);

  const handleTitleSubmit = () => {
    if (tempTitle.trim() && tempTitle !== task.title) {
      onQuickUpdate(task.id, { title: tempTitle });
    } else {
      setTempTitle(task.title);
    }
    setIsEditingTitle(false);
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter') handleTitleSubmit();
    if (e.key === 'Escape') {
      setTempTitle(task.title);
      setIsEditingTitle(false);
    }
  };

  const assigneeName = task.assignee_id ? (users.find(u => u.id === task.assignee_id)?.name || 'Unknown') : 'Unassigned';

  return (
    <Card className="group relative mb-2 bg-card border-border/60 hover:border-primary/40 hover:shadow transition-all rounded-md overflow-hidden cursor-grab active:cursor-grabbing">
      
      {/* Top Priority Bar Indicator */}
      <div className={cn(
        "h-0.5 w-full absolute top-0 left-0",
        task.priority === 'high' ? "bg-red-500" : task.priority === 'medium' ? "bg-yellow-500" : "bg-blue-500"
      )} />

      <div className="p-2.5 flex flex-col gap-1.5">
        
        {/* Ticket ID & Top Actions */}
        <div className="flex items-center justify-between w-full">
          <span className="text-[10px] font-mono font-semibold text-muted-foreground/80 px-1 bg-muted/50 rounded-sm tracking-wider">
            TSK-{getShortId(task.id)}
          </span>
          
          {/* Quick Actions */}
          <div className="flex items-center gap-1.5 opacity-0 group-hover:opacity-100 transition-opacity bg-background/95 backdrop-blur rounded-md absolute top-1 right-1 z-10 p-1 shadow-sm border border-border/60">
            <Button variant="outline" size="icon" className="h-6 w-6 text-muted-foreground hover:text-primary hover:bg-primary/10" onClick={() => onView(task)} title="View Task Details">
              <Eye className="h-3.5 w-3.5" />
            </Button>
            <Button variant="outline" size="icon" className="h-6 w-6 text-muted-foreground hover:text-primary hover:bg-primary/10" onClick={() => onEdit(task)} title="Edit Task">
              <Edit2 className="h-3.5 w-3.5" />
            </Button>
            <Button variant="outline" size="icon" className="h-6 w-6 text-muted-foreground hover:text-destructive hover:bg-destructive/10" onClick={() => onDelete(task.id)} title="Delete Task">
              <Trash2 className="h-3.5 w-3.5" />
            </Button>
          </div>
        </div>

        {/* Title */}
        <div className="relative">
          {isEditingTitle ? (
            <Input
              autoFocus
              className="h-6 text-xs font-semibold px-1.5 py-0 w-full"
              value={tempTitle}
              onChange={(e) => setTempTitle(e.target.value)}
              onBlur={handleTitleSubmit}
              onKeyDown={handleKeyDown}
            />
          ) : (
            <CardTitle 
              className="text-xs font-semibold leading-tight wrap-break-word pr-8 cursor-text hover:text-primary transition-colors"
              onClick={() => setIsEditingTitle(true)}
              title="Click to edit title"
            >
              {task.title}
            </CardTitle>
          )}
        </div>

        {/* Description (Truncated tightly) */}
        {task.description && (
          <p className="text-[11px] text-muted-foreground line-clamp-2 leading-snug">
            {task.description}
          </p>
        )}

        {/* Status & Priority Selectors */}
        <div className="flex flex-wrap items-center gap-1 mt-0.5">
          <Select value={task.status} onValueChange={(val: TaskStatus) => onQuickUpdate(task.id, { status: val })}>
            <SelectTrigger className={cn(
              "h-5 text-[10px] w-auto px-1.5 py-0 border-transparent rounded-[3px] font-semibold uppercase tracking-wide focus:ring-0",
              task.status === 'done' ? "bg-emerald-500/15 text-emerald-600 dark:text-emerald-400" :
              task.status === 'in_progress' ? "bg-blue-500/15 text-blue-600 dark:text-blue-400" :
              "bg-slate-500/15 text-slate-600 dark:text-slate-400"
            )}>
              <SelectValue />
            </SelectTrigger>
            <SelectContent>
              {TASK_STATUSES.map((s) => (
                <SelectItem key={s.id} value={s.id} className="text-[10px] font-medium uppercase">{s.label}</SelectItem>
              ))}
            </SelectContent>
          </Select>

          <Select value={task.priority} onValueChange={(val: TaskPriority) => onQuickUpdate(task.id, { priority: val })}>
            <SelectTrigger className={cn(
              "h-5 text-[10px] w-auto px-1.5 py-0 border-dashed rounded-[3px] font-medium uppercase focus:ring-0",
              task.priority === 'high' ? 'text-red-500 border-red-500/30' : 
              task.priority === 'medium' ? 'text-yellow-600 border-yellow-500/30' : 
              'text-blue-500 border-blue-500/30'
            )}>
              <SelectValue />
            </SelectTrigger>
            <SelectContent>
              {TASK_PRIORITIES.map((p) => (
                <SelectItem key={p.id} value={p.id} className="text-[10px] font-medium uppercase">{p.label}</SelectItem>
              ))}
            </SelectContent>
          </Select>
        </div>

        {/* Footer: User Avatar & Minimal Dates inline */}
        <div className="flex items-center justify-between mt-1 pt-1.5 border-t border-border/40">
          <Popover open={assigneeOpen} onOpenChange={setAssigneeOpen}>
            <PopoverTrigger asChild>
              <div className="flex items-center gap-1.5 cursor-pointer hover:bg-muted/50 rounded pr-1.5 py-0.5 transition-colors">
                <div className="h-5 w-5 rounded-full bg-primary/10 border border-primary/20 flex items-center justify-center shrink-0 overflow-hidden text-primary font-bold text-[10px]">
                  {task.assignee_id && assigneeName !== 'Unknown' && assigneeName !== 'Unassigned' ? (
                    getInitials(assigneeName)
                  ) : (
                    <User className="h-3 w-3 text-primary/70" />
                  )}
                </div>
                <span className="text-[11px] font-medium text-foreground/80 max-w-[80px] truncate">
                  {assigneeName}
                </span>
              </div>
            </PopoverTrigger>
            <PopoverContent className="w-[200px] p-0" align="start">
              <Command>
                <CommandInput placeholder="Assign to..." className="h-7 text-xs" />
                <CommandList>
                  <CommandEmpty className="text-xs py-2 text-center text-muted-foreground">No users found.</CommandEmpty>
                  <CommandGroup>
                    <CommandItem value="unassigned" className="text-xs" onSelect={() => { onQuickUpdate(task.id, { assignee_id: null }); setAssigneeOpen(false); }}>
                      <Check className={cn("mr-2 h-3 w-3", !task.assignee_id ? "opacity-100" : "opacity-0")} />
                      Unassigned
                    </CommandItem>
                    {users.map((user) => (
                      <CommandItem key={user.id} value={user.name} className="text-xs" onSelect={() => { onQuickUpdate(task.id, { assignee_id: user.id }); setAssigneeOpen(false); }}>
                        <Check className={cn("mr-2 h-3 w-3", task.assignee_id === user.id ? "opacity-100" : "opacity-0")} />
                        <div className="flex flex-col">
                          <span className="truncate w-full font-medium">{user.name}</span>
                          <span className="text-[9px] text-muted-foreground opacity-80">{user.email}</span>
                        </div>
                      </CommandItem>
                    ))}
                  </CommandGroup>
                </CommandList>
              </Command>
            </PopoverContent>
          </Popover>

          <div className="flex items-center">
            {task.due_date ? (
              <div className="flex items-center gap-1.5 text-[10px] font-medium text-destructive bg-destructive/10 px-1.5 py-0.5 rounded flex-shrink-0" title="Due Date">
                <CalendarIcon className="h-3 w-3" />
                {formatCompactDate(task.due_date)}
              </div>
            ) : (
              <div className="flex items-center gap-1.5 text-[9px] text-muted-foreground/70 font-medium flex-shrink-0" title="Created At">
                <Clock className="h-3 w-3" />
                {formatDateTime(task.created_at)}
              </div>
            )}
          </div>
        </div>

      </div>
    </Card>
  );
}
