"use client"

import { useState, useEffect } from "react"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { ScrollArea } from "@/components/ui/scroll-area"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { Eye, Activity, Cpu, MemoryStick, Network, AlertTriangle, CheckCircle } from "lucide-react"
import type { SystemMetrics } from "@/lib/api"

interface RealTimeMonitorProps {
  systemStats: SystemMetrics
  isScanning: boolean
}

interface LogEntry {
  id: string
  timestamp: string
  level: "info" | "warning" | "error" | "success"
  message: string
  component: string
}

export function RealTimeMonitor({ systemStats, isScanning }: RealTimeMonitorProps) {
  const [logs, setLogs] = useState<LogEntry[]>([])
  const [activeConnections, setActiveConnections] = useState(0)

  useEffect(() => {
    // Simulate real-time log entries
    const interval = setInterval(() => {
      const logTypes = [
        {
          level: "info" as const,
          messages: [
            "Engine initialization complete",
            "Cache hit for file signature",
            "Thread pool status: healthy",
            "Memory usage within normal range",
          ],
        },
        {
          level: "success" as const,
          messages: ["File scan completed successfully", "Engine performance optimal", "System health check passed"],
        },
        {
          level: "warning" as const,
          messages: ["High CPU usage detected", "Memory usage approaching threshold", "Slow engine response time"],
        },
      ]

      if (isScanning) {
        const scanLogs = [
          { level: "info" as const, message: "Starting file analysis", component: "Scanner" },
          { level: "info" as const, message: "Running detection engines", component: "Engine Manager" },
          { level: "success" as const, message: "File type detected", component: "Detection" },
          { level: "info" as const, message: "Generating file hashes", component: "Hash Generator" },
          { level: "info" as const, message: "Extracting metadata", component: "Metadata Extractor" },
        ]

        const randomLog = scanLogs[Math.floor(Math.random() * scanLogs.length)]
        const newLog: LogEntry = {
          id: `log_${Date.now()}_${Math.random()}`,
          timestamp: new Date().toISOString(),
          level: randomLog.level,
          message: randomLog.message,
          component: randomLog.component,
        }

        setLogs((prev) => [newLog, ...prev.slice(0, 99)]) // Keep last 100 logs
      } else {
        // System monitoring logs
        const category = logTypes[Math.floor(Math.random() * logTypes.length)]
        const message = category.messages[Math.floor(Math.random() * category.messages.length)]

        const newLog: LogEntry = {
          id: `log_${Date.now()}_${Math.random()}`,
          timestamp: new Date().toISOString(),
          level: category.level,
          message,
          component: "System Monitor",
        }

        setLogs((prev) => [newLog, ...prev.slice(0, 99)])
      }
    }, 2000)

    return () => clearInterval(interval)
  }, [isScanning])

  // Simulate active connections
  useEffect(() => {
    const interval = setInterval(() => {
      setActiveConnections((prev) => Math.max(0, prev + (Math.random() - 0.5) * 2))
    }, 3000)

    return () => clearInterval(interval)
  }, [])

  const getLevelColor = (level: string) => {
    switch (level) {
      case "error":
        return "text-red-400"
      case "warning":
        return "text-yellow-400"
      case "success":
        return "text-green-400"
      default:
        return "text-blue-400"
    }
  }

  const getLevelIcon = (level: string) => {
    switch (level) {
      case "error":
        return AlertTriangle
      case "warning":
        return AlertTriangle
      case "success":
        return CheckCircle
      default:
        return Activity
    }
  }

  return (
    <div className="space-y-6">
      {/* Real-time Status Overview */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <Card className="bg-purple-900/30 border-purple-700">
          <CardContent className="p-4">
            <div className="flex items-center gap-3">
              <Cpu className="w-8 h-8 text-blue-400" />
              <div>
                <p className="text-sm text-purple-300">CPU Usage</p>
                <p className="text-2xl font-bold text-white">{systemStats.cpu_usage.toFixed(1)}%</p>
              </div>
            </div>
            <div className="mt-2 w-full bg-purple-800/50 rounded-full h-2">
              <div
                className="bg-blue-500 h-2 rounded-full transition-all duration-500"
                style={{ width: `${systemStats.cpu_usage}%` }}
              />
            </div>
          </CardContent>
        </Card>

        <Card className="bg-purple-900/30 border-purple-700">
          <CardContent className="p-4">
            <div className="flex items-center gap-3">
              <MemoryStick className="w-8 h-8 text-green-400" />
              <div>
                <p className="text-sm text-purple-300">Memory</p>
                <p className="text-2xl font-bold text-white">{systemStats.memory_usage.toFixed(1)}%</p>
              </div>
            </div>
            <div className="mt-2 w-full bg-purple-800/50 rounded-full h-2">
              <div
                className="bg-green-500 h-2 rounded-full transition-all duration-500"
                style={{ width: `${systemStats.memory_usage}%` }}
              />
            </div>
          </CardContent>
        </Card>

        <Card className="bg-purple-900/30 border-purple-700">
          <CardContent className="p-4">
            <div className="flex items-center gap-3">
              <Activity className="w-8 h-8 text-purple-400" />
              <div>
                <p className="text-sm text-purple-300">Active Threads</p>
                <p className="text-2xl font-bold text-white">{systemStats.active_threads}</p>
              </div>
            </div>
            <div className="mt-2 flex items-center gap-1">
              <div className="w-2 h-2 bg-purple-400 rounded-full animate-pulse" />
              <span className="text-xs text-purple-400">{isScanning ? "Scanning" : "Idle"}</span>
            </div>
          </CardContent>
        </Card>

        <Card className="bg-purple-900/30 border-purple-700">
          <CardContent className="p-4">
            <div className="flex items-center gap-3">
              <Network className="w-8 h-8 text-yellow-400" />
              <div>
                <p className="text-sm text-purple-300">Connections</p>
                <p className="text-2xl font-bold text-white">{Math.round(activeConnections)}</p>
              </div>
            </div>
            <div className="mt-2 text-xs text-purple-400">API endpoints active</div>
          </CardContent>
        </Card>
      </div>

      {/* Real-time Monitoring Dashboard */}
      <Card className="bg-purple-900/30 border-purple-700">
        <CardHeader>
          <CardTitle className="text-white flex items-center gap-2">
            <Eye className="w-5 h-5" />
            Live System Monitor
          </CardTitle>
          <CardDescription className="text-purple-300">
            Real-time system activity and performance monitoring
          </CardDescription>
        </CardHeader>
        <CardContent>
          <Tabs defaultValue="logs" className="space-y-4">
            <TabsList className="grid w-full grid-cols-3 bg-purple-800/50">
              <TabsTrigger value="logs">Activity Logs</TabsTrigger>
              <TabsTrigger value="performance">Performance</TabsTrigger>
              <TabsTrigger value="engines">Engine Status</TabsTrigger>
            </TabsList>

            <TabsContent value="logs" className="space-y-4">
              <Card className="bg-purple-800/30 border-purple-600">
                <CardHeader>
                  <CardTitle className="text-white text-lg">Live Activity Feed</CardTitle>
                  <div className="flex items-center gap-2">
                    <div className="w-2 h-2 bg-green-400 rounded-full animate-pulse" />
                    <span className="text-green-400 text-sm">Live</span>
                  </div>
                </CardHeader>
                <CardContent>
                  <ScrollArea className="h-96">
                    <div className="space-y-2">
                      {logs.map((log) => {
                        const IconComponent = getLevelIcon(log.level)
                        return (
                          <div
                            key={log.id}
                            className="flex items-start gap-3 p-3 bg-purple-900/30 rounded border border-purple-700 hover:bg-purple-900/50 transition-colors"
                          >
                            <IconComponent className={`w-4 h-4 mt-0.5 ${getLevelColor(log.level)}`} />
                            <div className="flex-1 min-w-0">
                              <div className="flex items-center gap-2 mb-1">
                                <Badge variant="outline" className="border-purple-600 text-purple-300 text-xs">
                                  {log.component}
                                </Badge>
                                <span className="text-xs text-purple-400">
                                  {new Date(log.timestamp).toLocaleTimeString()}
                                </span>
                              </div>
                              <p className="text-white text-sm">{log.message}</p>
                            </div>
                          </div>
                        )
                      })}
                    </div>
                  </ScrollArea>
                </CardContent>
              </Card>
            </TabsContent>

            <TabsContent value="performance" className="space-y-4">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <Card className="bg-purple-800/30 border-purple-600">
                  <CardHeader>
                    <CardTitle className="text-white text-lg">Resource Usage</CardTitle>
                  </CardHeader>
                  <CardContent className="space-y-4">
                    <div className="space-y-2">
                      <div className="flex justify-between">
                        <span className="text-purple-300">CPU</span>
                        <span className="text-white">{systemStats.cpu_usage.toFixed(1)}%</span>
                      </div>
                      <div className="w-full bg-purple-900/50 rounded-full h-2">
                        <div
                          className="bg-blue-500 h-2 rounded-full transition-all duration-500"
                          style={{ width: `${systemStats.cpu_usage}%` }}
                        />
                      </div>
                    </div>

                    <div className="space-y-2">
                      <div className="flex justify-between">
                        <span className="text-purple-300">Memory</span>
                        <span className="text-white">{systemStats.memory_usage.toFixed(1)}%</span>
                      </div>
                      <div className="w-full bg-purple-900/50 rounded-full h-2">
                        <div
                          className="bg-green-500 h-2 rounded-full transition-all duration-500"
                          style={{ width: `${systemStats.memory_usage}%` }}
                        />
                      </div>
                    </div>

                    <div className="space-y-2">
                      <div className="flex justify-between">
                        <span className="text-purple-300">Disk</span>
                        <span className="text-white">{systemStats.disk_usage.toFixed(1)}%</span>
                      </div>
                      <div className="w-full bg-purple-900/50 rounded-full h-2">
                        <div
                          className="bg-yellow-500 h-2 rounded-full transition-all duration-500"
                          style={{ width: `${systemStats.disk_usage}%` }}
                        />
                      </div>
                    </div>
                  </CardContent>
                </Card>

                <Card className="bg-purple-800/30 border-purple-600">
                  <CardHeader>
                    <CardTitle className="text-white text-lg">System Health</CardTitle>
                  </CardHeader>
                  <CardContent className="space-y-3">
                    <div className="flex items-center justify-between">
                      <span className="text-purple-300">Overall Status</span>
                      <Badge className="bg-green-700">Healthy</Badge>
                    </div>
                    <div className="flex items-center justify-between">
                      <span className="text-purple-300">Uptime</span>
                      <span className="text-white">24h 15m</span>
                    </div>
                    <div className="flex items-center justify-between">
                      <span className="text-purple-300">Total Scans</span>
                      <span className="text-white">{systemStats.total_scans}</span>
                    </div>
                    <div className="flex items-center justify-between">
                      <span className="text-purple-300">Active Engines</span>
                      <span className="text-white">{Object.keys(systemStats.engine_stats).length}</span>
                    </div>
                  </CardContent>
                </Card>
              </div>
            </TabsContent>

            <TabsContent value="engines" className="space-y-4">
              <Card className="bg-purple-800/30 border-purple-600">
                <CardHeader>
                  <CardTitle className="text-white text-lg">Engine Status</CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="space-y-3">
                    {Object.entries(systemStats.engine_stats).map(([engineName, stats]) => (
                      <div
                        key={engineName}
                        className="flex items-center justify-between p-3 bg-purple-900/30 rounded border border-purple-700"
                      >
                        <div className="flex items-center gap-3">
                          <div className="w-2 h-2 bg-green-400 rounded-full" />
                          <span className="text-purple-300 capitalize">{engineName}</span>
                        </div>
                        <div className="flex items-center gap-4">
                          <div className="text-right">
                            <p className="text-white text-sm">{stats.scans_completed} scans</p>
                            <p className="text-purple-400 text-xs">
                              {stats.last_used ? new Date(stats.last_used).toLocaleTimeString() : "Never"}
                            </p>
                          </div>
                          <Badge className="bg-green-700">Active</Badge>
                        </div>
                      </div>
                    ))}
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
