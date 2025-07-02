"use client"

import { useState, useMemo } from "react"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import { Input } from "@/components/ui/input"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "@/components/ui/dialog"
import {
  Search,
  Download,
  Eye,
  Trash2,
  FileText,
  Filter,
  BarChart3,
  Hash,
  Shield,
  Clock,
  Database,
  AlertTriangle,
  CheckCircle,
  TrendingUp,
  Activity,
  Cpu,
} from "lucide-react"

interface ScanResultsProps {
  results: any[]
  onClear: () => void
}

export function ScanResults({ results, onClear }: ScanResultsProps) {
  const [searchTerm, setSearchTerm] = useState("")
  const [selectedResult, setSelectedResult] = useState<any>(null)
  const [filterType, setFilterType] = useState("all")
  const [sortBy, setSortBy] = useState("timestamp")
  const [sortOrder, setSortOrder] = useState("desc")

  const filteredAndSortedResults = useMemo(() => {
    const filtered = results.filter((result) => {
      const matchesSearch =
        result.filename.toLowerCase().includes(searchTerm.toLowerCase()) ||
        result.detectedType.toLowerCase().includes(searchTerm.toLowerCase())

      const matchesFilter =
        filterType === "all" ||
        (filterType === "high-confidence" && result.confidence >= 0.9) ||
        (filterType === "low-confidence" && result.confidence < 0.7) ||
        (filterType === "threats" && result.security?.threatLevel !== "low")

      return matchesSearch && matchesFilter
    })

    return filtered.sort((a, b) => {
      let aVal = a[sortBy]
      let bVal = b[sortBy]

      if (sortBy === "timestamp") {
        aVal = new Date(aVal).getTime()
        bVal = new Date(bVal).getTime()
      }

      if (sortOrder === "asc") {
        return aVal > bVal ? 1 : -1
      } else {
        return aVal < bVal ? 1 : -1
      }
    })
  }, [results, searchTerm, filterType, sortBy, sortOrder])

  const stats = useMemo(() => {
    const total = results.length
    const highConfidence = results.filter((r) => r.confidence >= 0.9).length
    const lowConfidence = results.filter((r) => r.confidence < 0.7).length
    const threats = results.filter((r) => r.security?.threatLevel !== "low").length
    const avgConfidence = total > 0 ? results.reduce((sum, r) => sum + r.confidence, 0) / total : 0
    const avgScanTime =
      total > 0 ? results.reduce((sum, r) => sum + Number.parseFloat(r.performance?.scanTime || "0"), 0) / total : 0

    const fileTypes = results.reduce(
      (acc, result) => {
        acc[result.detectedType] = (acc[result.detectedType] || 0) + 1
        return acc
      },
      {} as Record<string, number>,
    )

    return {
      total,
      highConfidence,
      lowConfidence,
      threats,
      avgConfidence,
      avgScanTime,
      fileTypes,
    }
  }, [results])

  const exportResults = (format: string) => {
    let dataStr = ""
    let filename = `probium-results-${new Date().toISOString().split("T")[0]}`

    if (format === "json") {
      dataStr = JSON.stringify(filteredAndSortedResults, null, 2)
      filename += ".json"
    } else if (format === "csv") {
      const headers = ["filename", "detectedType", "confidence", "size", "scanTime", "threatLevel"]
      const csvData = [
        headers.join(","),
        ...filteredAndSortedResults.map((result) =>
          headers
            .map((header) => {
              const value = result[header] || result.performance?.[header] || result.security?.[header] || ""
              return `"${value}"`
            })
            .join(","),
        ),
      ].join("\n")
      dataStr = csvData
      filename += ".csv"
    }

    const dataUri = `data:application/${format};charset=utf-8,` + encodeURIComponent(dataStr)
    const linkElement = document.createElement("a")
    linkElement.setAttribute("href", dataUri)
    linkElement.setAttribute("download", filename)
    linkElement.click()
  }

  const getConfidenceColor = (confidence: number) => {
    if (confidence >= 0.9) return "bg-green-900/50 text-green-300 border-green-600"
    if (confidence >= 0.7) return "bg-yellow-900/50 text-yellow-300 border-yellow-600"
    return "bg-red-900/50 text-red-300 border-red-600"
  }

  const getThreatColor = (threatLevel: string) => {
    switch (threatLevel) {
      case "low":
        return "bg-green-900/50 text-green-300 border-green-600"
      case "medium":
        return "bg-yellow-900/50 text-yellow-300 border-yellow-600"
      case "high":
        return "bg-red-900/50 text-red-300 border-red-600"
      default:
        return "bg-gray-900/50 text-gray-300 border-gray-600"
    }
  }

  return (
    <div className="space-y-6">
      {/* Results Statistics */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        <Card className="bg-gray-800 border-gray-700">
          <CardContent className="p-4">
            <div className="flex items-center gap-3">
              <Database className="w-8 h-8 text-purple-300" />
              <div>
                <p className="text-sm text-gray-200">Total Scans</p>
                <p className="text-2xl font-bold text-white">{stats.total}</p>
              </div>
            </div>
          </CardContent>
        </Card>

        <Card className="bg-gray-800 border-gray-700">
          <CardContent className="p-4">
            <div className="flex items-center gap-3">
              <CheckCircle className="w-8 h-8 text-green-400" />
              <div>
                <p className="text-sm text-gray-200">Avg Confidence</p>
                <p className="text-2xl font-bold text-white">{(stats.avgConfidence * 100).toFixed(1)}%</p>
              </div>
            </div>
          </CardContent>
        </Card>

        <Card className="bg-gray-800 border-gray-700">
          <CardContent className="p-4">
            <div className="flex items-center gap-3">
              <Clock className="w-8 h-8 text-blue-400" />
              <div>
                <p className="text-sm text-gray-200">Avg Scan Time</p>
                <p className="text-2xl font-bold text-white">{stats.avgScanTime.toFixed(2)}s</p>
              </div>
            </div>
          </CardContent>
        </Card>

        <Card className="bg-gray-800 border-gray-700">
          <CardContent className="p-4">
            <div className="flex items-center gap-3">
              <AlertTriangle className="w-8 h-8 text-red-400" />
              <div>
                <p className="text-sm text-gray-200">Threats</p>
                <p className="text-2xl font-bold text-white">{stats.threats}</p>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Results Management */}
      <Card className="bg-gray-800 border-gray-700">
        <CardHeader>
          <div className="flex items-center justify-between">
            <div>
              <CardTitle className="text-white flex items-center gap-2">
                <BarChart3 className="w-5 h-5" />
                Scan Results
              </CardTitle>
              <CardDescription className="text-gray-200">
                {filteredAndSortedResults.length} of {results.length} results
              </CardDescription>
            </div>
            <div className="flex gap-2">
              <Select onValueChange={(value) => exportResults(value)}>
                <SelectTrigger className="w-32 bg-gray-900 border-gray-700 text-white">
                  <Download className="w-4 h-4 mr-2" />
                  <SelectValue placeholder="Export" />
                </SelectTrigger>
                <SelectContent className="bg-gray-900 border-gray-700">
                  <SelectItem value="json" className="text-white">
                    JSON
                  </SelectItem>
                  <SelectItem value="csv" className="text-white">
                    CSV
                  </SelectItem>
                </SelectContent>
              </Select>
              <Button
                onClick={onClear}
                variant="outline"
                size="sm"
                className="border-gray-700 text-gray-200 bg-transparent"
              >
                <Trash2 className="w-4 h-4 mr-2" />
                Clear All
              </Button>
            </div>
          </div>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            {/* Search and Filter Controls */}
            <div className="flex flex-col md:flex-row gap-4">
              <div className="relative flex-1">
                <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-purple-300 w-4 h-4" />
                <Input
                  placeholder="Search by filename or file type..."
                  value={searchTerm}
                  onChange={(e) => setSearchTerm(e.target.value)}
                  className="pl-10 bg-gray-900 border-gray-700 text-white placeholder-purple-400"
                />
              </div>

              <Select value={filterType} onValueChange={setFilterType}>
                <SelectTrigger className="w-48 bg-gray-900 border-gray-700 text-white">
                  <Filter className="w-4 h-4 mr-2" />
                  <SelectValue />
                </SelectTrigger>
                <SelectContent className="bg-gray-900 border-gray-700">
                  <SelectItem value="all" className="text-white">
                    All Results
                  </SelectItem>
                  <SelectItem value="high-confidence" className="text-white">
                    High Confidence
                  </SelectItem>
                  <SelectItem value="low-confidence" className="text-white">
                    Low Confidence
                  </SelectItem>
                  <SelectItem value="threats" className="text-white">
                    Potential Threats
                  </SelectItem>
                </SelectContent>
              </Select>

              <Select value={sortBy} onValueChange={setSortBy}>
                <SelectTrigger className="w-40 bg-gray-900 border-gray-700 text-white">
                  <SelectValue />
                </SelectTrigger>
                <SelectContent className="bg-gray-900 border-gray-700">
                  <SelectItem value="timestamp" className="text-white">
                    Date
                  </SelectItem>
                  <SelectItem value="filename" className="text-white">
                    Name
                  </SelectItem>
                  <SelectItem value="confidence" className="text-white">
                    Confidence
                  </SelectItem>
                  <SelectItem value="size" className="text-white">
                    Size
                  </SelectItem>
                </SelectContent>
              </Select>

              <Button
                variant="outline"
                size="sm"
                onClick={() => setSortOrder(sortOrder === "asc" ? "desc" : "asc")}
                className="border-gray-700 text-gray-200"
              >
                {sortOrder === "asc" ? "↑" : "↓"}
              </Button>
            </div>

            {/* Results Table */}
            {filteredAndSortedResults.length > 0 ? (
              <div className="rounded-lg border border-gray-700 overflow-hidden">
                <Table>
                  <TableHeader className="bg-gray-900">
                    <TableRow className="border-gray-700">
                      <TableHead className="text-gray-200">File</TableHead>
                      <TableHead className="text-gray-200">Type</TableHead>
                      <TableHead className="text-gray-200">Confidence</TableHead>
                      <TableHead className="text-gray-200">Size</TableHead>
                      <TableHead className="text-gray-200">Threat Level</TableHead>
                      <TableHead className="text-gray-200">Scan Time</TableHead>
                      <TableHead className="text-gray-200">Actions</TableHead>
                    </TableRow>
                  </TableHeader>
                  <TableBody>
                    {filteredAndSortedResults.map((result) => (
                      <TableRow key={result.id} className="border-gray-700 hover:bg-gray-800">
                        <TableCell>
                          <div className="flex items-center gap-2">
                            <FileText className="w-4 h-4 text-purple-300" />
                            <div>
                              <span className="font-medium text-white">{result.filename}</span>
                              <p className="text-xs text-purple-300">{(result.size / 1024 / 1024).toFixed(2)} MB</p>
                            </div>
                          </div>
                        </TableCell>
                        <TableCell>
                          <Badge variant="outline" className="border-gray-700 text-gray-200">
                            {result.detectedType}
                          </Badge>
                        </TableCell>
                        <TableCell>
                          <Badge className={getConfidenceColor(result.confidence)}>
                            {(result.confidence * 100).toFixed(1)}%
                          </Badge>
                        </TableCell>
                        <TableCell className="text-gray-200">{(result.size / 1024 / 1024).toFixed(2)} MB</TableCell>
                        <TableCell>
                          <Badge className={getThreatColor(result.security?.threatLevel || "low")}>
                            {result.security?.threatLevel || "low"}
                          </Badge>
                        </TableCell>
                        <TableCell className="text-gray-200">{result.performance?.scanTime || "N/A"}</TableCell>
                        <TableCell>
                          <Dialog>
                            <DialogTrigger asChild>
                              <Button
                                variant="ghost"
                                size="sm"
                                onClick={() => setSelectedResult(result)}
                                className="text-gray-200 hover:text-white hover:bg-purple-600"
                              >
                                <Eye className="w-4 h-4" />
                              </Button>
                            </DialogTrigger>
                            <DialogContent className="max-w-4xl bg-gray-900 border-gray-700 text-white">
                              <DialogHeader>
                                <DialogTitle className="text-white">Detailed Analysis: {result.filename}</DialogTitle>
                                <DialogDescription className="text-gray-200">
                                  Comprehensive scan results from Probium analysis
                                </DialogDescription>
                              </DialogHeader>

                              {selectedResult && (
                                <Tabs defaultValue="overview" className="space-y-4">
                                  <TabsList className="grid w-full grid-cols-6 bg-gray-900">
                                    <TabsTrigger value="overview">Overview</TabsTrigger>
                                    <TabsTrigger value="hashes">Hashes</TabsTrigger>
                                    <TabsTrigger value="metadata">Metadata</TabsTrigger>
                                    <TabsTrigger value="structure">Structure</TabsTrigger>
                                    <TabsTrigger value="security">Security</TabsTrigger>
                                    <TabsTrigger value="performance">Performance</TabsTrigger>
                                  </TabsList>

                                  <TabsContent value="overview" className="space-y-4">
                                    <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                                      <div className="p-3 bg-gray-800 rounded-lg border border-gray-700">
                                        <p className="text-xs text-purple-300">File Type</p>
                                        <p className="text-white font-medium">{selectedResult.detectedType}</p>
                                      </div>
                                      <div className="p-3 bg-gray-800 rounded-lg border border-gray-700">
                                        <p className="text-xs text-purple-300">MIME Type</p>
                                        <p className="text-white font-medium">{selectedResult.mimeType}</p>
                                      </div>
                                      <div className="p-3 bg-gray-800 rounded-lg border border-gray-700">
                                        <p className="text-xs text-purple-300">Confidence</p>
                                        <p className="text-white font-medium">
                                          {(selectedResult.confidence * 100).toFixed(1)}%
                                        </p>
                                      </div>
                                      <div className="p-3 bg-gray-800 rounded-lg border border-gray-700">
                                        <p className="text-xs text-purple-300">Probium Version</p>
                                        <p className="text-white font-medium">{selectedResult.probiumVersion}</p>
                                      </div>
                                    </div>

                                    <div className="space-y-2">
                                      <p className="text-sm font-medium text-gray-200">Detection Engines Used:</p>
                                      <div className="flex flex-wrap gap-2">
                                        {selectedResult.engines.map((engine: string) => (
                                          <Badge
                                            key={engine}
                                            variant="secondary"
                                            className="bg-purple-600 text-gray-100"
                                          >
                                            {engine}
                                          </Badge>
                                        ))}
                                      </div>
                                    </div>
                                  </TabsContent>

                                  <TabsContent value="hashes" className="space-y-3">
                                    {Object.entries(selectedResult.hashes || {}).map(([type, hash]) => (
                                      <div
                                        key={type}
                                        className="flex items-center justify-between p-3 bg-gray-800 rounded-lg border border-gray-700"
                                      >
                                        <div className="flex items-center gap-2">
                                          <Hash className="w-4 h-4 text-purple-300" />
                                          <span className="text-gray-200 uppercase font-medium">{type}</span>
                                        </div>
                                        <code className="text-white text-sm font-mono bg-gray-800 px-2 py-1 rounded">
                                          {hash as string}
                                        </code>
                                      </div>
                                    ))}
                                  </TabsContent>

                                  <TabsContent value="metadata" className="space-y-3">
                                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                                      {Object.entries(selectedResult.metadata || {}).map(([key, value]) => (
                                        <div
                                          key={key}
                                          className="p-3 bg-gray-800 rounded-lg border border-gray-700"
                                        >
                                          <p className="text-xs text-purple-300 capitalize mb-1">
                                            {key.replace(/([A-Z])/g, " $1")}
                                          </p>
                                          <p className="text-white">
                                            {Array.isArray(value) ? value.join(", ") : String(value)}
                                          </p>
                                        </div>
                                      ))}
                                    </div>
                                  </TabsContent>

                                  <TabsContent value="structure" className="space-y-3">
                                    <div className="grid grid-cols-2 md:grid-cols-3 gap-4">
                                      {Object.entries(selectedResult.structure || {}).map(([key, value]) => (
                                        <div
                                          key={key}
                                          className="p-3 bg-gray-800 rounded-lg border border-gray-700"
                                        >
                                          <p className="text-xs text-purple-300 capitalize mb-1">{key}</p>
                                          <p className="text-white font-medium">{String(value)}</p>
                                        </div>
                                      ))}
                                    </div>
                                  </TabsContent>

                                  <TabsContent value="security" className="space-y-4">
                                    <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                                      <div className="p-4 bg-gray-800 rounded-lg border border-gray-700">
                                        <div className="flex items-center gap-2 mb-2">
                                          <Shield className="w-5 h-5 text-purple-300" />
                                          <p className="text-sm font-medium text-gray-200">Malware Score</p>
                                        </div>
                                        <p className="text-2xl font-bold text-white">
                                          {selectedResult.security?.malwareScore || 0}
                                        </p>
                                      </div>
                                      <div className="p-4 bg-gray-800 rounded-lg border border-gray-700">
                                        <div className="flex items-center gap-2 mb-2">
                                          <AlertTriangle className="w-5 h-5 text-purple-300" />
                                          <p className="text-sm font-medium text-gray-200">Threat Level</p>
                                        </div>
                                        <Badge
                                          className={getThreatColor(selectedResult.security?.threatLevel || "low")}
                                        >
                                          {selectedResult.security?.threatLevel || "low"}
                                        </Badge>
                                      </div>
                                      <div className="p-4 bg-gray-800 rounded-lg border border-gray-700">
                                        <div className="flex items-center gap-2 mb-2">
                                          <FileText className="w-5 h-5 text-purple-300" />
                                          <p className="text-sm font-medium text-gray-200">Embedded Files</p>
                                        </div>
                                        <p className="text-2xl font-bold text-white">
                                          {selectedResult.security?.embedded?.files || 0}
                                        </p>
                                      </div>
                                    </div>
                                  </TabsContent>

                                  <TabsContent value="performance" className="space-y-4">
                                    <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                                      <div className="p-3 bg-gray-800 rounded-lg border border-gray-700">
                                        <div className="flex items-center gap-2 mb-1">
                                          <Clock className="w-4 h-4 text-purple-300" />
                                          <p className="text-xs text-purple-300">Total Time</p>
                                        </div>
                                        <p className="text-white font-medium">{selectedResult.performance?.scanTime}</p>
                                      </div>
                                      <div className="p-3 bg-gray-800 rounded-lg border border-gray-700">
                                        <div className="flex items-center gap-2 mb-1">
                                          <Activity className="w-4 h-4 text-purple-300" />
                                          <p className="text-xs text-purple-300">Memory Used</p>
                                        </div>
                                        <p className="text-white font-medium">
                                          {selectedResult.performance?.memoryUsed}
                                        </p>
                                      </div>
                                      <div className="p-3 bg-gray-800 rounded-lg border border-gray-700">
                                        <div className="flex items-center gap-2 mb-1">
                                          <Cpu className="w-4 h-4 text-purple-300" />
                                          <p className="text-xs text-purple-300">CPU Time</p>
                                        </div>
                                        <p className="text-white font-medium">{selectedResult.performance?.cpuTime}</p>
                                      </div>
                                      <div className="p-3 bg-gray-800 rounded-lg border border-gray-700">
                                        <div className="flex items-center gap-2 mb-1">
                                          <TrendingUp className="w-4 h-4 text-purple-300" />
                                          <p className="text-xs text-purple-300">Efficiency</p>
                                        </div>
                                        <p className="text-white font-medium">
                                          {(
                                            selectedResult.size /
                                            1024 /
                                            1024 /
                                            Number.parseFloat(selectedResult.performance?.scanTime || "1")
                                          ).toFixed(1)}{" "}
                                          MB/s
                                        </p>
                                      </div>
                                    </div>

                                    <div className="space-y-3">
                                      <p className="text-sm font-medium text-gray-200">Engine Performance:</p>
                                      {Object.entries(selectedResult.performance?.engineTimes || {}).map(
                                        ([engine, time]) => (
                                          <div
                                            key={engine}
                                            className="flex items-center justify-between p-2 bg-gray-800 rounded border border-gray-700"
                                          >
                                            <span className="text-gray-200 capitalize">{engine} Engine</span>
                                            <span className="text-white font-mono">{time as string}</span>
                                          </div>
                                        ),
                                      )}
                                    </div>
                                  </TabsContent>
                                </Tabs>
                              )}
                            </DialogContent>
                          </Dialog>
                        </TableCell>
                      </TableRow>
                    ))}
                  </TableBody>
                </Table>
              </div>
            ) : (
              <Card className="bg-gray-800 border-gray-700">
                <CardContent className="p-12 text-center">
                  <FileText className="w-12 h-12 text-purple-300 mx-auto mb-4" />
                  <h3 className="text-lg font-semibold text-white mb-2">No Results Found</h3>
                  <p className="text-gray-200">
                    {results.length === 0
                      ? "Upload and scan files to see results here"
                      : "No results match your current filters"}
                  </p>
                </CardContent>
              </Card>
            )}
          </div>
        </CardContent>
      </Card>

      {/* File Type Distribution */}
      {Object.keys(stats.fileTypes).length > 0 && (
        <Card className="bg-gray-800 border-gray-700">
          <CardHeader>
            <CardTitle className="text-white flex items-center gap-2">
              <BarChart3 className="w-5 h-5" />
              File Type Distribution
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-3">
              {Object.entries(stats.fileTypes).map(([type, count]) => (
                <div key={type} className="flex items-center justify-between">
                  <span className="text-gray-200">{type}</span>
                  <div className="flex items-center gap-3">
                    <div className="w-32 bg-gray-900 rounded-full h-2">
                      <div
                        className="bg-purple-600 h-2 rounded-full"
                        style={{ width: `${(count / stats.total) * 100}%` }}
                      />
                    </div>
                    <span className="text-white font-medium w-8 text-right">{count}</span>
                  </div>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>
      )}
    </div>
  )
}
