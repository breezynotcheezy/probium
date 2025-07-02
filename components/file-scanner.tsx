"use client"

import { useState, useCallback } from "react"
import { useDropzone } from "react-dropzone"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Progress } from "@/components/ui/progress"
import { Badge } from "@/components/ui/badge"
import { Alert, AlertDescription } from "@/components/ui/alert"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Switch } from "@/components/ui/switch"
import { Upload, FileText, AlertCircle, CheckCircle, Shield, Microscope, Cpu } from "lucide-react"
import { api, type ScanResult } from "@/lib/api"

interface FileScannerProps {
  onScanComplete: (results: ScanResult) => void
  config: any
  setIsScanning: (scanning: boolean) => void
}

export function FileScanner({ onScanComplete, config, setIsScanning }: FileScannerProps) {
  const [uploadedFile, setUploadedFile] = useState<File | null>(null)
  const [scanProgress, setScanProgress] = useState(0)
  const [scanStatus, setScanStatus] = useState<"idle" | "scanning" | "complete" | "error">("idle")
  const [error, setError] = useState<string | null>(null)
  const [scanOptions, setScanOptions] = useState({
    deepScan: true,
    generateHashes: true,
    extractMetadata: true,
    validateSignatures: true,
    checkMalware: true,
    analyzeStructure: true,
    customEngines: [],
  })
  const [scanDetails, setScanDetails] = useState<ScanResult | null>(null)
  const [currentStage, setCurrentStage] = useState<string>("")

  const onDrop = useCallback((acceptedFiles: File[]) => {
    if (acceptedFiles.length > 0) {
      setUploadedFile(acceptedFiles[0])
      setScanStatus("idle")
      setError(null)
      setScanDetails(null)
    }
  }, [])

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    maxFiles: 1,
    maxSize: config.maxFileSize,
  })

  const performRealScan = async () => {
    if (!uploadedFile) return

    setScanStatus("scanning")
    setIsScanning(true)
    setScanProgress(0)
    setError(null)
    setCurrentStage("Initializing...")

    try {
      // Prepare scan options
      const scanOpts = {
        engines: config.engines,
        deep_analysis: scanOptions.deepScan,
        generate_hashes: scanOptions.generateHashes,
        extract_metadata: scanOptions.extractMetadata,
        validate_signatures: scanOptions.validateSignatures,
      }

      // Start the scan
      setCurrentStage("Uploading file...")
      setScanProgress(10)

      const result = await api.scanFile(uploadedFile, scanOpts)

      // Simulate progress updates during scan
      const progressSteps = [
        { progress: 30, stage: "Running detection engines..." },
        { progress: 50, stage: "Analyzing file structure..." },
        { progress: 70, stage: "Generating hashes..." },
        { progress: 85, stage: "Extracting metadata..." },
        { progress: 95, stage: "Security assessment..." },
        { progress: 100, stage: "Complete!" },
      ]

      for (const step of progressSteps) {
        setCurrentStage(step.stage)
        setScanProgress(step.progress)
        await new Promise((resolve) => setTimeout(resolve, 200))
      }

      onScanComplete(result)
      setScanStatus("complete")
      setScanDetails(result)
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : "Scan failed"
      setError(errorMessage)
      setScanStatus("error")
      console.error("Scan error:", err)
    } finally {
      setIsScanning(false)
    }
  }

  return (
    <div className="space-y-6">
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* File Upload Section */}
        <Card className="bg-purple-50 border-purple-300">
          <CardHeader>
            <CardTitle className="text-purple-900 flex items-center gap-2">
              <Upload className="w-5 h-5" />
              File Upload & Analysis
            </CardTitle>
            <CardDescription className="text-purple-700">
              Upload files for comprehensive analysis using Probium engines
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            {/* Drop Zone */}
            <div
              {...getRootProps()}
              className={`border-2 border-dashed rounded-lg p-8 text-center cursor-pointer transition-all ${
                isDragActive
                  ? "border-purple-200 bg-purple-50"
                  : "border-purple-300 hover:border-purple-300 bg-purple-50"
              }`}
            >
              <input {...getInputProps()} />
              <Upload className="w-12 h-12 text-purple-600 mx-auto mb-4" />
              {isDragActive ? (
                <p className="text-purple-700">Drop the file here...</p>
              ) : (
                <div>
                  <p className="text-purple-600 mb-2">Drag & drop a file here, or click to select</p>
                  <p className="text-sm text-purple-600">
                    Maximum file size: {(config.maxFileSize / 1024 / 1024).toFixed(0)}MB
                  </p>
                </div>
              )}
            </div>

            {/* File Info */}
            {uploadedFile && (
              <div className="flex items-center gap-3 p-4 bg-purple-50 rounded-lg border border-purple-300">
                <FileText className="w-8 h-8 text-purple-600" />
                <div className="flex-1">
                  <p className="font-medium text-purple-900">{uploadedFile.name}</p>
                  <p className="text-sm text-purple-700">
                    {(uploadedFile.size / 1024 / 1024).toFixed(2)} MB • {uploadedFile.type || "Unknown type"}
                  </p>
                </div>
                <Button
                  onClick={performRealScan}
                  disabled={scanStatus === "scanning"}
                  className="bg-purple-400 hover:bg-purple-500"
                >
                  {scanStatus === "scanning" ? "Scanning..." : "Analyze File"}
                </Button>
              </div>
            )}

            {/* Scan Progress */}
            {scanStatus === "scanning" && (
              <div className="space-y-3">
                <div className="flex justify-between text-sm">
                  <span className="text-purple-700">{currentStage}</span>
                  <span className="text-purple-700">{Math.round(scanProgress)}%</span>
                </div>
                <Progress value={scanProgress} className="bg-purple-200" />
                <div className="flex items-center gap-2 text-xs text-purple-600">
                  <Cpu className="w-3 h-3" />
                  <span>Using {config.engines.length} detection engines</span>
                </div>
              </div>
            )}

            {/* Status Messages */}
            {scanStatus === "complete" && (
              <Alert className="border-green-600 bg-green-900/30">
                <CheckCircle className="h-4 w-4 text-green-400" />
                <AlertDescription className="text-green-300">
                  File analyzed successfully! Detailed results available below.
                </AlertDescription>
              </Alert>
            )}

            {error && (
              <Alert className="border-red-600 bg-red-900/30">
                <AlertCircle className="h-4 w-4 text-red-400" />
                <AlertDescription className="text-red-300">{error}</AlertDescription>
              </Alert>
            )}
          </CardContent>
        </Card>

        {/* Scan Options */}
        <Card className="bg-purple-50 border-purple-300">
          <CardHeader>
            <CardTitle className="text-purple-900 flex items-center gap-2">
              <Shield className="w-5 h-5" />
              Scan Configuration
            </CardTitle>
            <CardDescription className="text-purple-700">
              Configure analysis options and detection engines
            </CardDescription>
          </CardHeader>
          <CardContent>
            <Tabs defaultValue="options" className="space-y-4">
              <TabsList className="grid w-full grid-cols-2 bg-purple-100">
                <TabsTrigger value="options">Scan Options</TabsTrigger>
                <TabsTrigger value="engines">Engine Config</TabsTrigger>
              </TabsList>

              <TabsContent value="options" className="space-y-4">
                <div className="space-y-4">
                  <div className="flex items-center justify-between">
                    <div>
                      <Label className="text-purple-900">Deep Analysis</Label>
                      <p className="text-xs text-purple-600">Comprehensive file structure analysis</p>
                    </div>
                    <Switch
                      checked={scanOptions.deepScan}
                      onCheckedChange={(checked) => setScanOptions((prev) => ({ ...prev, deepScan: checked }))}
                    />
                  </div>

                  <div className="flex items-center justify-between">
                    <div>
                      <Label className="text-purple-900">Generate Hashes</Label>
                      <p className="text-xs text-purple-600">MD5, SHA1, SHA256, CRC32</p>
                    </div>
                    <Switch
                      checked={scanOptions.generateHashes}
                      onCheckedChange={(checked) => setScanOptions((prev) => ({ ...prev, generateHashes: checked }))}
                    />
                  </div>

                  <div className="flex items-center justify-between">
                    <div>
                      <Label className="text-purple-900">Extract Metadata</Label>
                      <p className="text-xs text-purple-600">Author, creation date, properties</p>
                    </div>
                    <Switch
                      checked={scanOptions.extractMetadata}
                      onCheckedChange={(checked) => setScanOptions((prev) => ({ ...prev, extractMetadata: checked }))}
                    />
                  </div>

                  <div className="flex items-center justify-between">
                    <div>
                      <Label className="text-purple-900">Validate Signatures</Label>
                      <p className="text-xs text-purple-600">Digital signature verification</p>
                    </div>
                    <Switch
                      checked={scanOptions.validateSignatures}
                      onCheckedChange={(checked) =>
                        setScanOptions((prev) => ({ ...prev, validateSignatures: checked }))
                      }
                    />
                  </div>
                </div>
              </TabsContent>

              <TabsContent value="engines" className="space-y-4">
                <div className="space-y-3">
                  <Label className="text-purple-900">Active Engines</Label>
                  <div className="grid grid-cols-2 gap-2">
                    {config.engines.map((engine: string) => (
                      <Badge key={engine} variant="secondary" className="bg-purple-500 text-purple-500">
                        {engine}
                      </Badge>
                    ))}
                  </div>
                </div>

                <div className="space-y-2">
                  <Label className="text-purple-900">Thread Pool Size</Label>
                  <Input
                    type="number"
                    value={config.threadPool}
                    className="bg-purple-100 border-purple-300 text-purple-900"
                    readOnly
                  />
                </div>

                <div className="space-y-2">
                  <Label className="text-purple-900">Timeout (ms)</Label>
                  <Input
                    type="number"
                    value={config.timeout}
                    className="bg-purple-100 border-purple-300 text-purple-900"
                    readOnly
                  />
                </div>
              </TabsContent>
            </Tabs>
          </CardContent>
        </Card>
      </div>

      {/* Detailed Results */}
      {scanDetails && scanStatus === "complete" && (
        <Card className="bg-purple-50 border-purple-300">
          <CardHeader>
            <CardTitle className="text-purple-900 flex items-center gap-2">
              <Microscope className="w-5 h-5" />
              Detailed Analysis Results
            </CardTitle>
          </CardHeader>
          <CardContent>
            <Tabs defaultValue="overview" className="space-y-4">
              <TabsList className="grid w-full grid-cols-5 bg-purple-100">
                <TabsTrigger value="overview">Overview</TabsTrigger>
                <TabsTrigger value="hashes">Hashes</TabsTrigger>
                <TabsTrigger value="metadata">Metadata</TabsTrigger>
                <TabsTrigger value="structure">Structure</TabsTrigger>
                <TabsTrigger value="security">Security</TabsTrigger>
              </TabsList>

              <TabsContent value="overview" className="space-y-4">
                <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                  <div className="p-3 bg-purple-50 rounded-lg">
                    <p className="text-xs text-purple-600">File Type</p>
                    <p className="text-purple-900 font-medium">{scanDetails.detected_type}</p>
                  </div>
                  <div className="p-3 bg-purple-50 rounded-lg">
                    <p className="text-xs text-purple-600">Confidence</p>
                    <p className="text-purple-900 font-medium">{(scanDetails.confidence * 100).toFixed(1)}%</p>
                  </div>
                  <div className="p-3 bg-purple-50 rounded-lg">
                    <p className="text-xs text-purple-600">Scan Time</p>
                    <p className="text-purple-900 font-medium">{scanDetails.scan_time}</p>
                  </div>
                  <div className="p-3 bg-purple-50 rounded-lg">
                    <p className="text-xs text-purple-600">Probium Version</p>
                    <p className="text-purple-900 font-medium">{scanDetails.probium_version}</p>
                  </div>
                </div>

                <div className="space-y-2">
                  <p className="text-sm font-medium text-purple-700">Engines Used:</p>
                  <div className="flex flex-wrap gap-2">
                    {scanDetails.engines_used.map((engine: string) => (
                      <Badge key={engine} variant="secondary" className="bg-purple-500 text-purple-500">
                        {engine}
                      </Badge>
                    ))}
                  </div>
                </div>
              </TabsContent>

              <TabsContent value="hashes">
                <div className="space-y-3">
                  {scanDetails.hashes &&
                    Object.entries(scanDetails.hashes).map(([type, hash]) => (
                      <div key={type} className="flex items-center justify-between p-3 bg-purple-50 rounded-lg">
                        <span className="text-purple-700 uppercase font-medium">{type}</span>
                        <code className="text-purple-900 text-sm font-mono">{hash}</code>
                      </div>
                    ))}
                </div>
              </TabsContent>

              <TabsContent value="metadata">
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  {scanDetails.metadata &&
                    Object.entries(scanDetails.metadata).map(([key, value]) => (
                      <div key={key} className="p-3 bg-purple-50 rounded-lg">
                        <p className="text-xs text-purple-600 capitalize">{key.replace(/([A-Z])/g, " $1")}</p>
                        <p className="text-purple-900">{Array.isArray(value) ? value.join(", ") : String(value)}</p>
                      </div>
                    ))}
                </div>
              </TabsContent>

              <TabsContent value="structure">
                <div className="grid grid-cols-2 md:grid-cols-3 gap-4">
                  {scanDetails.structure &&
                    Object.entries(scanDetails.structure).map(([key, value]) => (
                      <div key={key} className="p-3 bg-purple-50 rounded-lg">
                        <p className="text-xs text-purple-600 capitalize">{key}</p>
                        <p className="text-purple-900 font-medium">{String(value)}</p>
                      </div>
                    ))}
                </div>
              </TabsContent>

              <TabsContent value="security">
                <div className="space-y-4">
                  {scanDetails.security && (
                    <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                      <div className="p-4 bg-purple-50 rounded-lg">
                        <p className="text-xs text-purple-600">Malware Score</p>
                        <p className="text-2xl font-bold text-purple-900">{scanDetails.security.malware_score}</p>
                      </div>
                      <div className="p-4 bg-purple-50 rounded-lg">
                        <p className="text-xs text-purple-600">Threat Level</p>
                        <Badge
                          className={`mt-1 ${
                            scanDetails.security.threat_level === "low"
                              ? "bg-green-600"
                              : scanDetails.security.threat_level === "medium"
                                ? "bg-yellow-600"
                                : "bg-red-600"
                          }`}
                        >
                          {scanDetails.security.threat_level}
                        </Badge>
                      </div>
                      <div className="p-4 bg-purple-50 rounded-lg">
                        <p className="text-xs text-purple-600">Embedded Files</p>
                        <p className="text-2xl font-bold text-purple-900">{scanDetails.security.embedded.files}</p>
                      </div>
                    </div>
                  )}
                </div>
              </TabsContent>
            </Tabs>
          </CardContent>
        </Card>
      )}
    </div>
  )
}
