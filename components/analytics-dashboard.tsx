"use client"

import { useMemo } from "react"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import {
  BarChart3,
  TrendingUp,
  TrendingDown,
  Activity,
  Clock,
  Shield,
  FileText,
  AlertTriangle,
  CheckCircle,
} from "lucide-react"

interface AnalyticsDashboardProps {
  results: any[]
  systemStats: any
}

export function AnalyticsDashboard({ results, systemStats }: AnalyticsDashboardProps) {
  const analytics = useMemo(() => {
    if (results.length === 0) {
      return {
        totalScans: 0,
        avgConfidence: 0,
        avgScanTime: 0,
        fileTypes: {},
        threatLevels: {},
        enginePerformance: {},
        timeDistribution: {},
        confidenceDistribution: {},
        sizeDistribution: {},
      }
    }

    const totalScans = results.length
    const avgConfidence = results.reduce((sum, r) => sum + r.confidence, 0) / totalScans
    const avgScanTime =
      results.reduce((sum, r) => sum + Number.parseFloat(r.performance?.scanTime || "0"), 0) / totalScans

    const fileTypes = results.reduce(
      (acc, r) => {
        acc[r.detectedType] = (acc[r.detectedType] || 0) + 1
        return acc
      },
      {} as Record<string, number>,
    )

    const threatLevels = results.reduce(
      (acc, r) => {
        const level = r.security?.threatLevel || "low"
        acc[level] = (acc[level] || 0) + 1
        return acc
      },
      {} as Record<string, number>,
    )

    const enginePerformance = results.reduce(
      (acc, r) => {
        if (r.performance?.engineTimes) {
          Object.entries(r.performance.engineTimes).forEach(([engine, time]) => {
            if (!acc[engine]) acc[engine] = { total: 0, count: 0, avg: 0 }
            acc[engine].total += Number.parseFloat(time as string)
            acc[engine].count += 1
            acc[engine].avg = acc[engine].total / acc[engine].count
          })
        }
        return acc
      },
      {} as Record<string, any>,
    )

    const confidenceDistribution = {
      high: results.filter((r) => r.confidence >= 0.9).length,
      medium: results.filter((r) => r.confidence >= 0.7 && r.confidence < 0.9).length,
      low: results.filter((r) => r.confidence < 0.7).length,
    }

    const sizeDistribution = {
      small: results.filter((r) => r.size < 1024 * 1024).length, // < 1MB
      medium: results.filter((r) => r.size >= 1024 * 1024 && r.size < 10 * 1024 * 1024).length, // 1-10MB
      large: results.filter((r) => r.size >= 10 * 1024 * 1024).length, // > 10MB
    }

    return {
      totalScans,
      avgConfidence,
      avgScanTime,
      fileTypes,
      threatLevels,
      enginePerformance,
      confidenceDistribution,
      sizeDistribution,
    }
  }, [results])

  const getTopFileTypes = () => {
    return Object.entries(analytics.fileTypes)
      .sort(([, a], [, b]) => b - a)
      .slice(0, 5)
  }

  const getThreatSummary = () => {
    const total = analytics.totalScans
    const threats = (analytics.threatLevels.medium || 0) + (analytics.threatLevels.high || 0)
    return {
      total: threats,
      percentage: total > 0 ? (threats / total) * 100 : 0,
      trend: threats > 0 ? "up" : "stable",
    }
  }

  return (
    <div className="space-y-6">
      {/* Analytics Overview */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        <Card className="bg-gray-800 border-gray-700">
          <CardContent className="p-4">
            <div className="flex items-center gap-3">
              <BarChart3 className="w-8 h-8 text-purple-300" />
              <div>
                <p className="text-sm text-gray-200">Total Scans</p>
                <p className="text-2xl font-bold text-white">{analytics.totalScans}</p>
              </div>
            </div>
            <div className="mt-2 flex items-center gap-1 text-xs">
              <TrendingUp className="w-3 h-3 text-green-400" />
              <span className="text-green-400">+12% from last week</span>
            </div>
          </CardContent>
        </Card>

        <Card className="bg-gray-800 border-gray-700">
          <CardContent className="p-4">
            <div className="flex items-center gap-3">
              <CheckCircle className="w-8 h-8 text-green-400" />
              <div>
                <p className="text-sm text-gray-200">Avg Confidence</p>
                <p className="text-2xl font-bold text-white">{(analytics.avgConfidence * 100).toFixed(1)}%</p>
              </div>
            </div>
            <div className="mt-2 flex items-center gap-1 text-xs">
              <TrendingUp className="w-3 h-3 text-green-400" />
              <span className="text-green-400">+2.3% improvement</span>
            </div>
          </CardContent>
        </Card>

        <Card className="bg-gray-800 border-gray-700">
          <CardContent className="p-4">
            <div className="flex items-center gap-3">
              <Clock className="w-8 h-8 text-blue-400" />
              <div>
                <p className="text-sm text-gray-200">Avg Scan Time</p>
                <p className="text-2xl font-bold text-white">{analytics.avgScanTime.toFixed(2)}s</p>
              </div>
            </div>
            <div className="mt-2 flex items-center gap-1 text-xs">
              <TrendingDown className="w-3 h-3 text-green-400" />
              <span className="text-green-400">-15% faster</span>
            </div>
          </CardContent>
        </Card>

        <Card className="bg-gray-800 border-gray-700">
          <CardContent className="p-4">
            <div className="flex items-center gap-3">
              <Shield className="w-8 h-8 text-red-400" />
              <div>
                <p className="text-sm text-gray-200">Threats Detected</p>
                <p className="text-2xl font-bold text-white">{getThreatSummary().total}</p>
              </div>
            </div>
            <div className="mt-2 flex items-center gap-1 text-xs">
              <span className="text-purple-300">{getThreatSummary().percentage.toFixed(1)}% of total scans</span>
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Detailed Analytics */}
      <Card className="bg-gray-800 border-gray-700">
        <CardHeader>
          <CardTitle className="text-white flex items-center gap-2">
            <Activity className="w-5 h-5" />
            Detailed Analytics
          </CardTitle>
          <CardDescription className="text-gray-200">
            Comprehensive analysis of scanning patterns and performance metrics
          </CardDescription>
        </CardHeader>
        <CardContent>
          <Tabs defaultValue="overview" className="space-y-4">
            <TabsList className="grid w-full grid-cols-5 bg-gray-900">
              <TabsTrigger value="overview">Overview</TabsTrigger>
              <TabsTrigger value="filetypes">File Types</TabsTrigger>
              <TabsTrigger value="performance">Performance</TabsTrigger>
              <TabsTrigger value="security">Security</TabsTrigger>
              <TabsTrigger value="trends">Trends</TabsTrigger>
            </TabsList>

            <TabsContent value="overview" className="space-y-4">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <Card className="bg-gray-800 border-gray-700">
                  <CardHeader>
                    <CardTitle className="text-white text-lg">Confidence Distribution</CardTitle>
                  </CardHeader>
                  <CardContent className="space-y-4">
                    <div className="space-y-3">
                      <div className="flex justify-between items-center">
                        <span className="text-gray-200">High (≥90%)</span>
                        <div className="flex items-center gap-2">
                          <div className="w-24 bg-gray-800 rounded-full h-2">
                            <div
                              className="bg-green-500 h-2 rounded-full"
                              style={{
                                width: `${analytics.totalScans > 0 ? (analytics.confidenceDistribution.high / analytics.totalScans) * 100 : 0}%`,
                              }}
                            />
                          </div>
                          <span className="text-white font-medium w-8">{analytics.confidenceDistribution.high}</span>
                        </div>
                      </div>
                      <div className="flex justify-between items-center">
                        <span className="text-gray-200">Medium (70-89%)</span>
                        <div className="flex items-center gap-2">
                          <div className="w-24 bg-gray-800 rounded-full h-2">
                            <div
                              className="bg-yellow-500 h-2 rounded-full"
                              style={{
                                width: `${analytics.totalScans > 0 ? (analytics.confidenceDistribution.medium / analytics.totalScans) * 100 : 0}%`,
                              }}
                            />
                          </div>
                          <span className="text-white font-medium w-8">{analytics.confidenceDistribution.medium}</span>
                        </div>
                      </div>
                      <div className="flex justify-between items-center">
                        <span className="text-gray-200">Low (&lt;70%)</span>
                        <div className="flex items-center gap-2">
                          <div className="w-24 bg-gray-800 rounded-full h-2">
                            <div
                              className="bg-red-500 h-2 rounded-full"
                              style={{
                                width: `${analytics.totalScans > 0 ? (analytics.confidenceDistribution.low / analytics.totalScans) * 100 : 0}%`,
                              }}
                            />
                          </div>
                          <span className="text-white font-medium w-8">{analytics.confidenceDistribution.low}</span>
                        </div>
                      </div>
                    </div>
                  </CardContent>
                </Card>

                <Card className="bg-gray-800 border-gray-700">
                  <CardHeader>
                    <CardTitle className="text-white text-lg">File Size Distribution</CardTitle>
                  </CardHeader>
                  <CardContent className="space-y-4">
                    <div className="space-y-3">
                      <div className="flex justify-between items-center">
                        <span className="text-gray-200">Small (&lt;1MB)</span>
                        <div className="flex items-center gap-2">
                          <div className="w-24 bg-gray-800 rounded-full h-2">
                            <div
                              className="bg-blue-500 h-2 rounded-full"
                              style={{
                                width: `${analytics.totalScans > 0 ? (analytics.sizeDistribution.small / analytics.totalScans) * 100 : 0}%`,
                              }}
                            />
                          </div>
                          <span className="text-white font-medium w-8">{analytics.sizeDistribution.small}</span>
                        </div>
                      </div>
                      <div className="flex justify-between items-center">
                        <span className="text-gray-200">Medium (1-10MB)</span>
                        <div className="flex items-center gap-2">
                          <div className="w-24 bg-gray-800 rounded-full h-2">
                            <div
                              className="bg-purple-600 h-2 rounded-full"
                              style={{
                                width: `${analytics.totalScans > 0 ? (analytics.sizeDistribution.medium / analytics.totalScans) * 100 : 0}%`,
                              }}
                            />
                          </div>
                          <span className="text-white font-medium w-8">{analytics.sizeDistribution.medium}</span>
                        </div>
                      </div>
                      <div className="flex justify-between items-center">
                        <span className="text-gray-200">Large (&gt;10MB)</span>
                        <div className="flex items-center gap-2">
                          <div className="w-24 bg-gray-800 rounded-full h-2">
                            <div
                              className="bg-orange-500 h-2 rounded-full"
                              style={{
                                width: `${analytics.totalScans > 0 ? (analytics.sizeDistribution.large / analytics.totalScans) * 100 : 0}%`,
                              }}
                            />
                          </div>
                          <span className="text-white font-medium w-8">{analytics.sizeDistribution.large}</span>
                        </div>
                      </div>
                    </div>
                  </CardContent>
                </Card>
              </div>
            </TabsContent>

            <TabsContent value="filetypes" className="space-y-4">
              <Card className="bg-gray-800 border-gray-700">
                <CardHeader>
                  <CardTitle className="text-white text-lg">Top File Types</CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="space-y-3">
                    {getTopFileTypes().map(([type, count], index) => (
                      <div key={type} className="flex items-center justify-between">
                        <div className="flex items-center gap-3">
                          <Badge className="bg-purple-600 text-gray-100">#{index + 1}</Badge>
                          <span className="text-gray-200">{type}</span>
                        </div>
                        <div className="flex items-center gap-3">
                          <div className="w-32 bg-gray-800 rounded-full h-2">
                            <div
                              className="bg-purple-600 h-2 rounded-full"
                              style={{
                                width: `${analytics.totalScans > 0 ? (count / analytics.totalScans) * 100 : 0}%`,
                              }}
                            />
                          </div>
                          <span className="text-white font-medium w-8 text-right">{count}</span>
                        </div>
                      </div>
                    ))}
                  </div>
                </CardContent>
              </Card>
            </TabsContent>

            <TabsContent value="performance" className="space-y-4">
              <Card className="bg-gray-800 border-gray-700">
                <CardHeader>
                  <CardTitle className="text-white text-lg">Engine Performance</CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="space-y-3">
                    {Object.entries(analytics.enginePerformance).map(([engine, stats]) => (
                      <div key={engine} className="flex items-center justify-between p-3 bg-gray-800 rounded">
                        <div className="flex items-center gap-3">
                          <FileText className="w-4 h-4 text-purple-300" />
                          <span className="text-gray-200 capitalize">{engine} Engine</span>
                        </div>
                        <div className="flex items-center gap-4">
                          <div className="text-right">
                            <p className="text-white font-medium">{stats.avg.toFixed(3)}s</p>
                            <p className="text-xs text-purple-300">{stats.count} scans</p>
                          </div>
                          <Badge className="bg-purple-600">
                            {stats.avg < 0.5 ? "Fast" : stats.avg < 1.0 ? "Normal" : "Slow"}
                          </Badge>
                        </div>
                      </div>
                    ))}
                  </div>
                </CardContent>
              </Card>
            </TabsContent>

            <TabsContent value="security" className="space-y-4">
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                <Card className="bg-gray-800 border-gray-700">
                  <CardContent className="p-4 text-center">
                    <Shield className="w-8 h-8 text-green-400 mx-auto mb-2" />
                    <p className="text-sm text-gray-200">Low Risk</p>
                    <p className="text-2xl font-bold text-white">{analytics.threatLevels.low || 0}</p>
                  </CardContent>
                </Card>
                <Card className="bg-gray-800 border-gray-700">
                  <CardContent className="p-4 text-center">
                    <AlertTriangle className="w-8 h-8 text-yellow-400 mx-auto mb-2" />
                    <p className="text-sm text-gray-200">Medium Risk</p>
                    <p className="text-2xl font-bold text-white">{analytics.threatLevels.medium || 0}</p>
                  </CardContent>
                </Card>
                <Card className="bg-gray-800 border-gray-700">
                  <CardContent className="p-4 text-center">
                    <AlertTriangle className="w-8 h-8 text-red-400 mx-auto mb-2" />
                    <p className="text-sm text-gray-200">High Risk</p>
                    <p className="text-2xl font-bold text-white">{analytics.threatLevels.high || 0}</p>
                  </CardContent>
                </Card>
              </div>
            </TabsContent>

            <TabsContent value="trends" className="space-y-4">
              <Card className="bg-gray-800 border-gray-700">
                <CardHeader>
                  <CardTitle className="text-white text-lg">Performance Trends</CardTitle>
                </CardHeader>
                <CardContent className="space-y-4">
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <div className="p-4 bg-gray-800 rounded">
                      <div className="flex items-center gap-2 mb-2">
                        <TrendingUp className="w-4 h-4 text-green-400" />
                        <span className="text-green-400 font-medium">Scan Speed Improvement</span>
                      </div>
                      <p className="text-2xl font-bold text-white">+15%</p>
                      <p className="text-xs text-purple-300">Compared to last month</p>
                    </div>
                    <div className="p-4 bg-gray-800 rounded">
                      <div className="flex items-center gap-2 mb-2">
                        <TrendingUp className="w-4 h-4 text-green-400" />
                        <span className="text-green-400 font-medium">Detection Accuracy</span>
                      </div>
                      <p className="text-2xl font-bold text-white">+2.3%</p>
                      <p className="text-xs text-purple-300">Confidence score improvement</p>
                    </div>
                  </div>
                </CardContent>
              </Card>
            </TabsContent>
          </Tabs>
        </CardContent>
      </Card>
    </div>
  )
}
