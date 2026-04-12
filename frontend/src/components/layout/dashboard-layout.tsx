import { Outlet, Navigate } from 'react-router';
import { useAuthStore } from '../../store/useAuthStore';
import { Navbar } from './navbar';
import { Toaster } from '@/components/ui/sonner';

export default function Layout() {
  const { user } = useAuthStore();

  if (!user) {
    return <Navigate to="/login" replace />;
  }

  return (
    <div className="min-h-screen bg-background flex flex-col font-sans">
      <Navbar />
      <main className="flex-1">
        <Outlet />
      </main>
      <Toaster position="bottom-right" />
    </div>
  );
}
