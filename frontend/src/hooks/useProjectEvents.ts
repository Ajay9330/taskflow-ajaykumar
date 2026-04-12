import { useEffect } from 'react';
import { useQueryClient } from '@tanstack/react-query';
import { useAuthStore } from '../store/useAuthStore';

export function useProjectEvents(projectId?: string) {
  const queryClient = useQueryClient();
  const token = useAuthStore(state => state.token);

  useEffect(() => {
    if (!projectId || !token) return;

    const apiUrl = import.meta.env.VITE_API_URL || 'http://localhost:8000';
    const eventSource = new EventSource(`${apiUrl}/projects/${projectId}/events?token=${token}`);

    eventSource.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data);
        const payloadType = data.payload?.type || data.type;
        if (payloadType === 'task_created' || payloadType === 'task_updated' || payloadType === 'task_deleted') {
          queryClient.invalidateQueries({ queryKey: ['projects', projectId] });
        }
      } catch (err) {
        console.error('Failed to parse SSE message', err);
      }
    };

    eventSource.onerror = (error) => {
      console.error('SSE Error:', error);
      eventSource.close();
    };

    return () => {
      eventSource.close();
    };
  }, [projectId, token, queryClient]);
}