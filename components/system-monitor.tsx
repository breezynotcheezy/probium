"use client"

import { useState, useEffect } from "react"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Progress } from "@/components/ui/progress"
import { Badge } from "@/components/ui/badge"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { Activity, Cpu, HardDrive, MemoryStick, Network, Server, AlertTriangle, CheckCircle } from "lucide-react"

interface SystemMonitorProps {
  systemStats: any
  config: any
}

export function SystemMonitor({ systemStats, config }: SystemMonitorProps) {
  const [realTimeStats, setRealTimeStats] = useState({
    cpu: { usage: 0, cores: 8, temperature: 45 },
    memory: { used: 0, total: 16384, available: 16384 },
    disk: { used: 45, total: 500, read: 0, write: 0 },
    network: { in: 0, out: 0, connections: 12 },
    processes: { total: 156, probium: 8, threads: 0 },
  })

  useEffect(() => {
    const interval = setInterval(() => {
      setRealTimeStats((prev) => ({
        cpu: {
          ...prev.cpu,
          usage: Math.max(0, Math.min(100, prev.cpu.usage + (Math.random() - 0.5) * 10)),
          temperature: Math.max(35, Math.min(75, prev.cpu.temperature + (Math.random() - 0.5) * 2)),
        },
        memory: {
          ...prev.memory,
          used: Math.max(0, Math.min(prev.memory.total, prev.memory.used + (Math.random() - 0.5) * 500)),
          available: prev.memory.total - prev.memory.used,
        },
        disk: {
          ...prev.disk,
          read: Math.random() * 100,
          write: Math.random() * 50,
        },
        network: {
          ...prev.network,
          in: Math.random() * 1000,
          out: Math.random() * 500,
        },
        processes: {
          ...prev.processes,
          threads: systemStats.activeThreads || 0,
        },
      }))
    }, 2000)

    return () => clearInterval(interval)
  }, [systemStats.activeThreads])

  const getStatusColor = (value: number, thresholds: { warning: number; critical: number }) => {
    if (value >= thresholds.critical) return "text-red-400"
    if (value >= thresholds.warning) return "text-yellow-400"
    return "text-green-400"
  }

  const getStatusIcon = (value: number, thresholds: { warning: number; critical: number }) => {
    if (value >= thresholds.critical) return AlertTriangle
    if (value >= thresholds.warning) return AlertTriangle
    return CheckCircle
  }

  return (
    <div className="space-y-6">
      {/* System Overview */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        <Card className="bg-purple-900/30 border-purple-700">
          <CardContent className="p-4">
            <div className="flex items-center gap-3">
              <Cpu className={`w-8 h-8 ${getStatusColor(realTimeStats.cpu.usage, { warning: 70, critical: 90 })}`} />
              <div>
                <p className="text-sm text-purple-300">CPU Usage</p>
                <p className="text-2xl font-bold text-white">{realTimeStats.cpu.usage.toFixed(1)}%</p>
              </div>
            </div>
            <Progress value={realTimeStats.cpu.usage} className="mt-2 bg-purple-800" />
          </CardContent>
        </Card>

        <Card className="bg-purple-900/30 border-purple-700">
          <CardContent className="p-4">
            <div className="flex items-center gap-3">
              <MemoryStick
                className={`w-8 h-8 ${getStatusColor((realTimeStats.memory.used / realTimeStats.memory.total) * 100, { warning: 70, critical: 90 })}`}
              />
              <div>
                <p className="text-sm text-purple-300">Memory</p>
                <p className="text-2xl font-bold text-white">
                  {((realTimeStats.memory.used / realTimeStats.memory.total) * 100).toFixed(1)}%
                </p>
              </div>
            </div>
            <Progress
              value={(realTimeStats.memory.used / realTimeStats.memory.total) * 100}
              className="mt-2 bg-purple-800"
            />
          </CardContent>
        </Card>

        <Card className="bg-purple-900/30 border-purple-700">
          <CardContent className="p-4">
            <div className="flex items-center gap-3">
              <HardDrive
                className={`w-8 h-8 ${getStatusColor((realTimeStats.disk.used / realTimeStats.disk.total) * 100, { warning: 80, critical: 95 })}`}
              />
              <div>
                <p className="text-sm text-purple-300">Disk Usage</p>
                <p className="text-2xl font-bold text-white">
                  {((realTimeStats.disk.used / realTimeStats.disk.total) * 100).toFixed(1)}%
                </p>
              </div>
            </div>
            <Progress
              value={(realTimeStats.disk.used / realTimeStats.disk.total) * 100}
              className="mt-2 bg-purple-800"
            />
          </CardContent>
        </Card>

        <Card className="bg-purple-900/30 border-purple-700">
          <CardContent className="p-4">
            <div className="flex items-center gap-3">
              <Activity className="w-8 h-8 text-blue-400" />
              <div>
                <p className="text-sm text-purple-300">Active Threads</p>
                <p className="text-2xl font-bold text-white">{realTimeStats.processes.threads}</p>
              </div>
            </div>
            <div className="mt-2 text-xs text-purple-400">Max: {config.threadPool}</div>
          </CardContent>
        </Card>
      </div>

      {/* Detailed Monitoring */}
      <Card className="bg-purple-900/30 border-purple-700">
        <CardHeader>
          <CardTitle className="text-white flex items-center gap-2">
            <Server className="w-5 h-5" />
            System Monitoring
          </CardTitle>
          <CardDescription className="text-purple-300">
            Real-time system performance and resource utilization
          </CardDescription>
        </CardHeader>
        <CardContent>
          <Tabs defaultValue="performance" className="space-y-4">
            <TabsList className="grid w-full grid-cols-4 bg-purple-800/50">
              <TabsTrigger value="performance">Performance</TabsTrigger>
              <TabsTrigger value="processes">Processes</TabsTrigger>
              <TabsTrigger value="network">Network</TabsTrigger>
              <TabsTrigger value="alerts">Alerts</TabsTrigger>
            </TabsList>

            <TabsContent value="performance" className="space-y-4">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <Card className="bg-purple-800/30 border-purple-600">
                  <CardHeader>
                    <CardTitle className="text-white text-lg flex items-center gap-2">
                      <Cpu className="w-5 h-5" />
                      CPU Metrics
                    </CardTitle>
                  </CardHeader>
                  <CardContent className="space-y-4">
                    <div className="space-y-3">
                      <div className="flex justify-between">
                        <span className="text-purple-300">Usage</span>
                        <span className="text-white">{realTimeStats.cpu.usage.toFixed(1)}%</span>
                      </div>
                      <Progress value={realTimeStats.cpu.usage} className="bg-purple-900" />
                    </div>

                    <div className="grid grid-cols-2 gap-4 pt-2">
                      <div className="text-center p-2 bg-purple-900/50 rounded">
                        <p className="text-xs text-purple-400">Cores</p>
                        <p className="text-lg font-bold text-white">{realTimeStats.cpu.cores}</p>
                      </div>
                      <div className="text-center p-2 bg-purple-900/50 rounded">
                        <p className="text-xs text-purple-400">Temperature</p>
                        <p className="text-lg font-bold text-white">{realTimeStats.cpu.temperature.toFixed(0)}°C</p>
                      </div>
                    </div>
                  </CardContent>
                </Card>

                <Card className="bg-purple-800/30 border-purple-600">
                  <CardHeader>
                    <CardTitle className="text-white text-lg flex items-center gap-2">
                      <MemoryStick className="w-5 h-5" />
                      Memory Usage
                    </CardTitle>
                  </CardHeader>
                  <CardContent className="space-y-4">
                    <div className="space-y-3">
                      <div className="flex justify-between">
                        <span className="text-purple-300">Used</span>
                        <span className="text-white">
                          {(realTimeStats.memory.used / 1024).toFixed(1)} /{" "}
                          {(realTimeStats.memory.total / 1024).toFixed(1)} GB
                        </span>
                      </div>
                      <Progress
                        value={(realTimeStats.memory.used / realTimeStats.memory.total) * 100}
                        className="bg-purple-900"
                      />
                    </div>

                    <div className="grid grid-cols-2 gap-4 pt-2">
                      <div className="text-center p-2 bg-purple-900/50 rounded">
                        <p className="text-xs text-purple-400">Available</p>
                        <p className="text-lg font-bold text-white">
                          {(realTimeStats.memory.available / 1024).toFixed(1)} GB
                        </p>
                      </div>
                      <div className="text-center p-2 bg-purple-900/50 rounded">
                        <p className="text-xs text-purple-400">Usage %</p>
                        <p className="text-lg font-bold text-white">
                          {((realTimeStats.memory.used / realTimeStats.memory.total) * 100).toFixed(1)}%
                        </p>
                      </div>
                    </div>
                  </CardContent>
                </Card>
              </div>

              <Card className="bg-purple-800/30 border-purple-600">
                <CardHeader>
                  <CardTitle className="text-white text-lg flex items-center gap-2">
                    <HardDrive className="w-5 h-5" />
                    Disk I/O
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
                    <div className="text-center p-3 bg-purple-900/50 rounded">
                      <p className="text-xs text-purple-400">Disk Usage</p>
                      <p className="text-xl font-bold text-white">
                        {((realTimeStats.disk.used / realTimeStats.disk.total) * 100).toFixed(1)}%
                      </p>
                    </div>
                    <div className="text-center p-3 bg-purple-900/50 rounded">
                      <p className="text-xs text-purple-400">Free Space</p>
                      <p className="text-xl font-bold text-white">
                        {(realTimeStats.disk.total - realTimeStats.disk.used).toFixed(0)} GB
                      </p>
                    </div>
                    <div className="text-center p-3 bg-purple-900/50 rounded">
                      <p className="text-xs text-purple-400">Read Speed</p>
                      <p className="text-xl font-bold text-white">{realTimeStats.disk.read.toFixed(1)} MB/s</p>
                    </div>
                    <div className="text-center p-3 bg-purple-900/50 rounded">
                      <p className="text-xs text-purple-400">Write Speed</p>
                      <p className="text-xl font-bold text-white">{realTimeStats.disk.write.toFixed(1)} MB/s</p>
                    </div>
                  </div>
                </CardContent>
              </Card>
            </TabsContent>

            <TabsContent value="processes" className="space-y-4">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <Card className="bg-purple-800/30 border-purple-600">
                  <CardHeader>
                    <CardTitle className="text-white text-lg">Probium Processes</CardTitle>
                  </CardHeader>
                  <CardContent className="space-y-3">
                    <div className="flex justify-between items-center p-2 bg-purple-900/50 rounded">
                      <span className="text-purple-300">Main Process</span>
                      <Badge className="bg-green-700">Running</Badge>
                    </div>
                    <div className="flex justify-between items-center p-2 bg-purple-900/50 rounded">
                      <span className="text-purple-300">Worker Threads</span>
                      <Badge className="bg-blue-700">{realTimeStats.processes.threads}</Badge>
                    </div>
                    <div className="flex justify-between items-center p-2 bg-purple-900/50 rounded">
                      <span className="text-purple-300">Engine Processes</span>
                      <Badge className="bg-purple-700">{config.engines.length}</Badge>
                    </div>
                  </CardContent>
                </Card>

                <Card className="bg-purple-800/30 border-purple-600">
                  <CardHeader>
                    <CardTitle className="text-white text-lg">System Processes</CardTitle>
                  </CardHeader>
                  <CardContent className="space-y-3">
                    <div className="flex justify-between items-center">
                      <span className="text-purple-300">Total Processes</span>
                      <span className="text-white font-bold">{realTimeStats.processes.total}</span>
                    </div>
                    <div className="flex justify-between items-center">
                      <span className="text-purple-300">Probium Processes</span>
                      <span className="text-white font-bold">{realTimeStats.processes.probium}</span>
                    </div>
                    <div className="flex justify-between items-center">
                      <span className="text-purple-300">Thread Pool Size</span>
                      <span className="text-white font-bold">{config.threadPool}</span>
                    </div>
                  </CardContent>
                </Card>
              </div>
            </TabsContent>

            <TabsContent value="network" className="space-y-4">
              <Card className="bg-purple-800/30 border-purple-600">
                <CardHeader>
                  <CardTitle className="text-white text-lg flex items-center gap-2">
                    <Network className="w-5 h-5" />
                    Network Activity
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                    <div className="text-center p-4 bg-purple-900/50 rounded">
                      <p className="text-sm text-purple-400">Incoming</p>
                      <p className="text-2xl font-bold text-white">{realTimeStats.network.in.toFixed(1)} KB/s</p>
                    </div>
                    <div className="text-center p-4 bg-purple-900/50 rounded">
                      <p className="text-sm text-purple-400">Outgoing</p>
                      <p className="text-2xl font-bold text-white">{realTimeStats.network.out.toFixed(1)} KB/s</p>
                    </div>
                    <div className="text-center p-4 bg-purple-900/50 rounded">
                      <p className="text-sm text-purple-400">Connections</p>
                      <p className="text-2xl font-bold text-white">{realTimeStats.network.connections}</p>
                    </div>
                  </div>
                </CardContent>
              </Card>
            </TabsContent>

            <TabsContent value="alerts" className="space-y-4">
              <div className="space-y-3">
                <Card className="bg-green-900/30 border-green-700">
                  <CardContent className="p-4">
                    <div className="flex items-center gap-3">
                      <CheckCircle className="w-5 h-5 text-green-400" />
                      <div>
                        <p className="text-green-300 font-medium">System Status: Normal</p>
                        <p className="text-green-200 text-sm">All systems operating within normal parameters</p>
                      </div>
                    </div>
                  </CardContent>
                </Card>

                {realTimeStats.cpu.usage > 80 && (
                  <Card className="bg-yellow-900/30 border-yellow-700">
                    <CardContent className="p-4">
                      <div className="flex items-center gap-3">
                        <AlertTriangle className="w-5 h-5 text-yellow-400" />
                        <div>
                          <p className="text-yellow-300 font-medium">High CPU Usage</p>
                          <p className="text-yellow-200 text-sm">
                            CPU usage is at {realTimeStats.cpu.usage.toFixed(1)}%
                          </p>
                        </div>
                      </div>
                    </CardContent>
                  </Card>
                )}

                {(realTimeStats.memory.used / realTimeStats.memory.total) * 100 > 85 && (
                  <Card className="bg-red-900/30 border-red-700">
                    <CardContent className="p-4">
                      <div className="flex items-center gap-3">
                        <AlertTriangle className="w-5 h-5 text-red-400" />
                        <div>
                          <p className="text-red-300 font-medium">Memory Usage Critical</p>
                          <p className="text-red-200 text-sm">
                            Memory usage is at{" "}
                            {((realTimeStats.memory.used / realTimeStats.memory.total) * 100).toFixed(1)}%
                          </p>
                        </div>
                      </div>
                    </CardContent>
                  </Card>
                )}
              </div>
            </TabsContent>
          </Tabs>
        </CardContent>
      </Card>
    </div>
  )
}
