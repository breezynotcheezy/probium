import { NextRequest } from 'next/server'
import { proxy } from '@/app/api/_proxy'

export async function POST(req: NextRequest) {
  const data = await req.formData()
  return proxy('/api/v1/scan/file', { method: 'POST', body: data })
}
