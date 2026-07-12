import React, { createContext, useState, useEffect, useContext } from 'react';
import { loginUser, logoutUser, restoreAuthSession, type UserSession } from '../services/transitApi';

interface AuthContextType {
  user: UserSession | null;
  isLoggedIn: boolean;
  isReady: boolean;
  login: (email: string, role: 'Admin' | 'Driver', name?: string, driverId?: string, password?: string) => Promise<void>;
  logout: () => Promise<void>;
  hasPermission: (action: 'create' | 'read' | 'update' | 'delete', resource: string) => boolean;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [user, setUser] = useState<UserSession | null>(null);
  const [isLoggedIn, setIsLoggedIn] = useState<boolean>(false);
  const [isReady, setIsReady] = useState<boolean>(false);

  useEffect(() => {
    let cancelled = false;

    const restoreSession = async () => {
      const savedSession = await restoreAuthSession();
      if (cancelled) return;

      if (savedSession) {
        setUser(savedSession);
        setIsLoggedIn(true);
      }

      setIsReady(true);
    };

    restoreSession();

    return () => {
      cancelled = true;
    };
  }, []);

  const login = async (email: string, role: 'Admin' | 'Driver', name?: string, driverId?: string, password?: string) => {
    const displayName = name || (role === 'Admin' ? 'James Donovan' : 'Alex Rivera');
    const actualDriverId = driverId || (role === 'Driver' ? 'd-alex' : undefined);
    const session = await loginUser({
      email,
      role,
      name: displayName,
      driverId: actualDriverId,
      password,
    });
    setUser(session);
    setIsLoggedIn(true);
  };

  const logout = async () => {
    await logoutUser();
    setUser(null);
    setIsLoggedIn(false);
  };

  const hasPermission = (action: 'create' | 'read' | 'update' | 'delete', resource: string) => {
    if (!isLoggedIn || !user) return false;
    if (user.role === 'Admin') return true;
    
    if (user.role === 'Driver') {
      // Driver can only read: vehicles, trips, profile, fuel, notifications
      if (action === 'read') {
        return ['vehicles', 'trips', 'profile', 'fuel', 'notifications', 'dashboard'].includes(resource);
      }
      // Driver can only create fuel logs
      if (action === 'create' && resource === 'fuel') {
        return true;
      }
      return false;
    }
    return false;
  };

  return (
    <AuthContext.Provider value={{ user, isLoggedIn, isReady, login, logout, hasPermission }}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
}
