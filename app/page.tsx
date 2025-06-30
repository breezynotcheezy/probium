"use client"

import { useState, useEffect } from "react"
import { Card, CardContent } from "@/components/ui/card"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { FileScanner } from "@/components/file-scanner"
import { BatchProcessor } from "@/components/batch-processor"
import { EngineManager } from "@/components/engine-manager"
import { ScanResults } from "@/components/scan-results"
import { SystemMonitor } from "@/components/system-monitor"
import { AnalyticsDashboard } from "@/components/analytics-dashboard"
import { ConfigurationPanel } from "@/components/configuration-panel"
import { APIExplorer } from "@/components/api-explorer"
import { RealTimeMonitor } from "@/components/realtime-monitor"
import { ThreatDetection } from "@/components/threat-detection"
import { FileTypeRegistry } from "@/components/filetype-registry"
import { PerformanceProfiler } from "@/components/performance-profiler"
import { api, type ScanResult, type SystemMetrics, type Engine } from "@/lib/api"
import {
  Shield,
  Cpu,
  Database,
  Activity,
  BarChart3,
  Settings,
  Code,
  Eye,
  AlertTriangle,
  FileType,
  Gauge,
} from "lucide-react"

export default function ProbiumComprehensiveDashboard() {
  const [scanResults, setScanResults] = useState<ScanResult[]>([])
  const [systemStats, setSystemStats] = useState<SystemMetrics>({
    cpu_usage: 0,
    memory_usage: 0,
    memory_total: 0,
    memory_used: 0,
    disk_usage: 0,
    disk_total: 0,
    disk_used: 0,
    active_threads: 0,
    total_scans: 0,
    engine_stats: {},
    timestamp: new Date().toISOString(),
  })
  const [availableEngines, setAvailableEngines] = useState<Engine[]>([])
  const [isScanning, setIsScanning] = useState(false)
  const [config, setConfig] = useState({
    engines: [] as string[],
    threadPool: 8,
    confidenceThreshold: 0.75,
    deepAnalysis: true,
    cacheResults: true,
    verboseLogging: false,
    maxFileSize: 500 * 1024 * 1024, // 500MB
    timeout: 30000,
    enableHashing: true,
    enableMetadata: true,
    enableSignatureValidation: true,
  })

  // Fetch initial data
  useEffect(() => {
    const fetchInitialData = async () => {
      try {
        // Fetch available engines
        const enginesData = await api.getEngines()
        setAvailableEngines(enginesData.engines)

        // Update config with available engines
        setConfig((prev) => ({
          ...prev,
          engines: enginesData.engines.map((e) => e.name),
        }))

        // Fetch system metrics
        const metrics = await api.getSystemMetrics()
        setSystemStats(metrics)

        // Fetch scan history
        const history = await api.getScanHistory(50)
        setScanResults(history.scans)
      } catch (error) {
        console.error("Failed to fetch initial data:", error)
      }
    }

    fetchInitialData()
  }, [])

  // Update system metrics periodically
  useEffect(() => {
    const interval = setInterval(async () => {
      try {
        const metrics = await api.getSystemMetrics()
        setSystemStats(metrics)
      } catch (error) {
        console.error("Failed to fetch system metrics:", error)
      }
    }, 5000) // Update every 5 seconds

    return () => clearInterval(interval)
  }, [])

  const handleScanComplete = (result: ScanResult) => {
    setScanResults((prev) => [result, ...prev])
  }

  const handleBatchComplete = (results: ScanResult[]) => {
    setScanResults((prev) => [...results, ...prev])
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-950 via-purple-900 to-indigo-950">
      <div className="container mx-auto p-6">
        {/* Header */}
        <div className="mb-8">
          <div className="flex items-center justify-between mb-6">
            <div className="flex items-center gap-4">
              <div className="w-16 h-16 bg-gradient-to-br from-purple-600 to-purple-800 rounded-xl flex items-center justify-center shadow-lg">
                <Shield className="w-8 h-8 text-white" />
              </div>
              <div>
                <h1 className="text-4xl font-bold text-white mb-2">Probium Advanced Scanner</h1>
                <p className="text-purple-200">
                  Comprehensive file analysis with {availableEngines.length} detection engines
                </p>
              </div>
            </div>
            <div className="flex items-center gap-4">
              <div className="text-right">
                <p className="text-sm text-purple-300">System Status</p>
                <div className="flex items-center gap-2">
                  <div className="w-2 h-2 bg-green-400 rounded-full animate-pulse"></div>
                  <span className="text-green-400 font-medium">Online</span>
                </div>
              </div>
            </div>
          </div>

          {/* Quick Stats */}
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-6 gap-4 mb-6">
            <Card className="bg-purple-900/50 border-purple-700">
              <CardContent className="p-4">
                <div className="flex items-center gap-3">
                  <Database className="w-8 h-8 text-purple-400" />
                  <div>
                    <p className="text-sm text-purple-300">Total Scans</p>
                    <p className="text-xl font-bold text-white">{systemStats.total_scans}</p>
                  </div>
                </div>
              </CardContent>
            </Card>
            <Card className="bg-purple-900/50 border-purple-700">
              <CardContent className="p-4">
                <div className="flex items-center gap-3">
                  <Cpu className="w-8 h-8 text-blue-400" />
                  <div>
                    <p className="text-sm text-purple-300">Active Threads</p>
                    <p className="text-xl font-bold text-white">{systemStats.active_threads}</p>
                  </div>
                </div>
              </CardContent>
            </Card>
            <Card className="bg-purple-900/50 border-purple-700">
              <CardContent className="p-4">
                <div className="flex items-center gap-3">
                  <Activity className="w-8 h-8 text-green-400" />
                  <div>
                    <p className="text-sm text-purple-300">CPU Usage</p>
                    <p className="text-xl font-bold text-white">{systemStats.cpu_usage.toFixed(1)}%</p>
                  </div>
                </div>
              </CardContent>
            </Card>
            <Card className="bg-purple-900/50 border-purple-700">
              <CardContent className="p-4">
                <div className="flex items-center gap-3">
                  <Gauge className="w-8 h-8 text-yellow-400" />
                  <div>
                    <p className="text-sm text-purple-300">Memory</p>
                    <p className="text-xl font-bold text-white">{systemStats.memory_usage.toFixed(1)}%</p>
                  </div>
                </div>
              </CardContent>
            </Card>
            <Card className="bg-purple-900/50 border-purple-700">
              <CardContent className="p-4">
                <div className="flex items-center gap-3">
                  <Shield className="w-8 h-8 text-red-400" />
                  <div>
                    <p className="text-sm text-purple-300">Threats</p>
                    <p className="text-xl font-bold text-white">
                      {scanResults.filter((r) => r.security?.threat_level !== "low").length}
                    </p>
                  </div>
                </div>
              </CardContent>
            </Card>
            <Card className="bg-purple-900/50 border-purple-700">
              <CardContent className="p-4">
                <div className="flex items-center gap-3">
                  <FileType className="w-8 h-8 text-purple-400" />
                  <div>
                    <p className="text-sm text-purple-300">Engines</p>
                    <p className="text-xl font-bold text-white">{availableEngines.length}</p>
                  </div>
                </div>
              </CardContent>
            </Card>
          </div>
        </div>

        {/* Main Interface */}
        <Tabs defaultValue="scanner" className="space-y-6">
          <TabsList className="grid w-full grid-cols-6 lg:grid-cols-12 bg-purple-900/50 border-purple-700">
            <TabsTrigger value="scanner" className="data-[state=active]:bg-purple-700">
              <Shield className="w-4 h-4 mr-2" />
              Scanner
            </TabsTrigger>
            <TabsTrigger value="batch" className="data-[state=active]:bg-purple-700">
              <Database className="w-4 h-4 mr-2" />
              Batch
            </TabsTrigger>
            <TabsTrigger value="engines" className="data-[state=active]:bg-purple-700">
              <Cpu className="w-4 h-4 mr-2" />
              Engines
            </TabsTrigger>
            <TabsTrigger value="results" className="data-[state=active]:bg-purple-700">
              <BarChart3 className="w-4 h-4 mr-2" />
              Results
            </TabsTrigger>
            <TabsTrigger value="monitor" className="data-[state=active]:bg-purple-700">
              <Activity className="w-4 h-4 mr-2" />
              Monitor
            </TabsTrigger>
            <TabsTrigger value="analytics" className="data-[state=active]:bg-purple-700">
              <BarChart3 className="w-4 h-4 mr-2" />
              Analytics
            </TabsTrigger>
            <TabsTrigger value="threats" className="data-[state=active]:bg-purple-700">
              <AlertTriangle className="w-4 h-4 mr-2" />
              Threats
            </TabsTrigger>
            <TabsTrigger value="registry" className="data-[state=active]:bg-purple-700">
              <FileType className="w-4 h-4 mr-2" />
              Registry
            </TabsTrigger>
            <TabsTrigger value="profiler" className="data-[state=active]:bg-purple-700">
              <Gauge className="w-4 h-4 mr-2" />
              Profiler
            </TabsTrigger>
            <TabsTrigger value="api" className="data-[state=active]:bg-purple-700">
              <Code className="w-4 h-4 mr-2" />
              API
            </TabsTrigger>
            <TabsTrigger value="realtime" className="data-[state=active]:bg-purple-700">
              <Eye className="w-4 h-4 mr-2" />
              Live
            </TabsTrigger>
            <TabsTrigger value="config" className="data-[state=active]:bg-purple-700">
              <Settings className="w-4 h-4 mr-2" />
              Config
            </TabsTrigger>
          </TabsList>

          <TabsContent value="scanner">
            <FileScanner onScanComplete={handleScanComplete} config={config} setIsScanning={setIsScanning} />
          </TabsContent>

          <TabsContent value="batch">
            <BatchProcessor onBatchComplete={handleBatchComplete} config={config} setIsScanning={setIsScanning} />
          </TabsContent>

          <TabsContent value="engines">
            <EngineManager
              config={config}
              onConfigChange={setConfig}
              availableEngines={availableEngines}
              systemStats={systemStats}
            />
          </TabsContent>

          <TabsContent value="results">
            <ScanResults results={scanResults} onClear={() => setScanResults([])} />
          </TabsContent>

          <TabsContent value="monitor">
            <SystemMonitor systemStats={systemStats} config={config} />
          </TabsContent>

          <TabsContent value="analytics">
            <AnalyticsDashboard results={scanResults} systemStats={systemStats} />
          </TabsContent>

          <TabsContent value="threats">
            <ThreatDetection results={scanResults} config={config} />
          </TabsContent>

          <TabsContent value="registry">
            <FileTypeRegistry config={config} onConfigChange={setConfig} />
          </TabsContent>

          <TabsContent value="profiler">
            <PerformanceProfiler results={scanResults} systemStats={systemStats} />
          </TabsContent>

          <TabsContent value="api">
            <APIExplorer config={config} />
          </TabsContent>

          <TabsContent value="realtime">
            <RealTimeMonitor systemStats={systemStats} isScanning={isScanning} />
          </TabsContent>

          <TabsContent value="config">
            <ConfigurationPanel config={config} onConfigChange={setConfig} />
          </TabsContent>
        </Tabs>
      </div>
    </div>
  )
}
