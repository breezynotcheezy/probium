"use client"

import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Label } from "@/components/ui/label"
import { Switch } from "@/components/ui/switch"
import { Slider } from "@/components/ui/slider"
import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import { Settings, Cpu, Shield, Zap } from "lucide-react"

interface ConfigPanelProps {
  config: any
  onConfigChange: (config: any) => void
}

export function ConfigPanel({ config, onConfigChange }: ConfigPanelProps) {
  const updateConfig = (key: string, value: any) => {
    onConfigChange({ ...config, [key]: value })
  }

  const toggleEngine = (engine: string) => {
    const engines = config.engines.includes(engine)
      ? config.engines.filter((e: string) => e !== engine)
      : [...config.engines, engine]
    updateConfig("engines", engines)
  }

  const resetToDefaults = () => {
    onConfigChange({
      engines: ["pdf", "zip", "office"],
      threadPool: 4,
      confidenceThreshold: 0.8,
    })
  }

  return (
    <div className="space-y-6">
      {/* Configuration Header */}
      <Card>
        <CardHeader>
          <div className="flex items-center gap-3">
            <Settings className="w-6 h-6 text-blue-600" />
            <div>
              <CardTitle>Probium Configuration</CardTitle>
              <CardDescription>Configure detection engines and scanning parameters</CardDescription>
            </div>
          </div>
        </CardHeader>
      </Card>

      {/* Detection Engines */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Shield className="w-5 h-5" />
            Detection Engines
          </CardTitle>
          <CardDescription>Select which file type detection engines to use during scanning</CardDescription>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {[
              { id: "pdf", name: "PDF Engine", description: "Detects PDF documents and metadata" },
              { id: "zip", name: "ZIP Engine", description: "Analyzes compressed archives" },
              { id: "office", name: "Office Engine", description: "Microsoft Office documents" },
              { id: "image", name: "Image Engine", description: "Image files and formats" },
              { id: "binary", name: "Binary Engine", description: "Binary file analysis" },
              { id: "text", name: "Text Engine", description: "Plain text and encoding detection" },
            ].map((engine) => (
              <div key={engine.id} className="flex items-center space-x-3 p-3 border rounded-lg">
                <Switch checked={config.engines.includes(engine.id)} onCheckedChange={() => toggleEngine(engine.id)} />
                <div className="flex-1">
                  <Label className="font-medium">{engine.name}</Label>
                  <p className="text-sm text-gray-600">{engine.description}</p>
                </div>
              </div>
            ))}
          </div>

          <div className="flex items-center gap-2 pt-2">
            <span className="text-sm font-medium">Active engines:</span>
            {config.engines.map((engine: string) => (
              <Badge key={engine} variant="secondary">
                {engine}
              </Badge>
            ))}
          </div>
        </CardContent>
      </Card>

      {/* Performance Settings */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Cpu className="w-5 h-5" />
            Performance Settings
          </CardTitle>
          <CardDescription>Configure parallel processing and performance parameters</CardDescription>
        </CardHeader>
        <CardContent className="space-y-6">
          <div className="space-y-3">
            <div className="flex items-center justify-between">
              <Label>Thread Pool Size</Label>
              <Badge variant="outline">{config.threadPool} threads</Badge>
            </div>
            <Slider
              value={[config.threadPool]}
              onValueChange={(value) => updateConfig("threadPool", value[0])}
              max={16}
              min={1}
              step={1}
              className="w-full"
            />
            <p className="text-sm text-gray-600">
              Number of parallel threads for batch processing. Higher values may improve performance but use more system
              resources.
            </p>
          </div>

          <div className="space-y-3">
            <div className="flex items-center justify-between">
              <Label>Confidence Threshold</Label>
              <Badge variant="outline">{(config.confidenceThreshold * 100).toFixed(0)}%</Badge>
            </div>
            <Slider
              value={[config.confidenceThreshold]}
              onValueChange={(value) => updateConfig("confidenceThreshold", value[0])}
              max={1}
              min={0.1}
              step={0.05}
              className="w-full"
            />
            <p className="text-sm text-gray-600">
              Minimum confidence level required for file type detection. Lower values may detect more files but with
              less certainty.
            </p>
          </div>
        </CardContent>
      </Card>

      {/* Advanced Options */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Zap className="w-5 h-5" />
            Advanced Options
          </CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="flex items-center justify-between">
            <div>
              <Label>Deep Analysis</Label>
              <p className="text-sm text-gray-600">Perform thorough content analysis</p>
            </div>
            <Switch />
          </div>

          <div className="flex items-center justify-between">
            <div>
              <Label>Cache Results</Label>
              <p className="text-sm text-gray-600">Cache scan results for faster re-scanning</p>
            </div>
            <Switch defaultChecked />
          </div>

          <div className="flex items-center justify-between">
            <div>
              <Label>Verbose Logging</Label>
              <p className="text-sm text-gray-600">Enable detailed logging output</p>
            </div>
            <Switch />
          </div>
        </CardContent>
      </Card>

      {/* Reset Configuration */}
      <Card>
        <CardContent className="p-6">
          <div className="flex items-center justify-between">
            <div>
              <h3 className="font-medium">Reset Configuration</h3>
              <p className="text-sm text-gray-600">Restore all settings to default values</p>
            </div>
            <Button onClick={resetToDefaults} variant="outline">
              Reset to Defaults
            </Button>
          </div>
        </CardContent>
      </Card>
    </div>
  )
}
