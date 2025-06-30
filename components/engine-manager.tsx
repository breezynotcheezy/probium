"use client"

import { useState } from "react"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Switch } from "@/components/ui/switch"
import { Progress } from "@/components/ui/progress"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import {
  Cpu,
  Settings,
  Activity,
  AlertTriangle,
  CheckCircle,
  Database,
  FileText,
  Archive,
  ImageIcon,
  Binary,
  Code,
  Shield,
  BarChart3,
} from "lucide-react"

interface EngineManagerProps {
  config: any
  onConfigChange: (config: any) => void
}

export function EngineManager({ config, onConfigChange }: EngineManagerProps) {
  const [engineStats, setEngineStats] = useState({
    pdf: { status: "active", performance: 95, lastUsed: "2 min ago", scansCompleted: 1247 },
    zip: { status: "active", performance: 88, lastUsed: "5 min ago", scansCompleted: 892 },
    office: { status: "active", performance: 92, lastUsed: "1 min ago", scansCompleted: 634 },
    image: { status: "active", performance: 97, lastUsed: "3 min ago", scansCompleted: 2156 },
    binary: { status: "active", performance: 85, lastUsed: "4 min ago", scansCompleted: 445 },
    text: { status: "active", performance: 99, lastUsed: "1 min ago", scansCompleted: 3421 },
    archive: { status: "active", performance: 90, lastUsed: "6 min ago", scansCompleted: 567 },
    executable: { status: "warning", performance: 78, lastUsed: "10 min ago", scansCompleted: 234 },
  })

  const engineDetails = {
    pdf: {
      name: "PDF Engine",
      description: "Advanced PDF document analysis and metadata extraction",
      version: "2.1.4",
      capabilities: ["Structure Analysis", "Metadata Extraction", "Encryption Detection", "Form Analysis"],
      supportedFormats: ["PDF", "PDF/A", "PDF/X"],
      icon: FileText,
      color: "text-red-400",
    },
    zip: {
      name: "ZIP Archive Engine",
      description: "Compressed archive analysis and content enumeration",
      version: "1.8.2",
      capabilities: ["Archive Structure", "Compression Analysis", "Nested Archives", "Password Detection"],
      supportedFormats: ["ZIP", "RAR", "7Z", "TAR", "GZ"],
      icon: Archive,
      color: "text-yellow-400",
    },
    office: {
      name: "Office Document Engine",
      description: "Microsoft Office and OpenDocument format analysis",
      version: "3.2.1",
      capabilities: ["Document Properties", "Macro Detection", "Embedded Objects", "Version Analysis"],
      supportedFormats: ["DOCX", "XLSX", "PPTX", "ODT", "ODS"],
      icon: FileText,
      color: "text-blue-400",
    },
    image: {
      name: "Image Analysis Engine",
      description: "Comprehensive image format detection and metadata extraction",
      version: "2.5.3",
      capabilities: ["EXIF Data", "Color Analysis", "Format Validation", "Steganography Detection"],
      supportedFormats: ["JPEG", "PNG", "GIF", "TIFF", "BMP", "WEBP"],
      icon: ImageIcon,
      color: "text-green-400",
    },
    binary: {
      name: "Binary Analysis Engine",
      description: "Low-level binary file analysis and pattern recognition",
      version: "1.9.7",
      capabilities: ["Hex Analysis", "Pattern Matching", "Entropy Calculation", "Signature Detection"],
      supportedFormats: ["BIN", "EXE", "DLL", "SO", "DYLIB"],
      icon: Binary,
      color: "text-purple-400",
    },
    text: {
      name: "Text Processing Engine",
      description: "Text file encoding detection and content analysis",
      version: "2.3.8",
      capabilities: ["Encoding Detection", "Language Analysis", "Format Recognition", "Content Parsing"],
      supportedFormats: ["TXT", "CSV", "JSON", "XML", "HTML"],
      icon: Code,
      color: "text-cyan-400",
    },
    archive: {
      name: "Advanced Archive Engine",
      description: "Specialized archive format analysis with deep inspection",
      version: "1.6.5",
      capabilities: ["Deep Scanning", "Malware Detection", "Structure Validation", "Recovery Analysis"],
      supportedFormats: ["TAR.GZ", "TAR.XZ", "CAB", "ISO", "DMG"],
      icon: Database,
      color: "text-orange-400",
    },
    executable: {
      name: "Executable Analysis Engine",
      description: "Executable file analysis and security assessment",
      version: "2.0.1",
      capabilities: ["PE Analysis", "ELF Analysis", "Mach-O Analysis", "Security Scanning"],
      supportedFormats: ["EXE", "DLL", "ELF", "MACH-O", "APP"],
      icon: Shield,
      color: "text-red-500",
    },
  }

  const toggleEngine = (engineId: string) => {
    const engines = config.engines.includes(engineId)
      ? config.engines.filter((e: string) => e !== engineId)
      : [...config.engines, engineId]
    onConfigChange({ ...config, engines })
  }

  const getStatusColor = (status: string) => {
    switch (status) {
      case "active":
        return "text-green-400"
      case "warning":
        return "text-yellow-400"
      case "error":
        return "text-red-400"
      default:
        return "text-gray-400"
    }
  }

  const getStatusIcon = (status: string) => {
    switch (status) {
      case "active":
        return CheckCircle
      case "warning":
        return AlertTriangle
      case "error":
        return AlertTriangle
      default:
        return Activity
    }
  }

  return (
    <div className="space-y-6">
      {/* Engine Overview */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <Card className="bg-purple-900/30 border-purple-700">
          <CardContent className="p-4">
            <div className="flex items-center gap-3">
              <Cpu className="w-8 h-8 text-purple-400" />
              <div>
                <p className="text-sm text-purple-300">Active Engines</p>
                <p className="text-2xl font-bold text-white">{config.engines.length}</p>
              </div>
            </div>
          </CardContent>
        </Card>

        <Card className="bg-purple-900/30 border-purple-700">
          <CardContent className="p-4">
            <div className="flex items-center gap-3">
              <Activity className="w-8 h-8 text-green-400" />
              <div>
                <p className="text-sm text-purple-300">Avg Performance</p>
                <p className="text-2xl font-bold text-white">
                  {Math.round(
                    Object.values(engineStats).reduce((sum: number, stat: any) => sum + stat.performance, 0) /
                      Object.keys(engineStats).length,
                  )}
                  %
                </p>
              </div>
            </div>
          </CardContent>
        </Card>

        <Card className="bg-purple-900/30 border-purple-700">
          <CardContent className="p-4">
            <div className="flex items-center gap-3">
              <BarChart3 className="w-8 h-8 text-blue-400" />
              <div>
                <p className="text-sm text-purple-300">Total Scans</p>
                <p className="text-2xl font-bold text-white">
                  {Object.values(engineStats)
                    .reduce((sum: number, stat: any) => sum + stat.scansCompleted, 0)
                    .toLocaleString()}
                </p>
              </div>
            </div>
          </CardContent>
        </Card>

        <Card className="bg-purple-900/30 border-purple-700">
          <CardContent className="p-4">
            <div className="flex items-center gap-3">
              <AlertTriangle className="w-8 h-8 text-yellow-400" />
              <div>
                <p className="text-sm text-purple-300">Warnings</p>
                <p className="text-2xl font-bold text-white">
                  {Object.values(engineStats).filter((stat: any) => stat.status === "warning").length}
                </p>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Engine Management */}
      <Card className="bg-purple-900/30 border-purple-700">
        <CardHeader>
          <CardTitle className="text-white flex items-center gap-2">
            <Settings className="w-5 h-5" />
            Engine Configuration
          </CardTitle>
          <CardDescription className="text-purple-300">
            Manage detection engines and their configurations
          </CardDescription>
        </CardHeader>
        <CardContent>
          <Tabs defaultValue="engines" className="space-y-4">
            <TabsList className="grid w-full grid-cols-3 bg-purple-800/50">
              <TabsTrigger value="engines">Engines</TabsTrigger>
              <TabsTrigger value="performance">Performance</TabsTrigger>
              <TabsTrigger value="advanced">Advanced</TabsTrigger>
            </TabsList>

            <TabsContent value="engines" className="space-y-4">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                {Object.entries(engineDetails).map(([engineId, details]) => {
                  const IconComponent = details.icon
                  const stats = engineStats[engineId as keyof typeof engineStats]
                  const StatusIcon = getStatusIcon(stats.status)

                  return (
                    <Card key={engineId} className="bg-purple-800/30 border-purple-600">
                      <CardContent className="p-4">
                        <div className="flex items-start justify-between mb-3">
                          <div className="flex items-center gap-3">
                            <IconComponent className={`w-6 h-6 ${details.color}`} />
                            <div>
                              <h3 className="font-semibold text-white">{details.name}</h3>
                              <p className="text-xs text-purple-400">v{details.version}</p>
                            </div>
                          </div>
                          <div className="flex items-center gap-2">
                            <StatusIcon className={`w-4 h-4 ${getStatusColor(stats.status)}`} />
                            <Switch
                              checked={config.engines.includes(engineId)}
                              onCheckedChange={() => toggleEngine(engineId)}
                            />
                          </div>
                        </div>

                        <p className="text-sm text-purple-300 mb-3">{details.description}</p>

                        <div className="space-y-2">
                          <div className="flex justify-between text-xs">
                            <span className="text-purple-400">Performance</span>
                            <span className="text-white">{stats.performance}%</span>
                          </div>
                          <Progress value={stats.performance} className="h-1" />
                        </div>

                        <div className="mt-3 flex justify-between text-xs text-purple-400">
                          <span>Last used: {stats.lastUsed}</span>
                          <span>{stats.scansCompleted.toLocaleString()} scans</span>
                        </div>

                        <div className="mt-3">
                          <p className="text-xs text-purple-400 mb-1">Supported Formats:</p>
                          <div className="flex flex-wrap gap-1">
                            {details.supportedFormats.slice(0, 3).map((format) => (
                              <Badge
                                key={format}
                                variant="outline"
                                className="text-xs border-purple-600 text-purple-300"
                              >
                                {format}
                              </Badge>
                            ))}
                            {details.supportedFormats.length > 3 && (
                              <Badge variant="outline" className="text-xs border-purple-600 text-purple-300">
                                +{details.supportedFormats.length - 3}
                              </Badge>
                            )}
                          </div>
                        </div>
                      </CardContent>
                    </Card>
                  )
                })}
              </div>
            </TabsContent>

            <TabsContent value="performance" className="space-y-4">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <Card className="bg-purple-800/30 border-purple-600">
                  <CardHeader>
                    <CardTitle className="text-white text-lg">Engine Performance</CardTitle>
                  </CardHeader>
                  <CardContent className="space-y-4">
                    {Object.entries(engineStats).map(([engineId, stats]) => (
                      <div key={engineId} className="space-y-2">
                        <div className="flex justify-between">
                          <span className="text-purple-300 capitalize">{engineId}</span>
                          <span className="text-white">{stats.performance}%</span>
                        </div>
                        <Progress value={stats.performance} className="h-2" />
                      </div>
                    ))}
                  </CardContent>
                </Card>

                <Card className="bg-purple-800/30 border-purple-600">
                  <CardHeader>
                    <CardTitle className="text-white text-lg">Usage Statistics</CardTitle>
                  </CardHeader>
                  <CardContent className="space-y-4">
                    {Object.entries(engineStats).map(([engineId, stats]) => (
                      <div key={engineId} className="flex justify-between items-center">
                        <span className="text-purple-300 capitalize">{engineId}</span>
                        <div className="text-right">
                          <p className="text-white font-medium">{stats.scansCompleted.toLocaleString()}</p>
                          <p className="text-xs text-purple-400">{stats.lastUsed}</p>
                        </div>
                      </div>
                    ))}
                  </CardContent>
                </Card>
              </div>
            </TabsContent>

            <TabsContent value="advanced" className="space-y-4">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <Card className="bg-purple-800/30 border-purple-600">
                  <CardHeader>
                    <CardTitle className="text-white text-lg">Thread Pool Configuration</CardTitle>
                  </CardHeader>
                  <CardContent className="space-y-4">
                    <div className="space-y-2">
                      <Label className="text-purple-300">Pool Size</Label>
                      <Input
                        type="number"
                        value={config.threadPool}
                        onChange={(e) => onConfigChange({ ...config, threadPool: Number.parseInt(e.target.value) })}
                        className="bg-purple-900/50 border-purple-600 text-white"
                      />
                    </div>

                    <div className="space-y-2">
                      <Label className="text-purple-300">Queue Size</Label>
                      <Input
                        type="number"
                        defaultValue={100}
                        className="bg-purple-900/50 border-purple-600 text-white"
                      />
                    </div>

                    <div className="space-y-2">
                      <Label className="text-purple-300">Timeout (ms)</Label>
                      <Input
                        type="number"
                        value={config.timeout}
                        className="bg-purple-900/50 border-purple-600 text-white"
                        readOnly
                      />
                    </div>
                  </CardContent>
                </Card>

                <Card className="bg-purple-800/30 border-purple-600">
                  <CardHeader>
                    <CardTitle className="text-white text-lg">Engine Priorities</CardTitle>
                  </CardHeader>
                  <CardContent className="space-y-4">
                    <div className="space-y-3">
                      {config.engines.map((engine: string, index: number) => (
                        <div key={engine} className="flex items-center justify-between p-2 bg-purple-900/30 rounded">
                          <span className="text-purple-300 capitalize">{engine}</span>
                          <Badge variant="outline" className="border-purple-600 text-purple-300">
                            Priority {index + 1}
                          </Badge>
                        </div>
                      ))}
                    </div>
                  </CardContent>
                </Card>
              </div>
            </TabsContent>
          </Tabs>
        </CardContent>
      </Card>
    </div>
  )
}
