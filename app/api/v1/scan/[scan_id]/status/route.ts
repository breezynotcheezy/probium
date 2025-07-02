import { NextResponse } from 'next/server'
import { localGetScanStatus } from '@/lib/local'

export const runtime = 'nodejs'

export async function GET(request: Request, { params }: { params: { scan_id: string } }) {
  try {
    const data = await localGetScanStatus(params.scan_id)
    if (!data) {
      return NextResponse.json({ error: 'not found' }, { status: 404 })
    }
    return NextResponse.json({ scan: data })
  } catch (err: any) {
    return NextResponse.json({ error: String(err) }, { status: 500 })
  }
}
