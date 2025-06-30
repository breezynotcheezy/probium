"use client"

import { useState, useCallback } from "react"
import { useDropzone } from "react-dropzone"
import { Button } from "@/components/ui/button"
import { Progress } from "@/components/ui/progress"
import { Alert, AlertDescription } from "@/components/ui/alert"
import { Upload, FileText, AlertCircle, CheckCircle } from "lucide-react"

interface FileUploadProps {
  onScanComplete: (results: any) => void
  config: any
  setIsScanning: (scanning: boolean) => void
}

export function FileUpload({ onScanComplete, config, setIsScanning }: FileUploadProps) {
  const [uploadedFile, setUploadedFile] = useState<File | null>(null)
  const [scanProgress, setScanProgress] = useState(0)
  const [scanStatus, setScanStatus] = useState<"idle" | "scanning" | "complete" | "error">("idle")
  const [error, setError] = useState<string | null>(null)

  const onDrop = useCallback((acceptedFiles: File[]) => {
    if (acceptedFiles.length > 0) {
      setUploadedFile(acceptedFiles[0])
      setScanStatus("idle")
      setError(null)
    }
  }, [])

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    maxFiles: 1,
    maxSize: 100 * 1024 * 1024, // 100MB
  })

  const simulateScan = async () => {
    if (!uploadedFile) return

    setScanStatus("scanning")
    setIsScanning(true)
    setScanProgress(0)
    setError(null)

    try {
      // Simulate API call to Probium backend
      const formData = new FormData()
      formData.append("file", uploadedFile)
      formData.append("config", JSON.stringify(config))

      // Simulate progress
      const progressInterval = setInterval(() => {
        setScanProgress((prev) => {
          if (prev >= 90) {
            clearInterval(progressInterval)
            return 90
          }
          return prev + Math.random() * 20
        })
      }, 200)

      // Simulate API response after 2 seconds
      await new Promise((resolve) => setTimeout(resolve, 2000))
      clearInterval(progressInterval)
      setScanProgress(100)

      // Mock Probium response
      const mockResult = {
        id: Date.now(),
        filename: uploadedFile.name,
        size: uploadedFile.size,
        detectedType: "PDF Document",
        confidence: 0.95,
        engines: ["pdf", "binary"],
        metadata: {
          pages: 12,
          encrypted: false,
          version: "1.4",
        },
        scanTime: "0.234s",
        timestamp: new Date().toISOString(),
      }

      onScanComplete(mockResult)
      setScanStatus("complete")
    } catch (err) {
      setError("Failed to scan file. Please try again.")
      setScanStatus("error")
    } finally {
      setIsScanning(false)
    }
  }

  return (
    <div className="space-y-6">
      {/* File Drop Zone */}
      <div
        {...getRootProps()}
        className={`border-2 border-dashed rounded-lg p-8 text-center cursor-pointer transition-colors ${
          isDragActive ? "border-blue-500 bg-blue-50" : "border-gray-300 hover:border-gray-400"
        }`}
      >
        <input {...getInputProps()} />
        <Upload className="w-12 h-12 text-gray-400 mx-auto mb-4" />
        {isDragActive ? (
          <p className="text-blue-600">Drop the file here...</p>
        ) : (
          <div>
            <p className="text-gray-600 mb-2">Drag & drop a file here, or click to select</p>
            <p className="text-sm text-gray-500">Maximum file size: 100MB</p>
          </div>
        )}
      </div>

      {/* Uploaded File Info */}
      {uploadedFile && (
        <div className="flex items-center gap-3 p-4 bg-gray-50 rounded-lg">
          <FileText className="w-8 h-8 text-blue-500" />
          <div className="flex-1">
            <p className="font-medium">{uploadedFile.name}</p>
            <p className="text-sm text-gray-600">{(uploadedFile.size / 1024 / 1024).toFixed(2)} MB</p>
          </div>
          <Button onClick={simulateScan} disabled={scanStatus === "scanning"} className="ml-auto">
            {scanStatus === "scanning" ? "Scanning..." : "Scan File"}
          </Button>
        </div>
      )}

      {/* Scan Progress */}
      {scanStatus === "scanning" && (
        <div className="space-y-2">
          <div className="flex justify-between text-sm">
            <span>Scanning with Probium engines...</span>
            <span>{Math.round(scanProgress)}%</span>
          </div>
          <Progress value={scanProgress} className="w-full" />
        </div>
      )}

      {/* Status Messages */}
      {scanStatus === "complete" && (
        <Alert className="border-green-200 bg-green-50">
          <CheckCircle className="h-4 w-4 text-green-600" />
          <AlertDescription className="text-green-800">
            File scanned successfully! Check the Results tab to view details.
          </AlertDescription>
        </Alert>
      )}

      {error && (
        <Alert className="border-red-200 bg-red-50">
          <AlertCircle className="h-4 w-4 text-red-600" />
          <AlertDescription className="text-red-800">{error}</AlertDescription>
        </Alert>
      )}
    </div>
  )
}
