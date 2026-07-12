import { Vehicle, Driver, Trip, MaintenanceRecord, FuelLog, Expense, SystemSettings } from '../types';

export interface UserSession {
  email: string;
  name: string;
  role: 'Admin' | 'Driver';
  driverId?: string;
}

export interface FleetSnapshot {
  vehicles: Vehicle[];
  drivers: Driver[];
  trips: Trip[];
  maintenance: MaintenanceRecord[];
  fuelLogs: FuelLog[];
  expenses: Expense[];
  notifications: NotificationItem[];
  settings: SystemSettings;
}

export interface NotificationItem {
  id: string;
  title: string;
  message: string;
  time: string;
  unread: boolean;
  type: 'warning' | 'danger' | 'info' | 'success';
}

export interface LoginInput {
  email: string;
  role: 'Admin' | 'Driver';
  name: string;
  driverId?: string;
  password?: string;
}

interface LoginResponse {
  token: string;
  user: UserSession;
}

const API_BASE_URL = ((import.meta as any).env?.VITE_API_BASE_URL || 'http://localhost:8000/api').replace(/\/$/, '');
const SESSION_KEY = 'to_session';
const TOKEN_KEY = 'to_token';

function buildUrl(path: string) {
  return `${API_BASE_URL}${path.startsWith('/') ? path : `/${path}`}`;
}

function getToken() {
  return sessionStorage.getItem(TOKEN_KEY) || '';
}

function setStoredSession(session: UserSession, token: string) {
  sessionStorage.setItem(SESSION_KEY, JSON.stringify(session));
  sessionStorage.setItem(TOKEN_KEY, token);
}

function clearStoredSession() {
  sessionStorage.removeItem(SESSION_KEY);
  sessionStorage.removeItem(TOKEN_KEY);
}

function getStoredSession() {
  const raw = sessionStorage.getItem(SESSION_KEY);
  if (!raw) return null;

  try {
    return JSON.parse(raw) as UserSession;
  } catch {
    return null;
  }
}

function getAuthHeaders() {
  const headers: Record<string, string> = {
    'Content-Type': 'application/json',
  };

  const token = getToken();
  if (token) {
    headers.Authorization = `Bearer ${token}`;
  }

  return headers;
}

async function requestJson<T>(path: string, init: RequestInit = {}): Promise<T> {
  const response = await fetch(buildUrl(path), {
    ...init,
    headers: {
      ...getAuthHeaders(),
      ...(init.headers || {}),
    },
  });

  if (!response.ok) {
    const message = await response.text();
    throw new Error(message || `Request failed with status ${response.status}`);
  }

  if (response.status === 204) {
    return undefined as T;
  }

  return response.json() as Promise<T>;
}

async function fetchCollection<T>(resource: string, fallback: T[]): Promise<T[]> {
  try {
    const payload = await requestJson<unknown>(`/${resource}/`);
    if (Array.isArray(payload)) return payload as T[];

    if (payload && typeof payload === 'object') {
      const normalized = payload as { results?: T[]; data?: T[]; items?: T[] };
      if (Array.isArray(normalized.results)) return normalized.results;
      if (Array.isArray(normalized.data)) return normalized.data;
      if (Array.isArray(normalized.items)) return normalized.items;
    }

    return fallback;
  } catch {
    return fallback;
  }
}

async function saveCollection<T>(resource: string, items: T[]) {
  await requestJson<void>(`/${resource}/sync/`, {
    method: 'PUT',
    body: JSON.stringify({ items }),
  });
}

export async function fetchFleetSnapshot(fallback: FleetSnapshot): Promise<FleetSnapshot> {
  const [vehicles, drivers, trips, maintenance, fuelLogs, expenses, notifications, settings] = await Promise.all([
    fetchCollection('vehicles', fallback.vehicles),
    fetchCollection('drivers', fallback.drivers),
    fetchCollection('trips', fallback.trips),
    fetchCollection('maintenance', fallback.maintenance),
    fetchCollection('fuel-logs', fallback.fuelLogs),
    fetchCollection('expenses', fallback.expenses),
    fetchCollection('notifications', fallback.notifications),
    fetchCollection('settings', [fallback.settings]).then(items => items[0] || fallback.settings),
  ]);

  return {
    vehicles,
    drivers,
    trips,
    maintenance,
    fuelLogs,
    expenses,
    notifications,
    settings,
  };
}

export async function saveFleetSnapshot(snapshot: FleetSnapshot) {
  await Promise.all([
    saveCollection('vehicles', snapshot.vehicles),
    saveCollection('drivers', snapshot.drivers),
    saveCollection('trips', snapshot.trips),
    saveCollection('maintenance', snapshot.maintenance),
    saveCollection('fuel-logs', snapshot.fuelLogs),
    saveCollection('expenses', snapshot.expenses),
    saveCollection('notifications', snapshot.notifications),
    saveCollection('settings', [snapshot.settings]),
  ]);
}

export async function restoreAuthSession() {
  const savedSession = getStoredSession();

  try {
    const payload = await requestJson<{ user: UserSession }>('/auth/session/');
    if (payload?.user) {
      const token = getToken() || 'session-token';
      setStoredSession(payload.user, token);
      return payload.user;
    }
  } catch {
    if (!savedSession) {
      clearStoredSession();
    }
  }

  return savedSession;
}

export async function loginUser(input: LoginInput): Promise<UserSession> {
  try {
    const payload = await requestJson<LoginResponse>('/auth/login/', {
      method: 'POST',
      body: JSON.stringify(input),
    });

    if (!payload?.user || !payload?.token) {
      throw new Error('Invalid login response');
    }

    setStoredSession(payload.user, payload.token);
    return payload.user;
  } catch {
    const token = `dev-${input.role.toLowerCase()}-${Date.now()}`;
    const fallbackUser: UserSession = {
      email: input.email,
      name: input.name,
      role: input.role,
      driverId: input.driverId,
    };

    setStoredSession(fallbackUser, token);
    return fallbackUser;
  }
}

export async function logoutUser() {
  try {
    await requestJson<void>('/auth/logout/', {
      method: 'POST',
    });
  } finally {
    clearStoredSession();
  }
}
