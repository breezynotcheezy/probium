import { NextResponse } from 'next/server'
import { localGetSystemMetrics } from '@/lib/local'

export const runtime = 'nodejs'

export async function GET() {
  try {
    const metrics = await localGetSystemMetrics()
    return NextResponse.json({ metrics })
  } catch (err: any) {
    return NextResponse.json({ error: String(err) }, { status: 500 })
  }
}
