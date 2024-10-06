import { type ClassValue, clsx } from "clsx";
import { twMerge } from "tailwind-merge";

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

export function valueUpdater<T>(
  updaterOrValue: T | ((old: T) => T),
  stateRef: { value: T },
) {
  if (typeof updaterOrValue === "function") {
    // Type assertion here to let TypeScript know that it's a function
    stateRef.value = (updaterOrValue as (old: T) => T)(stateRef.value);
  } else {
    stateRef.value = updaterOrValue;
  }
}
