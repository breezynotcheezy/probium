"use client"

import { useState } from "react"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Badge } from "@/components/ui/badge"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table"
import { FileType, Plus, Search, Edit, Trash2, Download, Upload } from "lucide-react"

interface FileTypeRegistryProps {
  config: any
  onConfigChange: (config: any) => void
}

export function FileTypeRegistry({ config, onConfigChange }: FileTypeRegistryProps) {
  const [searchTerm, setSearchTerm] = useState("")
  const [selectedCategory, setSelectedCategory] = useState("all")

  // Mock file type database - in real implementation this would come from Probium
  const fileTypes = [
    {
      id: "pdf",
      name: "PDF Document",
      mime_type: "application/pdf",
      extensions: ["pdf"],
      magic_bytes: "%PDF",
      category: "document",
      description: "Portable Document Format",
      confidence_threshold: 0.9,
      engines: ["pdf", "binary"],
    },
    {
      id: "zip",
      name: "ZIP Archive",
      mime_type: "application/zip",
      extensions: ["zip"],
      magic_bytes: "PK\\x03\\x04",
      category: "archive",
      description: "ZIP compressed archive",
      confidence_threshold: 0.95,
      engines: ["zip", "archive"],
    },
    {
      id: "docx",
      name: "Word Document",
      mime_type: "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
      extensions: ["docx"],
      magic_bytes: "PK\\x03\\x04",
      category: "document",
      description: "Microsoft Word document",
      confidence_threshold: 0.9,
      engines: ["zipoffice", "office"],
    },
    {
      id: "jpeg",
      name: "JPEG Image",
      mime_type: "image/jpeg",
      extensions: ["jpg", "jpeg"],
      magic_bytes: "\\xFF\\xD8\\xFF",
      category: "image",
      description: "JPEG image format",
      confidence_threshold: 0.95,
      engines: ["image", "binary"],
    },
    {
      id: "png",
      name: "PNG Image",
      mime_type: "image/png",
      extensions: ["png"],
      magic_bytes: "\\x89PNG\\r\\n\\x1a\\n",
      category: "image",
      description: "Portable Network Graphics",
      confidence_threshold: 0.98,
      engines: ["image", "binary"],
    },
  ]

  const categories = ["all", "document", "image", "archive", "executable", "text", "video", "audio"]

  const filteredFileTypes = fileTypes.filter((ft) => {
    const matchesSearch =
      ft.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
      ft.mime_type.toLowerCase().includes(searchTerm.toLowerCase()) ||
      ft.extensions.some((ext) => ext.toLowerCase().includes(searchTerm.toLowerCase()))
    const matchesCategory = selectedCategory === "all" || ft.category === selectedCategory
    return matchesSearch && matchesCategory
  })

  const getCategoryColor = (category: string) => {
    const colors = {
      document: "bg-blue-700",
      image: "bg-green-700",
      archive: "bg-yellow-700",
      executable: "bg-red-700",
      text: "bg-purple-600",
      video: "bg-pink-700",
      audio: "bg-cyan-700",
    }
    return colors[category as keyof typeof colors] || "bg-gray-700"
  }

  return (
    <div className="space-y-6">
      <Card className="bg-gray-800 border-gray-700">
        <CardHeader>
          <CardTitle className="text-white flex items-center gap-2">
            <FileType className="w-5 h-5" />
            File Type Registry
          </CardTitle>
          <CardDescription className="text-gray-200">
            Manage file type definitions, signatures, and detection rules
          </CardDescription>
        </CardHeader>
        <CardContent>
          <Tabs defaultValue="registry" className="space-y-4">
            <TabsList className="grid w-full grid-cols-3 bg-gray-900">
              <TabsTrigger value="registry">Registry</TabsTrigger>
              <TabsTrigger value="signatures">Signatures</TabsTrigger>
              <TabsTrigger value="custom">Custom Types</TabsTrigger>
            </TabsList>

            <TabsContent value="registry" className="space-y-4">
              {/* Search and Filter Controls */}
              <div className="flex flex-col md:flex-row gap-4">
                <div className="relative flex-1">
                  <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-purple-300 w-4 h-4" />
                  <Input
                    placeholder="Search file types..."
                    value={searchTerm}
                    onChange={(e) => setSearchTerm(e.target.value)}
                    className="pl-10 bg-gray-900 border-gray-700 text-white placeholder-purple-400"
                  />
                </div>

                <div className="flex gap-2">
                  {categories.map((category) => (
                    <Button
                      key={category}
                      variant={selectedCategory === category ? "default" : "outline"}
                      size="sm"
                      onClick={() => setSelectedCategory(category)}
                      className={
                        selectedCategory === category
                          ? "bg-purple-600 hover:bg-purple-600"
                          : "border-gray-700 text-gray-200 bg-transparent hover:bg-gray-800"
                      }
                    >
                      {category.charAt(0).toUpperCase() + category.slice(1)}
                    </Button>
                  ))}
                </div>
              </div>

              {/* File Types Table */}
              <Card className="bg-gray-800 border-gray-700">
                <CardContent className="p-0">
                  <Table>
                    <TableHeader>
                      <TableRow className="border-gray-700">
                        <TableHead className="text-gray-200">Type</TableHead>
                        <TableHead className="text-gray-200">MIME Type</TableHead>
                        <TableHead className="text-gray-200">Extensions</TableHead>
                        <TableHead className="text-gray-200">Category</TableHead>
                        <TableHead className="text-gray-200">Engines</TableHead>
                        <TableHead className="text-gray-200">Actions</TableHead>
                      </TableRow>
                    </TableHeader>
                    <TableBody>
                      {filteredFileTypes.map((fileType) => (
                        <TableRow key={fileType.id} className="border-gray-700 hover:bg-gray-800">
                          <TableCell>
                            <div>
                              <p className="font-medium text-white">{fileType.name}</p>
                              <p className="text-sm text-purple-300">{fileType.description}</p>
                            </div>
                          </TableCell>
                          <TableCell>
                            <code className="text-gray-200 bg-gray-800 px-2 py-1 rounded text-xs">
                              {fileType.mime_type}
                            </code>
                          </TableCell>
                          <TableCell>
                            <div className="flex flex-wrap gap-1">
                              {fileType.extensions.map((ext) => (
                                <Badge key={ext} variant="outline" className="border-gray-700 text-gray-200">
                                  .{ext}
                                </Badge>
                              ))}
                            </div>
                          </TableCell>
                          <TableCell>
                            <Badge className={getCategoryColor(fileType.category)}>{fileType.category}</Badge>
                          </TableCell>
                          <TableCell>
                            <div className="flex flex-wrap gap-1">
                              {fileType.engines.map((engine) => (
                                <Badge key={engine} variant="secondary" className="bg-purple-600 text-gray-100">
                                  {engine}
                                </Badge>
                              ))}
                            </div>
                          </TableCell>
                          <TableCell>
                            <div className="flex gap-1">
                              <Button variant="ghost" size="sm" className="text-gray-200 hover:text-white">
                                <Edit className="w-4 h-4" />
                              </Button>
                              <Button variant="ghost" size="sm" className="text-red-400 hover:text-red-300">
                                <Trash2 className="w-4 h-4" />
                              </Button>
                            </div>
                          </TableCell>
                        </TableRow>
                      ))}
                    </TableBody>
                  </Table>
                </CardContent>
              </Card>
            </TabsContent>

            <TabsContent value="signatures" className="space-y-4">
              <Card className="bg-gray-800 border-gray-700">
                <CardHeader>
                  <CardTitle className="text-white text-lg">Magic Byte Signatures</CardTitle>
                  <CardDescription className="text-gray-200">
                    Binary signatures used for file type detection
                  </CardDescription>
                </CardHeader>
                <CardContent className="space-y-4">
                  {filteredFileTypes.map((fileType) => (
                    <div key={fileType.id} className="p-4 bg-gray-800 rounded border border-gray-700">
                      <div className="flex items-center justify-between mb-2">
                        <h3 className="text-white font-medium">{fileType.name}</h3>
                        <Badge className={getCategoryColor(fileType.category)}>{fileType.category}</Badge>
                      </div>
                      <div className="space-y-2">
                        <div>
                          <Label className="text-gray-200 text-sm">Magic Bytes</Label>
                          <code className="block text-purple-300 bg-gray-800 p-2 rounded font-mono text-sm">
                            {fileType.magic_bytes}
                          </code>
                        </div>
                        <div className="flex items-center gap-4">
                          <div>
                            <Label className="text-gray-200 text-sm">Confidence Threshold</Label>
                            <p className="text-white">{(fileType.confidence_threshold * 100).toFixed(0)}%</p>
                          </div>
                          <div>
                            <Label className="text-gray-200 text-sm">Detection Engines</Label>
                            <p className="text-white">{fileType.engines.join(", ")}</p>
                          </div>
                        </div>
                      </div>
                    </div>
                  ))}
                </CardContent>
              </Card>
            </TabsContent>

            <TabsContent value="custom" className="space-y-4">
              <Card className="bg-gray-800 border-gray-700">
                <CardHeader>
                  <CardTitle className="text-white text-lg">Custom File Types</CardTitle>
                  <CardDescription className="text-gray-200">Define custom file type detection rules</CardDescription>
                </CardHeader>
                <CardContent className="space-y-4">
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <div className="space-y-2">
                      <Label className="text-gray-200">Type Name</Label>
                      <Input
                        placeholder="Custom Document"
                        className="bg-gray-800 border-gray-700 text-white placeholder-purple-400"
                      />
                    </div>
                    <div className="space-y-2">
                      <Label className="text-gray-200">MIME Type</Label>
                      <Input
                        placeholder="application/x-custom"
                        className="bg-gray-800 border-gray-700 text-white placeholder-purple-400"
                      />
                    </div>
                    <div className="space-y-2">
                      <Label className="text-gray-200">File Extensions</Label>
                      <Input
                        placeholder="cust,custom"
                        className="bg-gray-800 border-gray-700 text-white placeholder-purple-400"
                      />
                    </div>
                    <div className="space-y-2">
                      <Label className="text-gray-200">Magic Bytes (Hex)</Label>
                      <Input
                        placeholder="\\x43\\x55\\x53\\x54"
                        className="bg-gray-800 border-gray-700 text-white placeholder-purple-400"
                      />
                    </div>
                  </div>

                  <div className="flex gap-2">
                    <Button className="bg-purple-600 hover:bg-purple-600">
                      <Plus className="w-4 h-4 mr-2" />
                      Add Custom Type
                    </Button>
                    <Button variant="outline" className="border-gray-700 text-gray-200 bg-transparent">
                      <Upload className="w-4 h-4 mr-2" />
                      Import Definitions
                    </Button>
                    <Button variant="outline" className="border-gray-700 text-gray-200 bg-transparent">
                      <Download className="w-4 h-4 mr-2" />
                      Export Registry
                    </Button>
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
