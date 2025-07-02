import { NextResponse } from 'next/server'
import { localGetEngines } from '@/lib/local'

export const runtime = 'nodejs'

export async function GET() {
  try {
    const { engines } = await localGetEngines()
    return NextResponse.json({ engines })
  } catch (err: any) {
    return NextResponse.json({ error: String(err) }, { status: 500 })
  }
}
