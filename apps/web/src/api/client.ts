import type { Project } from "../types";

export async function listProjects(): Promise<Project[]> {
  const response = await fetch("/api/projects");
  if (!response.ok) {
    throw new Error(`Failed to load projects: ${response.status}`);
  }
  return response.json();
}
