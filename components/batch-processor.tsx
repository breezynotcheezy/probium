"use client"

import { useState, useCallback } from "react"
import { useDropzone } from "react-dropzone"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Progress } from "@/components/ui/progress"
import { Badge } from "@/components/ui/badge"
import { Label } from "@/components/ui/label"
import { Switch } from "@/components/ui/switch"
import { Files, Play, Pause, Database, Cpu, Clock } from "lucide-react"

interface BatchProcessorProps {
  onBatchComplete: (results: any[]) => void
  config: any
  setIsScanning: (scanning: boolean) => void
}

export function BatchProcessor({ onBatchComplete, config, setIsScanning }: BatchProcessorProps) {
  const [files, setFiles] = useState<File[]>([])
  const [batchStatus, setBatchStatus] = useState<"idle" | "running" | "paused" | "complete">("idle")
  const [processedCount, setProcessedCount] = useState(0)
  const [currentFile, setCurrentFile] = useState<string>("")
  const [batchOptions, setBatchOptions] = useState({
    parallelProcessing: true,
    skipDuplicates: true,
    generateReport: true,
    autoExport: false,
  })

  const onDrop = useCallback((acceptedFiles: File[]) => {
    setFiles((prev) => [...prev, ...acceptedFiles])
  }, [])

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    multiple: true,
    maxSize: config.maxFileSize,
  })

  const startBatchProcessing = async () => {
    if (files.length === 0) return

    setBatchStatus("running")
    setIsScanning(true)
    setProcessedCount(0)

    const results = []
    const batchSize = batchOptions.parallelProcessing ? config.threadPool : 1

    for (let i = 0; i < files.length; i += batchSize) {
      const batch = files.slice(i, i + batchSize)

      for (const file of batch) {
        setCurrentFile(file.name)
        await new Promise((resolve) => setTimeout(resolve, 800))

        const mockResult = {
          id: Date.now() + Math.random(),
          filename: file.name,
          size: file.size,
          detectedType: getRandomFileType(),
          confidence: 0.8 + Math.random() * 0.2,
          engines: config.engines,
          scanTime: `${(Math.random() * 0.5).toFixed(3)}s`,
          timestamp: new Date().toISOString(),
          batchId: Date.now(),
        }

        results.push(mockResult)
        setProcessedCount(i + batch.indexOf(file) + 1)
      }
    }

    onBatchComplete(results)
    setBatchStatus("complete")
    setIsScanning(false)
    setCurrentFile("")
  }

  const getRandomFileType = () => {
    const types = ["PDF Document", "ZIP Archive", "Office Document", "Image File", "Text File", "Binary File"]
    return types[Math.floor(Math.random() * types.length)]
  }

  const clearFiles = () => {
    setFiles([])
    setProcessedCount(0)
    setBatchStatus("idle")
  }

  return (
    <div className="space-y-6">
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Batch Upload */}
        <Card className="bg-purple-50 border-purple-300">
          <CardHeader>
            <CardTitle className="text-white flex items-center gap-2">
              <Files className="w-5 h-5" />
              Batch File Upload
            </CardTitle>
            <CardDescription className="text-purple-700">Upload multiple files for parallel processing</CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            <div
              {...getRootProps()}
              className={`border-2 border-dashed rounded-lg p-8 text-center cursor-pointer transition-all ${
                isDragActive
                  ? "border-purple-200 bg-purple-50"
                  : "border-purple-300 hover:border-purple-300 bg-purple-50"
              }`}
            >
              <input {...getInputProps()} />
              <Files className="w-12 h-12 text-purple-600 mx-auto mb-4" />
              {isDragActive ? (
                <p className="text-purple-700">Drop the files here...</p>
              ) : (
                <div>
                  <p className="text-purple-600 mb-2">Drag & drop multiple files here, or click to select</p>
                  <p className="text-sm text-purple-600">Process up to 1000 files simultaneously</p>
                </div>
              )}
            </div>

            {files.length > 0 && (
              <div className="space-y-3">
                <div className="flex items-center justify-between">
                  <span className="text-purple-700">{files.length} files queued</span>
                  <Button
                    onClick={clearFiles}
                    variant="outline"
                    size="sm"
                    className="border-purple-300 text-purple-700 bg-transparent"
                  >
                    Clear All
                  </Button>
                </div>
                <div className="max-h-40 overflow-y-auto space-y-1">
                  {files.slice(0, 10).map((file, index) => (
                    <div key={index} className="flex items-center justify-between p-2 bg-purple-50 rounded text-sm">
                      <span className="text-purple-600 truncate">{file.name}</span>
                      <span className="text-purple-600">{(file.size / 1024 / 1024).toFixed(1)}MB</span>
                    </div>
                  ))}
                  {files.length > 10 && (
                    <p className="text-center text-purple-600 text-sm">...and {files.length - 10} more files</p>
                  )}
                </div>
              </div>
            )}
          </CardContent>
        </Card>

        {/* Batch Options */}
        <Card className="bg-purple-50 border-purple-300">
          <CardHeader>
            <CardTitle className="text-white flex items-center gap-2">
              <Database className="w-5 h-5" />
              Batch Configuration
            </CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="space-y-4">
              <div className="flex items-center justify-between">
                <div>
                  <Label className="text-white">Parallel Processing</Label>
                  <p className="text-xs text-purple-600">Use multiple threads for faster processing</p>
                </div>
                <Switch
                  checked={batchOptions.parallelProcessing}
                  onCheckedChange={(checked) => setBatchOptions((prev) => ({ ...prev, parallelProcessing: checked }))}
                />
              </div>

              <div className="flex items-center justify-between">
                <div>
                  <Label className="text-white">Skip Duplicates</Label>
                  <p className="text-xs text-purple-600">Skip files with identical hashes</p>
                </div>
                <Switch
                  checked={batchOptions.skipDuplicates}
                  onCheckedChange={(checked) => setBatchOptions((prev) => ({ ...prev, skipDuplicates: checked }))}
                />
              </div>

              <div className="flex items-center justify-between">
                <div>
                  <Label className="text-white">Generate Report</Label>
                  <p className="text-xs text-purple-600">Create detailed batch processing report</p>
                </div>
                <Switch
                  checked={batchOptions.generateReport}
                  onCheckedChange={(checked) => setBatchOptions((prev) => ({ ...prev, generateReport: checked }))}
                />
              </div>

              <div className="flex items-center justify-between">
                <div>
                  <Label className="text-white">Auto Export</Label>
                  <p className="text-xs text-purple-600">Automatically export results when complete</p>
                </div>
                <Switch
                  checked={batchOptions.autoExport}
                  onCheckedChange={(checked) => setBatchOptions((prev) => ({ ...prev, autoExport: checked }))}
                />
              </div>
            </div>

            <div className="pt-4 border-t border-purple-300">
              <div className="flex gap-2">
                <Button
                  onClick={startBatchProcessing}
                  disabled={batchStatus === "running" || files.length === 0}
                  className="flex-1 bg-purple-400 hover:bg-purple-500"
                >
                  <Play className="w-4 h-4 mr-2" />
                  Start Batch
                </Button>
                {batchStatus === "running" && (
                  <Button
                    onClick={() => setBatchStatus("paused")}
                    variant="outline"
                    className="border-purple-300 text-purple-700"
                  >
                    <Pause className="w-4 h-4" />
                  </Button>
                )}
              </div>
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Batch Progress */}
      {batchStatus === "running" && (
        <Card className="bg-purple-50 border-purple-300">
          <CardContent className="p-6">
            <div className="space-y-4">
              <div className="flex justify-between items-center">
                <h3 className="font-semibold text-white">Batch Processing Progress</h3>
                <div className="flex items-center gap-4">
                  <Badge className="bg-purple-500">
                    <Cpu className="w-3 h-3 mr-1" />
                    {config.threadPool} threads
                  </Badge>
                  <Badge className="bg-purple-500">
                    <Clock className="w-3 h-3 mr-1" />
                    {Math.round((Date.now() - (Date.now() - processedCount * 800)) / 1000)}s
                  </Badge>
                </div>
              </div>

              <div className="space-y-2">
                <div className="flex justify-between text-sm">
                  <span className="text-purple-700">
                    Progress: {processedCount} / {files.length}
                  </span>
                  <span className="text-purple-700">{Math.round((processedCount / files.length) * 100)}%</span>
                </div>
                <Progress value={(processedCount / files.length) * 100} className="bg-purple-200" />
              </div>

              {currentFile && (
                <p className="text-sm text-purple-700">
                  Currently processing: <span className="font-medium text-white">{currentFile}</span>
                </p>
              )}
            </div>
          </CardContent>
        </Card>
      )}

      {/* Batch Complete */}
      {batchStatus === "complete" && (
        <Card className="bg-green-900/30 border-green-700">
          <CardContent className="p-6">
            <h3 className="font-semibold text-green-300 mb-2">Batch Processing Complete!</h3>
            <p className="text-green-200">
              Successfully processed {files.length} files. Results are available in the Results tab.
            </p>
          </CardContent>
        </Card>
      )}
    </div>
  )
}
