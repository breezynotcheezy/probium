"use client"

import { useMemo } from "react"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Progress } from "@/components/ui/progress"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { Gauge, Clock, Cpu, TrendingUp, AlertTriangle, CheckCircle } from "lucide-react"
import type { ScanResult, SystemMetrics } from "@/lib/api"

interface PerformanceProfilerProps {
  results: ScanResult[]
  systemStats: SystemMetrics
}

export function PerformanceProfiler({ results, systemStats }: PerformanceProfilerProps) {
  const performanceMetrics = useMemo(() => {
    if (results.length === 0) {
      return {
        avgScanTime: 0,
        totalScanTime: 0,
        fastestScan: 0,
        slowestScan: 0,
        throughput: 0,
        enginePerformance: {},
        bottlenecks: [],
        recommendations: [],
      }
    }

    const scanTimes = results.map((r) => Number.parseFloat(r.scan_time.replace("s", "")))
    const avgScanTime = scanTimes.reduce((sum, time) => sum + time, 0) / scanTimes.length
    const totalScanTime = scanTimes.reduce((sum, time) => sum + time, 0)
    const fastestScan = Math.min(...scanTimes)
    const slowestScan = Math.max(...scanTimes)

    // Calculate throughput (files per second)
    const throughput = results.length / totalScanTime

    // Analyze engine performance
    const enginePerformance: Record<
      string,
      {
        count: number
        totalTime: number
        avgTime: number
        efficiency: number
      }
    > = {}

    results.forEach((result) => {
      result.engines_used.forEach((engine) => {
        if (!enginePerformance[engine]) {
          enginePerformance[engine] = { count: 0, totalTime: 0, avgTime: 0, efficiency: 0 }
        }
        const scanTime = Number.parseFloat(result.scan_time.replace("s", ""))
        enginePerformance[engine].count += 1
        enginePerformance[engine].totalTime += scanTime
      })
    })

    // Calculate averages and efficiency scores
    Object.keys(enginePerformance).forEach((engine) => {
      const perf = enginePerformance[engine]
      perf.avgTime = perf.totalTime / perf.count
      perf.efficiency = perf.count / perf.totalTime // files per second
    })

    // Identify bottlenecks
    const bottlenecks = []
    if (avgScanTime > 2.0) {
      bottlenecks.push("High average scan time")
    }
    if (systemStats.cpu_usage > 80) {
      bottlenecks.push("High CPU usage")
    }
    if (systemStats.memory_usage > 85) {
      bottlenecks.push("High memory usage")
    }

    // Generate recommendations
    const recommendations = []
    if (avgScanTime > 1.0) {
      recommendations.push("Consider reducing thread pool size to optimize resource usage")
    }
    if (throughput < 5) {
      recommendations.push("Enable parallel processing for better throughput")
    }
    if (Object.keys(enginePerformance).length > 10) {
      recommendations.push("Disable unused engines to improve performance")
    }

    return {
      avgScanTime,
      totalScanTime,
      fastestScan,
      slowestScan,
      throughput,
      enginePerformance,
      bottlenecks,
      recommendations,
    }
  }, [results, systemStats])

  const getPerformanceColor = (value: number, thresholds: { good: number; warning: number }) => {
    if (value <= thresholds.good) return "text-green-400"
    if (value <= thresholds.warning) return "text-yellow-400"
    return "text-red-400"
  }

  const getEfficiencyScore = () => {
    let score = 100

    // Deduct points for performance issues
    if (performanceMetrics.avgScanTime > 2.0) score -= 20
    if (performanceMetrics.avgScanTime > 1.0) score -= 10
    if (systemStats.cpu_usage > 80) score -= 15
    if (systemStats.memory_usage > 85) score -= 15
    if (performanceMetrics.throughput < 5) score -= 10

    return Math.max(0, score)
  }

  return (
    <div className="space-y-6">
      {/* Performance Overview */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <Card className="bg-purple-900/30 border-purple-700">
          <CardContent className="p-4">
            <div className="flex items-center gap-3">
              <Clock className="w-8 h-8 text-blue-400" />
              <div>
                <p className="text-sm text-purple-300">Avg Scan Time</p>
                <p className="text-2xl font-bold text-white">{performanceMetrics.avgScanTime.toFixed(2)}s</p>
              </div>
            </div>
          </CardContent>
        </Card>

        <Card className="bg-purple-900/30 border-purple-700">
          <CardContent className="p-4">
            <div className="flex items-center gap-3">
              <TrendingUp className="w-8 h-8 text-green-400" />
              <div>
                <p className="text-sm text-purple-300">Throughput</p>
                <p className="text-2xl font-bold text-white">{performanceMetrics.throughput.toFixed(1)} f/s</p>
              </div>
            </div>
          </CardContent>
        </Card>

        <Card className="bg-purple-900/30 border-purple-700">
          <CardContent className="p-4">
            <div className="flex items-center gap-3">
              <Gauge className="w-8 h-8 text-purple-400" />
              <div>
                <p className="text-sm text-purple-300">Efficiency Score</p>
                <p className="text-2xl font-bold text-white">{getEfficiencyScore()}%</p>
              </div>
            </div>
          </CardContent>
        </Card>

        <Card className="bg-purple-900/30 border-purple-700">
          <CardContent className="p-4">
            <div className="flex items-center gap-3">
              <AlertTriangle className="w-8 h-8 text-yellow-400" />
              <div>
                <p className="text-sm text-purple-300">Bottlenecks</p>
                <p className="text-2xl font-bold text-white">{performanceMetrics.bottlenecks.length}</p>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Performance Analysis */}
      <Card className="bg-purple-900/30 border-purple-700">
        <CardHeader>
          <CardTitle className="text-white flex items-center gap-2">
            <Gauge className="w-5 h-5" />
            Performance Profiler
          </CardTitle>
          <CardDescription className="text-purple-300">
            Detailed performance analysis and optimization recommendations
          </CardDescription>
        </CardHeader>
        <CardContent>
          <Tabs defaultValue="overview" className="space-y-4">
            <TabsList className="grid w-full grid-cols-4 bg-purple-800/50">
              <TabsTrigger value="overview">Overview</TabsTrigger>
              <TabsTrigger value="engines">Engine Performance</TabsTrigger>
              <TabsTrigger value="bottlenecks">Bottlenecks</TabsTrigger>
              <TabsTrigger value="optimization">Optimization</TabsTrigger>
            </TabsList>

            <TabsContent value="overview" className="space-y-4">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <Card className="bg-purple-800/30 border-purple-600">
                  <CardHeader>
                    <CardTitle className="text-white text-lg">Scan Performance</CardTitle>
                  </CardHeader>
                  <CardContent className="space-y-4">
                    <div className="space-y-3">
                      <div className="flex justify-between">
                        <span className="text-purple-300">Average Time</span>
                        <span
                          className={`font-medium ${getPerformanceColor(performanceMetrics.avgScanTime, { good: 0.5, warning: 1.0 })}`}
                        >
                          {performanceMetrics.avgScanTime.toFixed(2)}s
                        </span>
                      </div>
                      <div className="flex justify-between">
                        <span className="text-purple-300">Fastest Scan</span>
                        <span className="text-green-400 font-medium">{performanceMetrics.fastestScan.toFixed(2)}s</span>
                      </div>
                      <div className="flex justify-between">
                        <span className="text-purple-300">Slowest Scan</span>
                        <span className="text-red-400 font-medium">{performanceMetrics.slowestScan.toFixed(2)}s</span>
                      </div>
                      <div className="flex justify-between">
                        <span className="text-purple-300">Total Time</span>
                        <span className="text-white font-medium">{performanceMetrics.totalScanTime.toFixed(2)}s</span>
                      </div>
                    </div>
                  </CardContent>
                </Card>

                <Card className="bg-purple-800/30 border-purple-600">
                  <CardHeader>
                    <CardTitle className="text-white text-lg">System Resources</CardTitle>
                  </CardHeader>
                  <CardContent className="space-y-4">
                    <div className="space-y-3">
                      <div>
                        <div className="flex justify-between mb-1">
                          <span className="text-purple-300">CPU Usage</span>
                          <span
                            className={`font-medium ${getPerformanceColor(systemStats.cpu_usage, { good: 50, warning: 80 })}`}
                          >
                            {systemStats.cpu_usage.toFixed(1)}%
                          </span>
                        </div>
                        <Progress value={systemStats.cpu_usage} className="bg-purple-900" />
                      </div>
                      <div>
                        <div className="flex justify-between mb-1">
                          <span className="text-purple-300">Memory Usage</span>
                          <span
                            className={`font-medium ${getPerformanceColor(systemStats.memory_usage, { good: 60, warning: 85 })}`}
                          >
                            {systemStats.memory_usage.toFixed(1)}%
                          </span>
                        </div>
                        <Progress value={systemStats.memory_usage} className="bg-purple-900" />
                      </div>
                      <div>
                        <div className="flex justify-between mb-1">
                          <span className="text-purple-300">Disk Usage</span>
                          <span
                            className={`font-medium ${getPerformanceColor(systemStats.disk_usage, { good: 70, warning: 90 })}`}
                          >
                            {systemStats.disk_usage.toFixed(1)}%
                          </span>
                        </div>
                        <Progress value={systemStats.disk_usage} className="bg-purple-900" />
                      </div>
                    </div>
                  </CardContent>
                </Card>
              </div>
            </TabsContent>

            <TabsContent value="engines" className="space-y-4">
              <Card className="bg-purple-800/30 border-purple-600">
                <CardHeader>
                  <CardTitle className="text-white text-lg">Engine Performance Analysis</CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="space-y-3">
                    {Object.entries(performanceMetrics.enginePerformance).map(([engine, perf]) => (
                      <div
                        key={engine}
                        className="flex items-center justify-between p-3 bg-purple-900/30 rounded border border-purple-700"
                      >
                        <div className="flex items-center gap-3">
                          <Cpu className="w-5 h-5 text-purple-400" />
                          <div>
                            <p className="text-white font-medium capitalize">{engine}</p>
                            <p className="text-purple-400 text-sm">{perf.count} scans</p>
                          </div>
                        </div>
                        <div className="flex items-center gap-4">
                          <div className="text-right">
                            <p className="text-white text-sm">{perf.avgTime.toFixed(3)}s avg</p>
                            <p className="text-purple-400 text-xs">{perf.efficiency.toFixed(1)} f/s</p>
                          </div>
                          <Badge
                            className={
                              perf.avgTime < 0.5 ? "bg-green-700" : perf.avgTime < 1.0 ? "bg-yellow-700" : "bg-red-700"
                            }
                          >
                            {perf.avgTime < 0.5 ? "Fast" : perf.avgTime < 1.0 ? "Normal" : "Slow"}
                          </Badge>
                        </div>
                      </div>
                    ))}
                  </div>
                </CardContent>
              </Card>
            </TabsContent>

            <TabsContent value="bottlenecks" className="space-y-4">
              <Card className="bg-purple-800/30 border-purple-600">
                <CardHeader>
                  <CardTitle className="text-white text-lg">Performance Bottlenecks</CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="space-y-3">
                    {performanceMetrics.bottlenecks.length > 0 ? (
                      performanceMetrics.bottlenecks.map((bottleneck, index) => (
                        <div
                          key={index}
                          className="flex items-center gap-3 p-3 bg-yellow-900/30 border border-yellow-600 rounded"
                        >
                          <AlertTriangle className="w-5 h-5 text-yellow-400" />
                          <span className="text-yellow-300">{bottleneck}</span>
                        </div>
                      ))
                    ) : (
                      <div className="text-center py-8">
                        <CheckCircle className="w-12 h-12 text-green-400 mx-auto mb-4" />
                        <h3 className="text-lg font-semibold text-white mb-2">No Bottlenecks Detected</h3>
                        <p className="text-purple-300">System is performing optimally</p>
                      </div>
                    )}
                  </div>
                </CardContent>
              </Card>
            </TabsContent>

            <TabsContent value="optimization" className="space-y-4">
              <Card className="bg-purple-800/30 border-purple-600">
                <CardHeader>
                  <CardTitle className="text-white text-lg">Optimization Recommendations</CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="space-y-3">
                    {performanceMetrics.recommendations.length > 0 ? (
                      performanceMetrics.recommendations.map((recommendation, index) => (
                        <div
                          key={index}
                          className="flex items-center gap-3 p-3 bg-blue-900/30 border border-blue-600 rounded"
                        >
                          <TrendingUp className="w-5 h-5 text-blue-400" />
                          <span className="text-blue-300">{recommendation}</span>
                        </div>
                      ))
                    ) : (
                      <div className="text-center py-8">
                        <CheckCircle className="w-12 h-12 text-green-400 mx-auto mb-4" />
                        <h3 className="text-lg font-semibold text-white mb-2">System Optimized</h3>
                        <p className="text-purple-300">No optimization recommendations at this time</p>
                      </div>
                    )}
                  </div>

                  <div className="mt-6 p-4 bg-purple-900/30 border border-purple-600 rounded">
                    <h4 className="text-white font-medium mb-3">Quick Optimization Actions</h4>
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-2">
                      <button className="p-2 bg-purple-700 hover:bg-purple-600 rounded text-white text-sm transition-colors">
                        Optimize Thread Pool
                      </button>
                      <button className="p-2 bg-purple-700 hover:bg-purple-600 rounded text-white text-sm transition-colors">
                        Clear Cache
                      </button>
                      <button className="p-2 bg-purple-700 hover:bg-purple-600 rounded text-white text-sm transition-colors">
                        Disable Slow Engines
                      </button>
                      <button className="p-2 bg-purple-700 hover:bg-purple-600 rounded text-white text-sm transition-colors">
                        Generate Report
                      </button>
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
