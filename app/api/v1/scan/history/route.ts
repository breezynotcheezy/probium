import { NextRequest, NextResponse } from 'next/server'
import { localGetScanHistory } from '@/lib/local'

export const runtime = 'nodejs'

export async function GET(req: NextRequest) {
  const url = new URL(req.url)
  const limit = Number(url.searchParams.get('limit') || '100')
  try {
    const data = await localGetScanHistory(limit)
    return NextResponse.json(data)
  } catch (err: any) {
    return NextResponse.json({ error: String(err) }, { status: 500 })
  }
}
