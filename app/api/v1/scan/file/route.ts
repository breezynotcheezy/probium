import { NextRequest, NextResponse } from 'next/server'
import { localScanFile } from '@/lib/local'

export const runtime = 'nodejs'

export async function POST(req: NextRequest) {
  const form = await req.formData()
  const file = form.get('file')
  if (!(file instanceof File)) {
    return NextResponse.json({ error: 'missing file' }, { status: 400 })
  }
  try {
    const result = await localScanFile(file)
    return NextResponse.json({ result })
  } catch (err: any) {
    return NextResponse.json({ error: String(err) }, { status: 500 })
  }
}
