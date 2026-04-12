import { useState } from 'react';
import { useNavigate } from 'react-router';
import { Plus, MoreVertical, FolderOpen, Clock } from 'lucide-react';
import { useProjects, useCreateProject, useUpdateProject, useDeleteProject, useUsers } from '@/api/queries';
import { formatDateTime, getInitials } from '@/lib/utils';
import { Button } from '@/components/ui/button';
import { Card, CardDescription, CardTitle } from '@/components/ui/card';
import { Dialog, DialogContent, DialogDescription, DialogFooter, DialogHeader, DialogTitle } from '@/components/ui/dialog';
import { DropdownMenu, DropdownMenuContent, DropdownMenuItem, DropdownMenuTrigger } from '@/components/ui/dropdown-menu';
import { AlertDialog, AlertDialogAction, AlertDialogCancel, AlertDialogContent, AlertDialogDescription, AlertDialogFooter, AlertDialogHeader, AlertDialogTitle } from '@/components/ui/alert-dialog';
import { Input } from '@/components/ui/input';
import { Textarea } from '@/components/ui/textarea';
import { Label } from '@/components/ui/label';
import { toast } from 'sonner';
import { Skeleton } from '@/components/ui/skeleton';
import { useAuthStore } from '@/store/useAuthStore';
import type { Project } from '@/types';

export default function Dashboard() {
  const { data: projects = [], isLoading, isError } = useProjects();
  const { data: users = [] } = useUsers();
  
  const createProject = useCreateProject();
  const updateProject = useUpdateProject();
  const deleteProject = useDeleteProject();
  const { user } = useAuthStore();
  
  const [isDialogOpen, setIsDialogOpen] = useState(false);
  const [editingProject, setEditingProject] = useState<Project | null>(null);
  const [projectToDelete, setProjectToDelete] = useState<string | null>(null);

  const [newProjectName, setNewProjectName] = useState('');
  const [newProjectDesc, setNewProjectDesc] = useState('');
  
  const navigate = useNavigate();

  const openCreateDialog = () => {
    setEditingProject(null);
    setNewProjectName('');
    setNewProjectDesc('');
    setIsDialogOpen(true);
  };

  const openEditDialog = (e: React.MouseEvent, project: Project) => {
    e.stopPropagation();
    setEditingProject(project);
    setNewProjectName(project.name);
    setNewProjectDesc(project.description || '');
    setIsDialogOpen(true);
  };

  if (isError) {
    toast.error('Failed to load projects');
  }

  const handleSaveProject = async (e: React.SyntheticEvent) => {
    e.preventDefault();
    if (!newProjectName.trim()) return;

    if (editingProject) {
      updateProject.mutate(
        { id: editingProject.id, updates: { name: newProjectName, description: newProjectDesc } },
        {
          onSuccess: () => {
            setIsDialogOpen(false);
            toast.success('Project updated successfully');
          },
          onError: () => toast.error('Failed to update project'),
        }
      );
    } else {
      createProject.mutate(
        { name: newProjectName, description: newProjectDesc },
        {
          onSuccess: () => {
            setIsDialogOpen(false);
            toast.success('Project created successfully');
          },
          onError: () => toast.error('Failed to create project'),
        }
      );
    }
  };

  const confirmDeleteProject = () => {
    if (!projectToDelete) return;
    deleteProject.mutate(projectToDelete, {
      onSuccess: () => {
        toast.success('Project deleted');
        setProjectToDelete(null);
      },
      onError: () => {
        toast.error('Failed to delete project');
        setProjectToDelete(null);
      }
    });
  };

  if (isLoading) {
    return (
      <div className="container p-6 mx-auto max-w-6xl">
        <Skeleton className="h-10 w-[150px] mb-6" />
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          <Skeleton className="h-[140px] w-full" />
          <Skeleton className="h-[140px] w-full" />
          <Skeleton className="h-[140px] w-full" />
        </div>
      </div>
    );
  }

  return (
    <div className="container p-6 mx-auto max-w-6xl">
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-3xl font-bold">Projects</h1>
        
        <Button onClick={openCreateDialog}>
          <Plus className="mr-2 h-4 w-4" />
          New Project
        </Button>
        <Dialog open={isDialogOpen} onOpenChange={setIsDialogOpen}>
          <DialogContent className="sm:max-w-106.25">
            <form onSubmit={handleSaveProject}>
              <DialogHeader>
                <DialogTitle>{editingProject ? 'Edit Project' : 'Create Project'}</DialogTitle>
                <DialogDescription>
                  {editingProject ? 'Update project details.' : 'Add a new project to your workspace.'}
                </DialogDescription>
              </DialogHeader>
              <div className="grid gap-4 py-4">
                <div className="grid gap-2">
                  <Label htmlFor="name">Name</Label>
                  <Input
                    id="name"
                    value={newProjectName}
                    onChange={(e) => setNewProjectName(e.target.value)}
                    required
                    placeholder="E.g. Website Redesign"
                  />
                </div>
                <div className="grid gap-2">
                  <Label htmlFor="description">Description</Label>
                  <Textarea
                    id="description"
                    value={newProjectDesc}
                    onChange={(e) => setNewProjectDesc(e.target.value)}
                    placeholder="Optional details about this project..."
                    rows={4}
                  />
                </div>
              </div>
              <DialogFooter>
                <Button type="button" variant="outline" onClick={() => setIsDialogOpen(false)}>
                  Cancel
                </Button>
                <Button type="submit" disabled={createProject.isPending || updateProject.isPending}>
                  {createProject.isPending || updateProject.isPending ? 'Saving...' : 'Save Project'}
                </Button>
              </DialogFooter>
            </form>
          </DialogContent>
        </Dialog>
      </div>

      {projects.length === 0 ? (
        <div className="text-center py-20 bg-muted/50 rounded-lg border border-dashed">
          <h3 className="text-lg font-medium mb-2">No projects yet</h3>
          <p className="text-muted-foreground mb-4">Create a project to start managing your tasks.</p>
          <Button onClick={openCreateDialog}>
            <Plus className="mr-2 h-4 w-4" />
            Create Project
          </Button>
        </div>
      ) : (
        <div className="flex flex-col gap-3">
          {projects.map((project) => {
            const ownerName = users.find(u => u.id === project.owner_id)?.name || 'Unknown User';
            const isOwner = user?.id === project.owner_id;
            
            return (
              <Card 
                key={project.id} 
                className="group cursor-pointer border-border/50 hover:border-primary/50 hover:shadow-md transition-all rounded-lg overflow-hidden flex flex-row items-center bg-card pr-4"
                onClick={() => navigate(`/projects/${project.id}`)}
              >
                {/* Visual Left Accent */}
                <div className="w-1.5 self-stretch bg-primary/20 group-hover:bg-primary/60 transition-colors shrink-0" />
                
                {/* Main Content Area */}
                <div className="flex flex-col sm:flex-row flex-1 items-start sm:items-center py-4 px-5 gap-4">
                  {/* Title & Description block */}
                  <div className="flex-1 min-w-0">
                    <CardTitle className="text-base font-bold flex items-center gap-2 mb-1.5">
                      <FolderOpen className="h-4 w-4 text-primary/70 shrink-0" />
                      <span className="truncate">{project.name}</span>
                      {isOwner && (
                        <span className="ml-2 px-2 py-0.5 rounded text-[10px] font-semibold bg-primary/10 text-primary border border-primary/20 uppercase tracking-wider shrink-0">
                          Owner
                        </span>
                      )}
                    </CardTitle>
                    {project.description ? (
                      <CardDescription className="line-clamp-1 text-sm text-muted-foreground/80 max-w-2xl">
                        {project.description}
                      </CardDescription>
                    ) : (
                      <CardDescription className="text-sm text-muted-foreground/50 italic">
                        No description provided.
                      </CardDescription>
                    )}
                  </div>

                  {/* Metadata Block */}
                  <div className="flex items-center gap-6 sm:gap-8 shrink-0 text-sm text-muted-foreground border-t sm:border-t-0 sm:border-l border-border/40 pt-3 sm:pt-0 sm:pl-8 w-full sm:w-auto">
                    <div className="flex items-center gap-2" title="Project Owner">
                      <div className="h-7 w-7 rounded-full bg-primary/10 border border-primary/20 flex items-center justify-center shrink-0 text-primary font-bold text-xs uppercase">
                        {getInitials(ownerName)}
                      </div>
                      <div className="flex flex-col">
                        <span className="text-[10px] uppercase font-semibold text-muted-foreground/60 leading-none mb-0.5">Owner</span>
                        <span className="font-medium text-foreground/80 truncate max-w-[120px] leading-none">
                          {isOwner ? 'You' : ownerName}
                        </span>
                      </div>
                    </div>

                    <div className="flex items-center gap-2" title="Created At">
                      <div className="h-7 w-7 rounded-full bg-muted border border-border/40 flex items-center justify-center shrink-0 text-muted-foreground">
                        <Clock className="h-3.5 w-3.5" />
                      </div>
                      <div className="flex flex-col">
                        <span className="text-[10px] uppercase font-semibold text-muted-foreground/60 leading-none mb-0.5">Created</span>
                        <span className="font-medium text-foreground/80 leading-none">
                          {formatDateTime(project.created_at).split(' • ')[0]}
                        </span>
                      </div>
                    </div>
                  </div>
                </div>
                
                {/* Dropdown Menu (Only visible to owner) */}
                {isOwner ? (
                  <DropdownMenu>
                    <DropdownMenuTrigger asChild>
                      <Button 
                        variant="ghost" 
                        size="icon"
                        className="h-8 w-8 text-muted-foreground hover:bg-muted hover:text-foreground opacity-0 group-hover:opacity-100 transition-opacity shrink-0 ml-2" 
                        onClick={(e) => e.stopPropagation()}
                      >
                        <span className="sr-only">Open menu</span>
                        <MoreVertical className="h-4 w-4" />
                      </Button>
                    </DropdownMenuTrigger>
                    <DropdownMenuContent align="end" className="w-40">
                      <DropdownMenuItem onClick={(e) => openEditDialog(e, project)}>
                        Edit Project
                      </DropdownMenuItem>
                      <DropdownMenuItem 
                        className="text-destructive focus:text-destructive"
                        onClick={(e) => { e.stopPropagation(); setProjectToDelete(project.id); }}
                      >
                        Delete Project
                      </DropdownMenuItem>
                    </DropdownMenuContent>
                  </DropdownMenu>
                ) : (
                  <div className="w-8 shrink-0 ml-2" /> /* Placeholder to match width */
                )}
              </Card>
            );
          })}
        </div>
      )}

      <AlertDialog open={!!projectToDelete} onOpenChange={() => setProjectToDelete(null)}>
        <AlertDialogContent className="sm:max-w-106.25">
          <AlertDialogHeader>
            <AlertDialogTitle>Are you absolutely sure?</AlertDialogTitle>
            <AlertDialogDescription>
              This action cannot be undone. This will permanently delete the project and remove all its tasks from our servers.
            </AlertDialogDescription>
          </AlertDialogHeader>
          <AlertDialogFooter>
            <AlertDialogCancel>Cancel</AlertDialogCancel>
            <AlertDialogAction className="bg-destructive text-destructive-foreground hover:bg-destructive/90" onClick={confirmDeleteProject}>
              Delete Project
            </AlertDialogAction>
          </AlertDialogFooter>
        </AlertDialogContent>
      </AlertDialog>
    </div>
  );
}
