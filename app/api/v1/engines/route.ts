import { NextResponse } from 'next/server'
import { spawn } from 'child_process'

async function getEngines(): Promise<string> {
  return new Promise((resolve, reject) => {
    const code = "import json, probium.registry as r; print(json.dumps({'engines': r.list_engines(), 'total': len(r.list_engines())}))"
    const proc = spawn('python3', ['-c', code])
    let out = ''
    proc.stdout.on('data', (d) => { out += d })
    proc.stderr.on('data', (d) => { out += d })
    proc.on('close', (c) => {
      if (c === 0) resolve(out)
      else reject(new Error(out))
    })
  })
}

export async function GET() {
  try {
    const res = await getEngines()
    return NextResponse.json(JSON.parse(res))
  } catch (err: any) {
    return NextResponse.json({ error: String(err) }, { status: 500 })
  }
}
