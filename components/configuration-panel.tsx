"use client"

import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Label } from "@/components/ui/label"
import { Switch } from "@/components/ui/switch"
import { Slider } from "@/components/ui/slider"
import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Textarea } from "@/components/ui/textarea"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { Settings, Cpu, Shield, Zap, Database, AlertTriangle } from "lucide-react"

interface ConfigurationPanelProps {
  config: any
  onConfigChange: (config: any) => void
}

export function ConfigurationPanel({ config, onConfigChange }: ConfigurationPanelProps) {
  const updateConfig = (key: string, value: any) => {
    onConfigChange({ ...config, [key]: value })
  }

  const resetToDefaults = () => {
    onConfigChange({
      engines: ["pdf", "zip", "office", "image", "binary", "text"],
      threadPool: 8,
      confidenceThreshold: 0.75,
      deepAnalysis: true,
      cacheResults: true,
      verboseLogging: false,
      maxFileSize: 500 * 1024 * 1024,
      timeout: 30000,
      enableHashing: true,
      enableMetadata: true,
      enableSignatureValidation: true,
    })
  }

  return (
    <div className="space-y-6">
      <Card className="bg-purple-50 border-purple-300">
        <CardHeader>
          <div className="flex items-center gap-3">
            <Settings className="w-6 h-6 text-purple-600" />
            <div>
              <CardTitle className="text-white">Probium Configuration</CardTitle>
              <CardDescription className="text-purple-700">
                Configure detection engines, performance settings, and advanced options
              </CardDescription>
            </div>
          </div>
        </CardHeader>
        <CardContent>
          <Tabs defaultValue="engines" className="space-y-4">
            <TabsList className="grid w-full grid-cols-4 bg-purple-100">
              <TabsTrigger value="engines">Engines</TabsTrigger>
              <TabsTrigger value="performance">Performance</TabsTrigger>
              <TabsTrigger value="security">Security</TabsTrigger>
              <TabsTrigger value="advanced">Advanced</TabsTrigger>
            </TabsList>

            <TabsContent value="engines" className="space-y-4">
              <Card className="bg-purple-50 border-purple-300">
                <CardHeader>
                  <CardTitle className="text-white text-lg flex items-center gap-2">
                    <Shield className="w-5 h-5" />
                    Detection Engines
                  </CardTitle>
                  <CardDescription className="text-purple-700">
                    Select which file type detection engines to use during scanning
                  </CardDescription>
                </CardHeader>
                <CardContent className="space-y-4">
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    {[
                      {
                        id: "pdf",
                        name: "PDF Engine",
                        description: "Detects PDF documents and metadata",
                        color: "text-red-400",
                      },
                      {
                        id: "zip",
                        name: "ZIP Engine",
                        description: "Analyzes compressed archives",
                        color: "text-yellow-400",
                      },
                      {
                        id: "office",
                        name: "Office Engine",
                        description: "Microsoft Office documents",
                        color: "text-blue-400",
                      },
                      {
                        id: "image",
                        name: "Image Engine",
                        description: "Image files and formats",
                        color: "text-green-400",
                      },
                      {
                        id: "binary",
                        name: "Binary Engine",
                        description: "Binary file analysis",
                        color: "text-purple-600",
                      },
                      {
                        id: "text",
                        name: "Text Engine",
                        description: "Plain text and encoding detection",
                        color: "text-cyan-400",
                      },
                      {
                        id: "archive",
                        name: "Archive Engine",
                        description: "Advanced archive formats",
                        color: "text-orange-400",
                      },
                      {
                        id: "executable",
                        name: "Executable Engine",
                        description: "Executable file analysis",
                        color: "text-red-500",
                      },
                    ].map((engine) => (
                      <div
                        key={engine.id}
                        className="flex items-center space-x-3 p-3 border border-purple-300 rounded-lg bg-purple-50"
                      >
                        <Switch
                          checked={config.engines.includes(engine.id)}
                          onCheckedChange={(checked) => {
                            const engines = checked
                              ? [...config.engines, engine.id]
                              : config.engines.filter((e: string) => e !== engine.id)
                            updateConfig("engines", engines)
                          }}
                        />
                        <div className="flex-1">
                          <Label className={`font-medium ${engine.color}`}>{engine.name}</Label>
                          <p className="text-sm text-purple-600">{engine.description}</p>
                        </div>
                      </div>
                    ))}
                  </div>

                  <div className="flex items-center gap-2 pt-2">
                    <span className="text-sm font-medium text-purple-700">Active engines:</span>
                    {config.engines.map((engine: string) => (
                      <Badge key={engine} variant="secondary" className="bg-purple-500 text-purple-500">
                        {engine}
                      </Badge>
                    ))}
                  </div>
                </CardContent>
              </Card>
            </TabsContent>

            <TabsContent value="performance" className="space-y-4">
              <Card className="bg-purple-50 border-purple-300">
                <CardHeader>
                  <CardTitle className="text-white text-lg flex items-center gap-2">
                    <Cpu className="w-5 h-5" />
                    Performance Settings
                  </CardTitle>
                  <CardDescription className="text-purple-700">
                    Configure parallel processing and performance parameters
                  </CardDescription>
                </CardHeader>
                <CardContent className="space-y-6">
                  <div className="space-y-3">
                    <div className="flex items-center justify-between">
                      <Label className="text-white">Thread Pool Size</Label>
                      <Badge variant="outline" className="border-purple-300 text-purple-700">
                        {config.threadPool} threads
                      </Badge>
                    </div>
                    <Slider
                      value={[config.threadPool]}
                      onValueChange={(value) => updateConfig("threadPool", value[0])}
                      max={32}
                      min={1}
                      step={1}
                      className="w-full"
                    />
                    <p className="text-sm text-purple-600">
                      Number of parallel threads for batch processing. Higher values may improve performance but use
                      more system resources.
                    </p>
                  </div>

                  <div className="space-y-3">
                    <div className="flex items-center justify-between">
                      <Label className="text-white">Confidence Threshold</Label>
                      <Badge variant="outline" className="border-purple-300 text-purple-700">
                        {(config.confidenceThreshold * 100).toFixed(0)}%
                      </Badge>
                    </div>
                    <Slider
                      value={[config.confidenceThreshold]}
                      onValueChange={(value) => updateConfig("confidenceThreshold", value[0])}
                      max={1}
                      min={0.1}
                      step={0.05}
                      className="w-full"
                    />
                    <p className="text-sm text-purple-600">
                      Minimum confidence level required for file type detection. Lower values may detect more files but
                      with less certainty.
                    </p>
                  </div>

                  <div className="space-y-3">
                    <div className="flex items-center justify-between">
                      <Label className="text-white">Max File Size</Label>
                      <Badge variant="outline" className="border-purple-300 text-purple-700">
                        {(config.maxFileSize / 1024 / 1024).toFixed(0)} MB
                      </Badge>
                    </div>
                    <Slider
                      value={[config.maxFileSize / 1024 / 1024]}
                      onValueChange={(value) => updateConfig("maxFileSize", value[0] * 1024 * 1024)}
                      max={1000}
                      min={1}
                      step={10}
                      className="w-full"
                    />
                    <p className="text-sm text-purple-600">
                      Maximum file size that can be processed. Larger files may require more memory and processing time.
                    </p>
                  </div>

                  <div className="space-y-3">
                    <div className="flex items-center justify-between">
                      <Label className="text-white">Timeout</Label>
                      <Badge variant="outline" className="border-purple-300 text-purple-700">
                        {(config.timeout / 1000).toFixed(0)}s
                      </Badge>
                    </div>
                    <Slider
                      value={[config.timeout / 1000]}
                      onValueChange={(value) => updateConfig("timeout", value[0] * 1000)}
                      max={120}
                      min={5}
                      step={5}
                      className="w-full"
                    />
                    <p className="text-sm text-purple-600">
                      Maximum time allowed for file processing before timeout. Increase for large or complex files.
                    </p>
                  </div>
                </CardContent>
              </Card>
            </TabsContent>

            <TabsContent value="security" className="space-y-4">
              <Card className="bg-purple-50 border-purple-300">
                <CardHeader>
                  <CardTitle className="text-white text-lg flex items-center gap-2">
                    <Shield className="w-5 h-5" />
                    Security Options
                  </CardTitle>
                </CardHeader>
                <CardContent className="space-y-4">
                  <div className="flex items-center justify-between">
                    <div>
                      <Label className="text-white">Enable Hashing</Label>
                      <p className="text-sm text-purple-600">Generate MD5, SHA1, SHA256, and CRC32 hashes</p>
                    </div>
                    <Switch
                      checked={config.enableHashing}
                      onCheckedChange={(checked) => updateConfig("enableHashing", checked)}
                    />
                  </div>

                  <div className="flex items-center justify-between">
                    <div>
                      <Label className="text-white">Metadata Extraction</Label>
                      <p className="text-sm text-purple-600">Extract file metadata and properties</p>
                    </div>
                    <Switch
                      checked={config.enableMetadata}
                      onCheckedChange={(checked) => updateConfig("enableMetadata", checked)}
                    />
                  </div>

                  <div className="flex items-center justify-between">
                    <div>
                      <Label className="text-white">Signature Validation</Label>
                      <p className="text-sm text-purple-600">Validate digital signatures and certificates</p>
                    </div>
                    <Switch
                      checked={config.enableSignatureValidation}
                      onCheckedChange={(checked) => updateConfig("enableSignatureValidation", checked)}
                    />
                  </div>

                  <div className="flex items-center justify-between">
                    <div>
                      <Label className="text-white">Deep Analysis</Label>
                      <p className="text-sm text-purple-600">
                        Perform thorough content analysis and structure validation
                      </p>
                    </div>
                    <Switch
                      checked={config.deepAnalysis}
                      onCheckedChange={(checked) => updateConfig("deepAnalysis", checked)}
                    />
                  </div>
                </CardContent>
              </Card>
            </TabsContent>

            <TabsContent value="advanced" className="space-y-4">
              <Card className="bg-purple-50 border-purple-300">
                <CardHeader>
                  <CardTitle className="text-white text-lg flex items-center gap-2">
                    <Zap className="w-5 h-5" />
                    Advanced Options
                  </CardTitle>
                </CardHeader>
                <CardContent className="space-y-4">
                  <div className="flex items-center justify-between">
                    <div>
                      <Label className="text-white">Cache Results</Label>
                      <p className="text-sm text-purple-600">Cache scan results for faster re-scanning</p>
                    </div>
                    <Switch
                      checked={config.cacheResults}
                      onCheckedChange={(checked) => updateConfig("cacheResults", checked)}
                    />
                  </div>

                  <div className="flex items-center justify-between">
                    <div>
                      <Label className="text-white">Verbose Logging</Label>
                      <p className="text-sm text-purple-600">Enable detailed logging output</p>
                    </div>
                    <Switch
                      checked={config.verboseLogging}
                      onCheckedChange={(checked) => updateConfig("verboseLogging", checked)}
                    />
                  </div>

                  <div className="space-y-2">
                    <Label className="text-white">Custom Engine Path</Label>
                    <Input
                      placeholder="/path/to/custom/engines"
                      className="bg-purple-50 border-purple-300 text-white placeholder-purple-400"
                    />
                    <p className="text-sm text-purple-600">Path to custom detection engines</p>
                  </div>

                  <div className="space-y-2">
                    <Label className="text-white">Configuration Notes</Label>
                    <Textarea
                      placeholder="Add notes about this configuration..."
                      className="bg-purple-50 border-purple-300 text-white placeholder-purple-400"
                      rows={3}
                    />
                  </div>
                </CardContent>
              </Card>

              <Card className="bg-purple-50 border-purple-300">
                <CardHeader>
                  <CardTitle className="text-white text-lg flex items-center gap-2">
                    <Database className="w-5 h-5" />
                    Configuration Management
                  </CardTitle>
                </CardHeader>
                <CardContent className="space-y-4">
                  <div className="flex gap-2">
                    <Button className="flex-1 bg-purple-400 hover:bg-purple-500">Save Configuration</Button>
                    <Button variant="outline" className="flex-1 border-purple-300 text-purple-700 bg-transparent">
                      Load Configuration
                    </Button>
                  </div>

                  <div className="flex gap-2">
                    <Button variant="outline" className="flex-1 border-purple-300 text-purple-700 bg-transparent">
                      Export Settings
                    </Button>
                    <Button
                      onClick={resetToDefaults}
                      variant="outline"
                      className="flex-1 border-red-600 text-red-300 hover:bg-red-900/30 bg-transparent"
                    >
                      Reset to Defaults
                    </Button>
                  </div>

                  <div className="p-3 bg-yellow-900/30 border border-yellow-700 rounded">
                    <div className="flex items-center gap-2">
                      <AlertTriangle className="w-4 h-4 text-yellow-400" />
                      <span className="text-yellow-300 font-medium">Configuration Warning</span>
                    </div>
                    <p className="text-yellow-200 text-sm mt-1">
                      Changes to engine configuration require a restart to take effect.
                    </p>
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
