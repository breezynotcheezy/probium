"use client"

import { useState } from "react"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import { Textarea } from "@/components/ui/textarea"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { Code, Play, Copy, Download, FileText } from "lucide-react"

interface APIExplorerProps {
  config: any
}

export function APIExplorer({ config }: APIExplorerProps) {
  const [selectedEndpoint, setSelectedEndpoint] = useState("scan_file")
  const [requestBody, setRequestBody] = useState("")
  const [response, setResponse] = useState("")

  const apiEndpoints = {
    scan_file: {
      method: "POST",
      path: "/api/v1/scan/file",
      description: "Scan a single file for type detection",
      example: {
        file: "base64_encoded_file_content",
        engines: ["pdf", "zip", "office"],
        options: {
          deep_analysis: true,
          generate_hashes: true,
          extract_metadata: true,
        },
      },
    },
    scan_batch: {
      method: "POST",
      path: "/api/v1/scan/batch",
      description: "Scan multiple files in parallel",
      example: {
        files: ["file1.pdf", "file2.zip"],
        engines: ["pdf", "zip"],
        options: {
          parallel_processing: true,
          thread_pool_size: 8,
        },
      },
    },
    get_engines: {
      method: "GET",
      path: "/api/v1/engines",
      description: "Get list of available detection engines",
      example: {},
    },
    engine_status: {
      method: "GET",
      path: "/api/v1/engines/status",
      description: "Get status and performance of all engines",
      example: {},
    },
    scan_url: {
      method: "POST",
      path: "/api/v1/scan/url",
      description: "Scan a file from URL",
      example: {
        url: "https://example.com/file.pdf",
        engines: ["pdf"],
        download_timeout: 30,
      },
    },
  }

  const executeRequest = async () => {
    const endpoint = apiEndpoints[selectedEndpoint as keyof typeof apiEndpoints]

    // Simulate API response
    const mockResponse = {
      scan_file: {
        success: true,
        result: {
          filename: "document.pdf",
          detected_type: "PDF Document",
          confidence: 0.97,
          engines_used: ["pdf", "binary"],
          hashes: {
            md5: "d41d8cd98f00b204e9800998ecf8427e",
            sha256: "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
          },
          metadata: {
            pages: 10,
            author: "John Doe",
            creation_date: "2024-01-15T10:30:00Z",
          },
          scan_time: "0.234s",
        },
      },
      scan_batch: {
        success: true,
        batch_id: "batch_123456",
        total_files: 5,
        completed: 5,
        results: [
          { filename: "file1.pdf", detected_type: "PDF Document", confidence: 0.95 },
          { filename: "file2.zip", detected_type: "ZIP Archive", confidence: 0.98 },
        ],
      },
      get_engines: {
        success: true,
        engines: [
          { name: "pdf", version: "2.1.4", status: "active" },
          { name: "zip", version: "1.8.2", status: "active" },
          { name: "office", version: "3.2.1", status: "active" },
        ],
      },
      engine_status: {
        success: true,
        engines: {
          pdf: { status: "active", performance: 95, last_used: "2 min ago" },
          zip: { status: "active", performance: 88, last_used: "5 min ago" },
        },
      },
      scan_url: {
        success: true,
        result: {
          url: "https://example.com/file.pdf",
          downloaded_size: 1024000,
          detected_type: "PDF Document",
          confidence: 0.94,
        },
      },
    }

    setResponse(JSON.stringify(mockResponse[selectedEndpoint as keyof typeof mockResponse], null, 2))
  }

  const copyToClipboard = (text: string) => {
    navigator.clipboard.writeText(text)
  }

  return (
    <div className="space-y-6">
      <Card className="bg-gray-800 border-gray-700">
        <CardHeader>
          <CardTitle className="text-white flex items-center gap-2">
            <Code className="w-5 h-5" />
            Probium API Explorer
          </CardTitle>
          <CardDescription className="text-gray-200">
            Interactive API documentation and testing interface
          </CardDescription>
        </CardHeader>
        <CardContent>
          <Tabs defaultValue="endpoints" className="space-y-4">
            <TabsList className="grid w-full grid-cols-4 bg-gray-900">
              <TabsTrigger value="endpoints">Endpoints</TabsTrigger>
              <TabsTrigger value="examples">Examples</TabsTrigger>
              <TabsTrigger value="sdk">SDK</TabsTrigger>
              <TabsTrigger value="docs">Documentation</TabsTrigger>
            </TabsList>

            <TabsContent value="endpoints" className="space-y-4">
              <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                <Card className="bg-gray-800 border-gray-700">
                  <CardHeader>
                    <CardTitle className="text-white text-lg">API Request</CardTitle>
                  </CardHeader>
                  <CardContent className="space-y-4">
                    <div className="space-y-2">
                      <label className="text-gray-200 text-sm">Endpoint</label>
                      <Select value={selectedEndpoint} onValueChange={setSelectedEndpoint}>
                        <SelectTrigger className="bg-gray-800 border-gray-700 text-white">
                          <SelectValue />
                        </SelectTrigger>
                        <SelectContent className="bg-gray-900 border-gray-700">
                          {Object.entries(apiEndpoints).map(([key, endpoint]) => (
                            <SelectItem key={key} value={key} className="text-white">
                              <div className="flex items-center gap-2">
                                <Badge
                                  className={`text-xs ${endpoint.method === "GET" ? "bg-green-700" : "bg-blue-700"}`}
                                >
                                  {endpoint.method}
                                </Badge>
                                {endpoint.path}
                              </div>
                            </SelectItem>
                          ))}
                        </SelectContent>
                      </Select>
                    </div>

                    <div className="space-y-2">
                      <label className="text-gray-200 text-sm">Request Body</label>
                      <Textarea
                        value={
                          requestBody ||
                          JSON.stringify(apiEndpoints[selectedEndpoint as keyof typeof apiEndpoints].example, null, 2)
                        }
                        onChange={(e) => setRequestBody(e.target.value)}
                        className="bg-gray-800 border-gray-700 text-white font-mono text-sm"
                        rows={10}
                      />
                    </div>

                    <Button onClick={executeRequest} className="w-full bg-purple-600 hover:bg-purple-600">
                      <Play className="w-4 h-4 mr-2" />
                      Execute Request
                    </Button>
                  </CardContent>
                </Card>

                <Card className="bg-gray-800 border-gray-700">
                  <CardHeader>
                    <CardTitle className="text-white text-lg flex items-center justify-between">
                      API Response
                      <Button
                        variant="ghost"
                        size="sm"
                        onClick={() => copyToClipboard(response)}
                        className="text-gray-200"
                      >
                        <Copy className="w-4 h-4" />
                      </Button>
                    </CardTitle>
                  </CardHeader>
                  <CardContent>
                    <div className="space-y-2">
                      <div className="flex items-center gap-2">
                        <Badge className="bg-green-700">200 OK</Badge>
                        <span className="text-gray-200 text-sm">application/json</span>
                      </div>
                      <Textarea
                        value={response}
                        readOnly
                        className="bg-gray-800 border-gray-700 text-white font-mono text-sm"
                        rows={15}
                      />
                    </div>
                  </CardContent>
                </Card>
              </div>

              <Card className="bg-gray-800 border-gray-700">
                <CardHeader>
                  <CardTitle className="text-white text-lg">Endpoint Details</CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="space-y-3">
                    <div className="flex items-center gap-3">
                      <Badge
                        className={`${apiEndpoints[selectedEndpoint as keyof typeof apiEndpoints].method === "GET" ? "bg-green-700" : "bg-blue-700"}`}
                      >
                        {apiEndpoints[selectedEndpoint as keyof typeof apiEndpoints].method}
                      </Badge>
                      <code className="text-gray-200 bg-gray-800 px-2 py-1 rounded">
                        {apiEndpoints[selectedEndpoint as keyof typeof apiEndpoints].path}
                      </code>
                    </div>
                    <p className="text-purple-300">
                      {apiEndpoints[selectedEndpoint as keyof typeof apiEndpoints].description}
                    </p>
                  </div>
                </CardContent>
              </Card>
            </TabsContent>

            <TabsContent value="examples" className="space-y-4">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <Card className="bg-gray-800 border-gray-700">
                  <CardHeader>
                    <CardTitle className="text-white text-lg">Python Example</CardTitle>
                  </CardHeader>
                  <CardContent>
                    <pre className="text-sm text-purple-300 bg-gray-800 p-4 rounded overflow-x-auto">
                      {`import requests
import json

# Scan a file
with open('document.pdf', 'rb') as f:
    files = {'file': f}
    data = {
        'engines': ['pdf', 'binary'],
        'options': json.dumps({
            'deep_analysis': True,
            'generate_hashes': True
        })
    }
    
response = requests.post(
    'http://localhost:8000/api/v1/scan/file',
    files=files,
    data=data
)

result = response.json()
print(f"Detected: {result['result']['detected_type']}")
print(f"Confidence: {result['result']['confidence']}")
`}
                    </pre>
                  </CardContent>
                </Card>

                <Card className="bg-gray-800 border-gray-700">
                  <CardHeader>
                    <CardTitle className="text-white text-lg">cURL Example</CardTitle>
                  </CardHeader>
                  <CardContent>
                    <pre className="text-sm text-purple-300 bg-gray-800 p-4 rounded overflow-x-auto">
                      {`curl -X POST \\
  http://localhost:8000/api/v1/scan/file \\
  -H "Content-Type: multipart/form-data" \\
  -F "file=@document.pdf" \\
  -F "engines=pdf,binary" \\
  -F "options={
    \\"deep_analysis\\": true,
    \\"generate_hashes\\": true
  }"
`}
                    </pre>
                  </CardContent>
                </Card>

                <Card className="bg-gray-800 border-gray-700">
                  <CardHeader>
                    <CardTitle className="text-white text-lg">JavaScript Example</CardTitle>
                  </CardHeader>
                  <CardContent>
                    <pre className="text-sm text-purple-300 bg-gray-800 p-4 rounded overflow-x-auto">
                      {`const formData = new FormData();
formData.append('file', fileInput.files[0]);
formData.append('engines', 'pdf,binary');
formData.append('options', JSON.stringify({
  deep_analysis: true,
  generate_hashes: true
}));

fetch('/api/v1/scan/file', {
  method: 'POST',
  body: formData
})
.then(response => response.json())
.then(data => {
  console.log('Detected:', data.result.detected_type);
  console.log('Confidence:', data.result.confidence);
});
`}
                    </pre>
                  </CardContent>
                </Card>

                <Card className="bg-gray-800 border-gray-700">
                  <CardHeader>
                    <CardTitle className="text-white text-lg">Go Example</CardTitle>
                  </CardHeader>
                  <CardContent>
                    <pre className="text-sm text-purple-300 bg-gray-800 p-4 rounded overflow-x-auto">
                      {`package main

import (
    "bytes"
    "encoding/json"
    "fmt"
    "io"
    "mime/multipart"
    "net/http"
    "os"
)

func main() {
    file, _ := os.Open("document.pdf")
    defer file.Close()
    
    var b bytes.Buffer
    writer := multipart.NewWriter(&b)
    
    part, _ := writer.CreateFormFile("file", "document.pdf")
    io.Copy(part, file)
    
    writer.WriteField("engines", "pdf,binary")
    writer.Close()
    
    resp, _ := http.Post(
        "http://localhost:8000/api/v1/scan/file",
        writer.FormDataContentType(),
        &b,
    )
    defer resp.Body.Close()
}
`}
                    </pre>
                  </CardContent>
                </Card>
              </div>
            </TabsContent>

            <TabsContent value="sdk" className="space-y-4">
              <Card className="bg-gray-800 border-gray-700">
                <CardHeader>
                  <CardTitle className="text-white text-lg flex items-center gap-2">
                    <Download className="w-5 h-5" />
                    Official SDKs
                  </CardTitle>
                </CardHeader>
                <CardContent className="space-y-4">
                  <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                    <div className="p-4 bg-gray-800 rounded border border-gray-700">
                      <h3 className="text-white font-medium mb-2">Python SDK</h3>
                      <p className="text-gray-200 text-sm mb-3">Official Python client library</p>
                      <code className="text-xs text-purple-300 bg-gray-800 px-2 py-1 rounded block mb-2">
                        pip install probium-client
                      </code>
                      <Button size="sm" className="w-full bg-purple-600 hover:bg-purple-600">
                        Download
                      </Button>
                    </div>

                    <div className="p-4 bg-gray-800 rounded border border-gray-700">
                      <h3 className="text-white font-medium mb-2">Node.js SDK</h3>
                      <p className="text-gray-200 text-sm mb-3">JavaScript/TypeScript client</p>
                      <code className="text-xs text-purple-300 bg-gray-800 px-2 py-1 rounded block mb-2">
                        npm install @probium/client
                      </code>
                      <Button size="sm" className="w-full bg-purple-600 hover:bg-purple-600">
                        Download
                      </Button>
                    </div>

                    <div className="p-4 bg-gray-800 rounded border border-gray-700">
                      <h3 className="text-white font-medium mb-2">Go SDK</h3>
                      <p className="text-gray-200 text-sm mb-3">Go client library</p>
                      <code className="text-xs text-purple-300 bg-gray-800 px-2 py-1 rounded block mb-2">
                        go get github.com/probium/go-client
                      </code>
                      <Button size="sm" className="w-full bg-purple-600 hover:bg-purple-600">
                        Download
                      </Button>
                    </div>
                  </div>
                </CardContent>
              </Card>
            </TabsContent>

            <TabsContent value="docs" className="space-y-4">
              <Card className="bg-gray-800 border-gray-700">
                <CardHeader>
                  <CardTitle className="text-white text-lg flex items-center gap-2">
                    <FileText className="w-5 h-5" />
                    API Documentation
                  </CardTitle>
                </CardHeader>
                <CardContent className="space-y-4">
                  <div className="space-y-3">
                    <div className="p-3 bg-gray-800 rounded border border-gray-700">
                      <h3 className="text-white font-medium">Authentication</h3>
                      <p className="text-gray-200 text-sm">
                        API uses Bearer token authentication. Include your API key in the Authorization header.
                      </p>
                    </div>

                    <div className="p-3 bg-gray-800 rounded border border-gray-700">
                      <h3 className="text-white font-medium">Rate Limiting</h3>
                      <p className="text-gray-200 text-sm">
                        API requests are limited to 1000 requests per hour per API key.
                      </p>
                    </div>

                    <div className="p-3 bg-gray-800 rounded border border-gray-700">
                      <h3 className="text-white font-medium">Error Handling</h3>
                      <p className="text-gray-200 text-sm">
                        API returns standard HTTP status codes. Error details are included in the response body.
                      </p>
                    </div>

                    <div className="p-3 bg-gray-800 rounded border border-gray-700">
                      <h3 className="text-white font-medium">Webhooks</h3>
                      <p className="text-gray-200 text-sm">
                        Configure webhooks to receive real-time notifications about scan results.
                      </p>
                    </div>
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
