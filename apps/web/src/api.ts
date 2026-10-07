export type ApiTrace<T> = {
  data: T;
  endpoint: string;
  method: string;
  request: unknown;
  response: T;
  durationMs: number;
};

export async function api<T>(
  path: string,
  options?: RequestInit
): Promise<T> {
  const response = await fetch(path, {
    ...options,
    headers: {
      "Content-Type": "application/json",
      ...(options?.headers ?? {})
    }
  });

  if (!response.ok) {
    let detail = `Request failed with status ${response.status}`;
    try {
      const body = await response.json();
      detail = body.detail ?? detail;
    } catch {
      // Keep the HTTP status fallback.
    }
    throw new Error(detail);
  }

  return response.json() as Promise<T>;
}

export async function apiTrace<T>(
  path: string,
  options?: RequestInit
): Promise<ApiTrace<T>> {
  const started = performance.now();
  const data = await api<T>(path, options);

  let request: unknown = null;
  if (typeof options?.body === "string" && options.body.length > 0) {
    try {
      request = JSON.parse(options.body);
    } catch {
      request = options.body;
    }
  }

  return {
    data,
    endpoint: path,
    method: options?.method ?? "GET",
    request,
    response: data,
    durationMs: performance.now() - started
  };
}
