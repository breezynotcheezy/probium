"use client"

import { useMemo } from "react"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Progress } from "@/components/ui/progress"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { AlertTriangle, Shield, Eye, FileX, Lock, Zap } from "lucide-react"
import type { ScanResult } from "@/lib/api"

interface ThreatDetectionProps {
  results: ScanResult[]
  config: any
}

export function ThreatDetection({ results, config }: ThreatDetectionProps) {
  const threatAnalysis = useMemo(() => {
    const threats = results.filter((r) => r.security && r.security.threat_level !== "low")
    const highThreats = threats.filter((r) => r.security?.threat_level === "high")
    const mediumThreats = threats.filter((r) => r.security?.threat_level === "medium")

    const anomalies = results.reduce(
      (acc, r) => {
        if (r.security?.anomalies) {
          acc.push(
            ...r.security.anomalies.map((anomaly) => ({
              filename: r.filename,
              anomaly,
              threat_level: r.security?.threat_level || "low",
            })),
          )
        }
        return acc
      },
      [] as Array<{ filename: string; anomaly: string; threat_level: string }>,
    )

    const suspiciousFiles = results.filter((r) => r.security?.malware_score && r.security.malware_score > 0.3)

    return {
      totalThreats: threats.length,
      highThreats: highThreats.length,
      mediumThreats: mediumThreats.length,
      anomalies,
      suspiciousFiles,
      threatPercentage: results.length > 0 ? (threats.length / results.length) * 100 : 0,
    }
  }, [results])

  const getThreatColor = (level: string) => {
    switch (level) {
      case "high":
        return "text-red-400 bg-red-900/30 border-red-600"
      case "medium":
        return "text-yellow-400 bg-yellow-900/30 border-yellow-600"
      default:
        return "text-green-400 bg-green-900/30 border-green-600"
    }
  }

  return (
    <div className="space-y-6">
      {/* Threat Overview */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <Card className="bg-purple-50 border-purple-300">
          <CardContent className="p-4">
            <div className="flex items-center gap-3">
              <AlertTriangle className="w-8 h-8 text-red-400" />
              <div>
                <p className="text-sm text-purple-700">Total Threats</p>
                <p className="text-2xl font-bold text-white">{threatAnalysis.totalThreats}</p>
              </div>
            </div>
          </CardContent>
        </Card>

        <Card className="bg-purple-50 border-purple-300">
          <CardContent className="p-4">
            <div className="flex items-center gap-3">
              <Shield className="w-8 h-8 text-yellow-400" />
              <div>
                <p className="text-sm text-purple-700">High Risk</p>
                <p className="text-2xl font-bold text-white">{threatAnalysis.highThreats}</p>
              </div>
            </div>
          </CardContent>
        </Card>

        <Card className="bg-purple-50 border-purple-300">
          <CardContent className="p-4">
            <div className="flex items-center gap-3">
              <Eye className="w-8 h-8 text-orange-400" />
              <div>
                <p className="text-sm text-purple-700">Anomalies</p>
                <p className="text-2xl font-bold text-white">{threatAnalysis.anomalies.length}</p>
              </div>
            </div>
          </CardContent>
        </Card>

        <Card className="bg-purple-50 border-purple-300">
          <CardContent className="p-4">
            <div className="flex items-center gap-3">
              <FileX className="w-8 h-8 text-purple-600" />
              <div>
                <p className="text-sm text-purple-700">Suspicious</p>
                <p className="text-2xl font-bold text-white">{threatAnalysis.suspiciousFiles.length}</p>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Threat Analysis Dashboard */}
      <Card className="bg-purple-50 border-purple-300">
        <CardHeader>
          <CardTitle className="text-white flex items-center gap-2">
            <Shield className="w-5 h-5" />
            Threat Detection & Analysis
          </CardTitle>
          <CardDescription className="text-purple-700">Security assessment and threat categorization</CardDescription>
        </CardHeader>
        <CardContent>
          <Tabs defaultValue="overview" className="space-y-4">
            <TabsList className="grid w-full grid-cols-4 bg-purple-100">
              <TabsTrigger value="overview">Overview</TabsTrigger>
              <TabsTrigger value="threats">Threats</TabsTrigger>
              <TabsTrigger value="anomalies">Anomalies</TabsTrigger>
              <TabsTrigger value="prevention">Prevention</TabsTrigger>
            </TabsList>

            <TabsContent value="overview" className="space-y-4">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <Card className="bg-purple-50 border-purple-300">
                  <CardHeader>
                    <CardTitle className="text-white text-lg">Threat Distribution</CardTitle>
                  </CardHeader>
                  <CardContent className="space-y-4">
                    <div className="space-y-3">
                      <div className="flex justify-between items-center">
                        <span className="text-purple-700">High Risk</span>
                        <div className="flex items-center gap-2">
                          <div className="w-24 bg-purple-50 rounded-full h-2">
                            <div
                              className="bg-red-500 h-2 rounded-full"
                              style={{
                                width: `${results.length > 0 ? (threatAnalysis.highThreats / results.length) * 100 : 0}%`,
                              }}
                            />
                          </div>
                          <span className="text-white font-medium w-8">{threatAnalysis.highThreats}</span>
                        </div>
                      </div>
                      <div className="flex justify-between items-center">
                        <span className="text-purple-700">Medium Risk</span>
                        <div className="flex items-center gap-2">
                          <div className="w-24 bg-purple-50 rounded-full h-2">
                            <div
                              className="bg-yellow-500 h-2 rounded-full"
                              style={{
                                width: `${results.length > 0 ? (threatAnalysis.mediumThreats / results.length) * 100 : 0}%`,
                              }}
                            />
                          </div>
                          <span className="text-white font-medium w-8">{threatAnalysis.mediumThreats}</span>
                        </div>
                      </div>
                      <div className="flex justify-between items-center">
                        <span className="text-purple-700">Low Risk</span>
                        <div className="flex items-center gap-2">
                          <div className="w-24 bg-purple-50 rounded-full h-2">
                            <div
                              className="bg-green-500 h-2 rounded-full"
                              style={{
                                width: `${results.length > 0 ? ((results.length - threatAnalysis.totalThreats) / results.length) * 100 : 0}%`,
                              }}
                            />
                          </div>
                          <span className="text-white font-medium w-8">
                            {results.length - threatAnalysis.totalThreats}
                          </span>
                        </div>
                      </div>
                    </div>
                  </CardContent>
                </Card>

                <Card className="bg-purple-50 border-purple-300">
                  <CardHeader>
                    <CardTitle className="text-white text-lg">Security Score</CardTitle>
                  </CardHeader>
                  <CardContent className="space-y-4">
                    <div className="text-center">
                      <div className="text-4xl font-bold text-white mb-2">
                        {(100 - threatAnalysis.threatPercentage).toFixed(0)}%
                      </div>
                      <p className="text-purple-700">Overall Security Score</p>
                    </div>
                    <Progress value={100 - threatAnalysis.threatPercentage} className="bg-purple-200" />
                    <div className="text-center text-sm text-purple-600">
                      {threatAnalysis.threatPercentage < 10
                        ? "Excellent"
                        : threatAnalysis.threatPercentage < 25
                          ? "Good"
                          : threatAnalysis.threatPercentage < 50
                            ? "Fair"
                            : "Poor"}{" "}
                      security posture
                    </div>
                  </CardContent>
                </Card>
              </div>
            </TabsContent>

            <TabsContent value="threats" className="space-y-4">
              <Card className="bg-purple-50 border-purple-300">
                <CardHeader>
                  <CardTitle className="text-white text-lg">Detected Threats</CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="space-y-3">
                    {threatAnalysis.suspiciousFiles.length > 0 ? (
                      threatAnalysis.suspiciousFiles.map((file, index) => (
                        <div
                          key={index}
                          className="flex items-center justify-between p-3 bg-purple-50 rounded border border-purple-300"
                        >
                          <div className="flex items-center gap-3">
                            <AlertTriangle className="w-5 h-5 text-red-400" />
                            <div>
                              <p className="text-white font-medium">{file.filename}</p>
                              <p className="text-purple-600 text-sm">
                                Malware Score: {file.security?.malware_score?.toFixed(2)}
                              </p>
                            </div>
                          </div>
                          <Badge className={getThreatColor(file.security?.threat_level || "low")}>
                            {file.security?.threat_level || "low"}
                          </Badge>
                        </div>
                      ))
                    ) : (
                      <div className="text-center py-8">
                        <Shield className="w-12 h-12 text-green-400 mx-auto mb-4" />
                        <h3 className="text-lg font-semibold text-white mb-2">No Threats Detected</h3>
                        <p className="text-purple-700">All scanned files appear to be safe</p>
                      </div>
                    )}
                  </div>
                </CardContent>
              </Card>
            </TabsContent>

            <TabsContent value="anomalies" className="space-y-4">
              <Card className="bg-purple-50 border-purple-300">
                <CardHeader>
                  <CardTitle className="text-white text-lg">File Anomalies</CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="space-y-3">
                    {threatAnalysis.anomalies.length > 0 ? (
                      threatAnalysis.anomalies.map((anomaly, index) => (
                        <div
                          key={index}
                          className="flex items-center justify-between p-3 bg-purple-50 rounded border border-purple-300"
                        >
                          <div className="flex items-center gap-3">
                            <Eye className="w-5 h-5 text-yellow-400" />
                            <div>
                              <p className="text-white font-medium">{anomaly.filename}</p>
                              <p className="text-purple-600 text-sm">{anomaly.anomaly}</p>
                            </div>
                          </div>
                          <Badge className={getThreatColor(anomaly.threat_level)}>{anomaly.threat_level}</Badge>
                        </div>
                      ))
                    ) : (
                      <div className="text-center py-8">
                        <Eye className="w-12 h-12 text-green-400 mx-auto mb-4" />
                        <h3 className="text-lg font-semibold text-white mb-2">No Anomalies Detected</h3>
                        <p className="text-purple-700">All files conform to expected patterns</p>
                      </div>
                    )}
                  </div>
                </CardContent>
              </Card>
            </TabsContent>

            <TabsContent value="prevention" className="space-y-4">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <Card className="bg-purple-50 border-purple-300">
                  <CardHeader>
                    <CardTitle className="text-white text-lg flex items-center gap-2">
                      <Lock className="w-5 h-5" />
                      Security Recommendations
                    </CardTitle>
                  </CardHeader>
                  <CardContent className="space-y-3">
                    <div className="p-3 bg-purple-50 rounded border border-purple-300">
                      <h4 className="text-white font-medium mb-1">Enable Real-time Scanning</h4>
                      <p className="text-purple-700 text-sm">Monitor files as they are accessed or modified</p>
                    </div>
                    <div className="p-3 bg-purple-50 rounded border border-purple-300">
                      <h4 className="text-white font-medium mb-1">Update Engine Signatures</h4>
                      <p className="text-purple-700 text-sm">
                        Keep detection engines updated with latest threat signatures
                      </p>
                    </div>
                    <div className="p-3 bg-purple-50 rounded border border-purple-300">
                      <h4 className="text-white font-medium mb-1">Quarantine Suspicious Files</h4>
                      <p className="text-purple-700 text-sm">Automatically isolate files with high threat scores</p>
                    </div>
                  </CardContent>
                </Card>

                <Card className="bg-purple-50 border-purple-300">
                  <CardHeader>
                    <CardTitle className="text-white text-lg flex items-center gap-2">
                      <Zap className="w-5 h-5" />
                      Quick Actions
                    </CardTitle>
                  </CardHeader>
                  <CardContent className="space-y-3">
                    <button className="w-full p-3 bg-red-900/30 border border-red-600 rounded text-red-300 hover:bg-red-900/50 transition-colors">
                      Quarantine All High-Risk Files
                    </button>
                    <button className="w-full p-3 bg-yellow-900/30 border border-yellow-600 rounded text-yellow-300 hover:bg-yellow-900/50 transition-colors">
                      Review Medium-Risk Files
                    </button>
                    <button className="w-full p-3 bg-blue-900/30 border border-blue-600 rounded text-blue-300 hover:bg-blue-900/50 transition-colors">
                      Generate Security Report
                    </button>
                    <button className="w-full p-3 bg-purple-50 border border-purple-300 rounded text-purple-700 hover:bg-purple-50 transition-colors">
                      Update Threat Database
                    </button>
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
