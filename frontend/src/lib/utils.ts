import { clsx, type ClassValue } from "clsx"
import { twMerge } from "tailwind-merge"
import { format } from "date-fns"

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs))
}

/**
 * Returns the first letter of a name capitalized.
 */
export function getInitials(name?: string): string {
  if (!name) return '?'
  return name.charAt(0).toUpperCase()
}

/**
 * Truncates a UUID to just the first segment for use as a Ticket ID.
 */
export function getShortId(id: string): string {
  if (!id) return ''
  return id.split('-')[0].toUpperCase()
}

/**
 * Formats a given UTC ISO string to a compact date representation.
 * (e.g. "Apr 12")
 */
export function formatCompactDate(dateString?: string): string {
  if (!dateString) return ''
  return format(new Date(dateString), 'MMM d')
}

/**
 * Formats a given UTC ISO string to a full date representation.
 * (e.g. "Apr 12, 2026")
 */
export function formatFullDate(dateString?: string): string {
  if (!dateString) return ''
  return format(new Date(dateString), 'MMM d, yyyy')
}

/**
 * Formats a given UTC ISO string to a full datetime representation.
 * (e.g. "Apr 12, 2026 • 2:30 PM")
 */
export function formatDateTime(dateString?: string): string {
  if (!dateString) return ''
  return format(new Date(dateString), 'MMM d, yyyy • h:mm a')
}
