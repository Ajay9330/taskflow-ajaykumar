import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import apiClient from './client';
import type { Project, Task } from '../types';

// Users
export const useUsers = () => {
  return useQuery({
    queryKey: ['users'],
    queryFn: async () => {
      const { data } = await apiClient.get('/users');
      return data.users as { id: string; name: string; email: string }[];
    },
  });
};

// Projects
export const useProjects = () => {
  return useQuery({
    queryKey: ['projects'],
    queryFn: async () => {
      const { data } = await apiClient.get('/projects');
      return data.projects as Project[];
    },
  });
};

export const useCreateProject = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: async (newProject: { name: string; description?: string }) => {
      const { data } = await apiClient.post('/projects', newProject);
      return data as Project;
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['projects'] });
    },
  });
};

export const useUpdateProject = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: async ({ id, updates }: { id: string; updates: { name?: string; description?: string } }) => {
      const { data } = await apiClient.patch(`/projects/${id}`, updates);
      return data as Project;
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['projects'] });
    },
  });
};

export const useDeleteProject = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: async (id: string) => {
      await apiClient.delete(`/projects/${id}`);
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['projects'] });
    },
  });
};

export const useProjectDetails = (id?: string) => {
  return useQuery({
    queryKey: ['projects', id],
    queryFn: async () => {
      const { data } = await apiClient.get(`/projects/${id}`);
      return data as Project & { tasks: Task[] };
    },
    enabled: !!id,
  });
};

// Tasks
export const useCreateTask = (projectId?: string) => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: async (newTask: Partial<Task>) => {
      const { data } = await apiClient.post(`/projects/${projectId}/tasks`, newTask);
      return data as Task;
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['projects', projectId] });
    },
  });
};

export const useUpdateTask = (projectId?: string) => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: async ({ taskId, updates }: { taskId: string; updates: Partial<Task> }) => {
      const { data } = await apiClient.patch(`/tasks/${taskId}`, updates);
      return data as Task;
    },
    onMutate: async ({ taskId, updates }) => {
      await queryClient.cancelQueries({ queryKey: ['projects', projectId] });
      const previousProject = queryClient.getQueryData(['projects', projectId]);

      queryClient.setQueryData(['projects', projectId], (old: any) => {
        if (!old) return old;

        // Ensure we explicitly map through without losing the array reference
        const updatedTasks = old.tasks.map((t: Task) => 
          t.id === taskId ? { ...t, ...updates } : t
        );

        return { ...old, tasks: updatedTasks };
      });

      return { previousProject };
    },
    onError: (_err, _variables, context) => {
      if (context?.previousProject) {
        queryClient.setQueryData(['projects', projectId], context.previousProject);
      }
    },
  });
};

export const useDeleteTask = (projectId?: string) => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: async (taskId: string) => {
      await apiClient.delete(`/tasks/${taskId}`);
      return taskId;
    },
    onSuccess: (taskId) => {
      queryClient.setQueryData(['projects', projectId], (old: any) => {
        if (!old) return old;
        return {
          ...old,
          tasks: old.tasks.filter((t: Task) => t.id !== taskId),
        };
      });
    },
  });
};
