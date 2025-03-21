import { clsx, type ClassValue } from 'clsx';
import { twMerge } from 'tailwind-merge';

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

export function formatDateUTC(date: Date) {
  return date.toLocaleDateString('en-US', {
    timeZone: 'UTC',
  });
}
