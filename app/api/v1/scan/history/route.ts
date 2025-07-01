import { NextRequest } from 'next/server'
import { proxy } from '@/app/api/_proxy'

export async function GET(req: NextRequest) {
  const url = new URL(req.url)
  return proxy(`/api/v1/scan/history${url.search}`)
}
