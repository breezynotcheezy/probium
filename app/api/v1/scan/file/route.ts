import { NextRequest, NextResponse } from 'next/server'
import { spawn } from 'child_process'
import { promises as fs } from 'fs'
import os from 'os'
import path from 'path'

async function runPythonDetect(filePath: string): Promise<string> {
  return new Promise((resolve, reject) => {
    const proc = spawn('python3', ['-m', 'probium.cli', 'detect', filePath, '--raw'])
    let out = ''
    proc.stdout.on('data', (d) => { out += d })
    proc.stderr.on('data', (d) => { out += d })
    proc.on('close', (code) => {
      if (code === 0) resolve(out)
      else reject(new Error(out))
    })
  })
}

export async function POST(req: NextRequest) {
  const data = await req.formData()
  const file = data.get('file')
  if (!(file instanceof Blob)) {
    return NextResponse.json({ error: 'file field missing' }, { status: 400 })
  }
  const buf = Buffer.from(await file.arrayBuffer())
  const temp = path.join(os.tmpdir(), `probium-${Date.now()}`)
  await fs.writeFile(temp, buf)
  try {
    const res = await runPythonDetect(temp)
    await fs.unlink(temp)
    return NextResponse.json({ result: JSON.parse(res) })
  } catch (err: any) {
    await fs.unlink(temp).catch(() => {})
    return NextResponse.json({ error: String(err) }, { status: 500 })
  }
}
