import { spawn } from 'child_process'
import { writeFile, unlink, readFile, access, constants } from 'fs/promises'
import { tmpdir } from 'os'
import { join } from 'path'
import type { ScanResult, Engine, SystemMetrics } from './api'

async function runPython(args: string[]): Promise<string> {
  return new Promise((resolve, reject) => {
    const proc = spawn('python', args)
    let out = ''
    let err = ''
    proc.stdout.on('data', (d) => { out += d })
    proc.stderr.on('data', (d) => { err += d })
    proc.on('close', (code) => {
      if (code === 0) resolve(out.trim())
      else reject(new Error(err || `Python exited with code ${code}`))
    })
  })
}

const HISTORY_FILE = join(process.cwd(), 'local_scan_history.json')

async function appendHistory(res: ScanResult) {
  let data: ScanResult[] = []
  try {
    await access(HISTORY_FILE, constants.F_OK)
    const txt = await readFile(HISTORY_FILE, 'utf8')
    data = JSON.parse(txt)
  } catch {
    data = []
  }
  data.unshift(res)
  await writeFile(HISTORY_FILE, JSON.stringify(data, null, 2))
}

export async function localScanFile(file: File): Promise<ScanResult> {
  const buffer = Buffer.from(await file.arrayBuffer())
  const tmpPath = join(tmpdir(), `${Date.now()}_${file.name}`)
  await writeFile(tmpPath, buffer)
  try {
    const out = await runPython(['-m', 'probium.cli', 'detect', tmpPath, '--raw'])
    const parsed = JSON.parse(out)
    const cand = parsed.candidates?.[0] ?? {}
    const result: ScanResult = {
      id: String(Date.now()),
      filename: file.name,
      size: file.size,
      detected_type: cand.media_type || '',
      mime_type: cand.media_type || '',
      confidence: cand.confidence || 0,
      extension: cand.extension ?? null,
      engines_used: [parsed.engine || ''],
      scan_time: `${parsed.elapsed_ms}ms`,
      timestamp: new Date().toISOString(),
      probium_version: parsed.probium_version || '',
    }
    await appendHistory(result)
    return result
  } finally {
    await unlink(tmpPath).catch(() => {})
  }
}

export async function localGetEngines(): Promise<{ engines: Engine[]; total: number }> {
  const out = await runPython(['-c', 'import json, probium; print(json.dumps(probium.list_engines()))'])
  const names: string[] = JSON.parse(out)
  return { engines: names.map((name) => ({ name, cost: 1, status: 'available', version: '' })), total: names.length }
}

export async function localGetScanHistory(limit = 100): Promise<{ scans: ScanResult[]; total: number }> {
  try {
    const txt = await readFile(HISTORY_FILE, 'utf8')
    const scans: ScanResult[] = JSON.parse(txt)
    return { scans: scans.slice(0, limit), total: scans.length }
  } catch {
    return { scans: [], total: 0 }
  }
}

export async function localGetSystemMetrics(): Promise<SystemMetrics> {
  const os = await import('os')
  const total = os.totalmem()
  const free = os.freemem()
  return {
    cpu_usage: os.loadavg()[0],
    memory_usage: (total - free) / total,
    memory_total: total,
    memory_used: total - free,
    disk_usage: 0,
    disk_total: 0,
    disk_used: 0,
    active_threads: os.cpus().length,
    total_scans: 0,
    engine_stats: {},
    timestamp: new Date().toISOString(),
  }
}

export async function localGetScanStatus(id: string): Promise<ScanResult | null> {
  try {
    const txt = await readFile(HISTORY_FILE, 'utf8')
    const scans: ScanResult[] = JSON.parse(txt)
    return scans.find((s) => s.id === id) || null
  } catch {
    return null
  }
}
