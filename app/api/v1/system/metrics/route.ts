import { proxy } from '@/app/api/_proxy'

export async function GET() {
  return proxy('/api/v1/system/metrics')
}
