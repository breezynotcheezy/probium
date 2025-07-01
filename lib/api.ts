// Default to same-origin when no API URL is provided.
const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || ""

export interface ScanResult {
  id: string
  filename: string
  size: number
  detected_type: string
  mime_type: string
  confidence: number
  extension: string | null
  engines_used: string[]
  scan_time: string
  timestamp: string
  probium_version: string
  breakdown?: Record<string, any>
  hashes?: {
    md5: string
    sha1: string
    sha256: string
    crc32: string
  }
  metadata?: Record<string, any>
  structure?: Record<string, any>
  security?: {
    malware_score: number
    threat_level: string
    signatures: string[]
    anomalies: string[]
    embedded: {
      files: number
      scripts: number
      forms: number
    }
  }
  performance?: {
    total_time: string
    detection_time: string
    memory_used: string
    cpu_time: string
    efficiency: string
  }
}

export interface Engine {
  name: string
  cost: number
  status: string
  version: string
}

export interface SystemMetrics {
  cpu_usage: number
  memory_usage: number
  memory_total: number
  memory_used: number
  disk_usage: number
  disk_total: number
  disk_used: number
  active_threads: number
  total_scans: number
  engine_stats: Record<
    string,
    {
      scans_completed: number
      avg_time: number
      last_used: string | null
      performance: number
    }
  >
  timestamp: string
}

export class ProbiumAPI {
  private baseUrl: string

  constructor(baseUrl: string = API_BASE_URL) {
    this.baseUrl = baseUrl
  }

  async getEngines(): Promise<{ engines: Engine[]; total: number }> {
    const response = await fetch(`${this.baseUrl}/api/v1/engines`)
    if (!response.ok) {
      throw new Error(`Failed to fetch engines: ${response.statusText}`)
    }
    const data = await response.json()
    return data
  }

  async getEngineStatus(): Promise<Record<string, any>> {
    const response = await fetch(`${this.baseUrl}/api/v1/engines/status`)
    if (!response.ok) {
      throw new Error(`Failed to fetch engine status: ${response.statusText}`)
    }
    const data = await response.json()
    return data.engines
  }

  async scanFile(
    file: File,
    options: {
      engines?: string[]
      deep_analysis?: boolean
      generate_hashes?: boolean
      extract_metadata?: boolean
      validate_signatures?: boolean
    } = {},
  ): Promise<ScanResult> {
    const formData = new FormData()
    formData.append("file", file)

    if (options.engines && options.engines.length > 0) {
      formData.append("engines", options.engines.join(","))
    }

    formData.append("deep_analysis", String(options.deep_analysis ?? true))
    formData.append("generate_hashes", String(options.generate_hashes ?? true))
    formData.append("extract_metadata", String(options.extract_metadata ?? true))
    formData.append("validate_signatures", String(options.validate_signatures ?? true))

    const response = await fetch(`${this.baseUrl}/api/v1/scan/file`, {
      method: "POST",
      body: formData,
    })

    if (!response.ok) {
      throw new Error(`Scan failed: ${response.statusText}`)
    }

    const data = await response.json()
    return data.result
  }

  async scanBatch(
    files: File[],
    options: {
      engines?: string[]
      parallel_processing?: boolean
      thread_pool_size?: number
    } = {},
  ): Promise<{
    batch_id: string
    total_files: number
    completed: number
    failed: number
    results: any[]
    total_time: string
  }> {
    const formData = new FormData()

    files.forEach((file) => {
      formData.append("files", file)
    })

    if (options.engines && options.engines.length > 0) {
      formData.append("engines", options.engines.join(","))
    }

    formData.append("parallel_processing", String(options.parallel_processing ?? true))
    formData.append("thread_pool_size", String(options.thread_pool_size ?? 8))

    const response = await fetch(`${this.baseUrl}/api/v1/scan/batch`, {
      method: "POST",
      body: formData,
    })

    if (!response.ok) {
      throw new Error(`Batch scan failed: ${response.statusText}`)
    }

    const data = await response.json()
    return data
  }

  async getScanStatus(scanId: string): Promise<any> {
    const response = await fetch(`${this.baseUrl}/api/v1/scan/${scanId}/status`)
    if (!response.ok) {
      throw new Error(`Failed to get scan status: ${response.statusText}`)
    }
    const data = await response.json()
    return data.scan
  }

  async getSystemMetrics(): Promise<SystemMetrics> {
    const response = await fetch(`${this.baseUrl}/api/v1/system/metrics`)
    if (!response.ok) {
      throw new Error(`Failed to fetch system metrics: ${response.statusText}`)
    }
    const data = await response.json()
    return data.metrics
  }

  async getScanHistory(limit = 100): Promise<{ scans: ScanResult[]; total: number }> {
    const response = await fetch(`${this.baseUrl}/api/v1/scan/history?limit=${limit}`)
    if (!response.ok) {
      throw new Error(`Failed to fetch scan history: ${response.statusText}`)
    }
    const data = await response.json()
    return data
  }
}

export const api = new ProbiumAPI()
