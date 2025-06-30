"use client"

import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Progress } from "@/components/ui/progress"
import { Badge } from "@/components/ui/badge"
import { FileText, CheckCircle, AlertTriangle } from "lucide-react"

interface StatsOverviewProps {
  results: any[]
  isScanning: boolean
}

export function StatsOverview({ results, isScanning }: StatsOverviewProps) {
  const totalFiles = results.length
  const avgConfidence = results.length > 0 ? results.reduce((sum, r) => sum + r.confidence, 0) / results.length : 0

  const fileTypes = results.reduce(
    (acc, result) => {
      acc[result.detectedType] = (acc[result.detectedType] || 0) + 1
      return acc
    },
    {} as Record<string, number>,
  )

  const highConfidenceFiles = results.filter((r) => r.confidence >= 0.9).length
  const lowConfidenceFiles = results.filter((r) => r.confidence < 0.7).length

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-6">
      {/* Total Files Scanned */}
      <Card>
        <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
          <CardTitle className="text-sm font-medium">Files Scanned</CardTitle>
          <FileText className="h-4 w-4 text-muted-foreground" />
        </CardHeader>
        <CardContent>
          <div className="text-2xl font-bold">{totalFiles}</div>
          {isScanning && (
            <Badge variant="secondary" className="mt-2">
              Scanning...
            </Badge>
          )}
        </CardContent>
      </Card>

      {/* Average Confidence */}
      <Card>
        <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
          <CardTitle className="text-sm font-medium">Avg Confidence</CardTitle>
          <CheckCircle className="h-4 w-4 text-muted-foreground" />
        </CardHeader>
        <CardContent>
          <div className="text-2xl font-bold">{totalFiles > 0 ? `${(avgConfidence * 100).toFixed(1)}%` : "0%"}</div>
          <Progress value={avgConfidence * 100} className="mt-2" />
        </CardContent>
      </Card>

      {/* High Confidence */}
      <Card>
        <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
          <CardTitle className="text-sm font-medium">High Confidence</CardTitle>
          <CheckCircle className="h-4 w-4 text-green-600" />
        </CardHeader>
        <CardContent>
          <div className="text-2xl font-bold text-green-600">{highConfidenceFiles}</div>
          <p className="text-xs text-muted-foreground">≥90% confidence</p>
        </CardContent>
      </Card>

      {/* Low Confidence */}
      <Card>
        <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
          <CardTitle className="text-sm font-medium">Needs Review</CardTitle>
          <AlertTriangle className="h-4 w-4 text-yellow-600" />
        </CardHeader>
        <CardContent>
          <div className="text-2xl font-bold text-yellow-600">{lowConfidenceFiles}</div>
          <p className="text-xs text-muted-foreground">{"<70% confidence"}</p>
        </CardContent>
      </Card>
    </div>
  )
}
