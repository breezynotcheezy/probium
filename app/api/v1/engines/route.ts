import { NextResponse } from 'next/server'
import { localGetEngines } from '@/lib/local'

export const runtime = 'nodejs'

export async function GET() {
  try {
    const data = await localGetEngines()
    return NextResponse.json(data)
  } catch (err: any) {
    return NextResponse.json({ error: String(err) }, { status: 500 })
  }
}
