import { proxy } from '@/app/api/_proxy'

export async function GET(request: Request, { params }: { params: { scan_id: string } }) {
  return proxy(`/api/v1/scan/${params.scan_id}/status`)
}
