
import React, { useState, useRef } from 'react';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Upload, Download, Eye, Trash2, File, Image, FileText, Archive } from 'lucide-react';
import { useToast } from '@/hooks/use-toast';

interface FileItem {
  id: string;
  name: string;
  size: number;
  type: string;
  uploadDate: Date;
  url?: string;
}

export const FileManager = () => {
  const { toast } = useToast();
  const fileInputRef = useRef<HTMLInputElement>(null);
  
  const [files, setFiles] = useState<FileItem[]>([
    {
      id: '1',
      name: 'configuracion.json',
      size: 2048,
      type: 'application/json',
      uploadDate: new Date('2024-06-01'),
    },
    {
      id: '2',
      name: 'camara_entrada.jpg',
      size: 1536000,
      type: 'image/jpeg',
      uploadDate: new Date('2024-06-02'),
    },
    {
      id: '3',
      name: 'manual_sistema.pdf',
      size: 5242880,
      type: 'application/pdf',
      uploadDate: new Date('2024-06-03'),
    }
  ]);

  const formatFileSize = (bytes: number) => {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
  };

  const getFileIcon = (type: string) => {
    if (type.startsWith('image/')) return Image;
    if (type.includes('pdf')) return FileText;
    if (type.includes('zip') || type.includes('rar')) return Archive;
    return File;
  };

  const handleFileUpload = (event: React.ChangeEvent<HTMLInputElement>) => {
    const uploadedFiles = event.target.files;
    if (uploadedFiles) {
      Array.from(uploadedFiles).forEach(file => {
        const newFile: FileItem = {
          id: Date.now().toString() + Math.random().toString(36).substr(2, 9),
          name: file.name,
          size: file.size,
          type: file.type,
          uploadDate: new Date(),
          url: URL.createObjectURL(file)
        };
        
        setFiles(prev => [newFile, ...prev]);
        
        toast({
          title: "Archivo Subido",
          description: `${file.name} se ha subido correctamente`,
        });
      });
    }
    
    // Reset input
    if (fileInputRef.current) {
      fileInputRef.current.value = '';
    }
  };

  const handleView = (file: FileItem) => {
    if (file.url) {
      window.open(file.url, '_blank');
    } else {
      toast({
        title: "Vista Previa",
        description: `Abriendo ${file.name}...`,
      });
    }
  };

  const handleDownload = (file: FileItem) => {
    if (file.url) {
      const link = document.createElement('a');
      link.href = file.url;
      link.download = file.name;
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
    }
    
    toast({
      title: "Descarga Iniciada",
      description: `Descargando ${file.name}...`,
    });
  };

  const handleDelete = (id: string) => {
    const file = files.find(f => f.id === id);
    setFiles(prev => prev.filter(f => f.id !== id));
    
    toast({
      title: "Archivo Eliminado",
      description: `${file?.name} ha sido eliminado del sistema`,
      variant: "destructive"
    });
  };

  return (
    <div className="space-y-6">
      {/* Upload Section */}
      <Card className="bg-slate-800/50 border-slate-700">
        <CardHeader>
          <CardTitle className="text-white flex items-center space-x-2">
            <Upload className="h-5 w-5" />
            <span>Subir Archivos</span>
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            <input
              ref={fileInputRef}
              type="file"
              multiple
              onChange={handleFileUpload}
              className="hidden"
              accept=".jpg,.jpeg,.png,.pdf,.txt,.json,.zip,.rar"
            />
            <Button
              onClick={() => fileInputRef.current?.click()}
              className="w-full bg-blue-500 hover:bg-blue-600 text-white"
            >
              <Upload className="h-4 w-4 mr-2" />
              Seleccionar Archivos
            </Button>
            <p className="text-xs text-slate-400 text-center">
              Formatos permitidos: JPG, PNG, PDF, TXT, JSON, ZIP, RAR (Max: 10MB)
            </p>
          </div>
        </CardContent>
      </Card>

      {/* Files List */}
      <Card className="bg-slate-800/50 border-slate-700">
        <CardHeader>
          <CardTitle className="text-white">
            Archivos Almacenados ({files.length})
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="space-y-3 max-h-96 overflow-y-auto">
            {files.length === 0 ? (
              <div className="text-center py-8 text-slate-400">
                <File className="h-12 w-12 mx-auto mb-3 opacity-50" />
                <p>No hay archivos almacenados</p>
              </div>
            ) : (
              files.map((file) => {
                const IconComponent = getFileIcon(file.type);
                return (
                  <div
                    key={file.id}
                    className="flex items-center justify-between p-3 bg-slate-700/30 rounded-lg border border-slate-600 hover:bg-slate-700/50 transition-colors"
                  >
                    <div className="flex items-center space-x-3 flex-1 min-w-0">
                      <div className="p-2 bg-slate-600 rounded">
                        <IconComponent className="h-4 w-4 text-slate-300" />
                      </div>
                      <div className="flex-1 min-w-0">
                        <h4 className="text-white font-medium truncate">{file.name}</h4>
                        <p className="text-xs text-slate-400">
                          {formatFileSize(file.size)} • {file.uploadDate.toLocaleDateString()}
                        </p>
                      </div>
                    </div>
                    <div className="flex items-center space-x-1 ml-4">
                      <Button
                        size="sm"
                        variant="ghost"
                        onClick={() => handleView(file)}
                        className="text-blue-400 hover:text-blue-300 hover:bg-blue-500/20"
                      >
                        <Eye className="h-4 w-4" />
                      </Button>
                      <Button
                        size="sm"
                        variant="ghost"
                        onClick={() => handleDownload(file)}
                        className="text-green-400 hover:text-green-300 hover:bg-green-500/20"
                      >
                        <Download className="h-4 w-4" />
                      </Button>
                      <Button
                        size="sm"
                        variant="ghost"
                        onClick={() => handleDelete(file.id)}
                        className="text-red-400 hover:text-red-300 hover:bg-red-500/20"
                      >
                        <Trash2 className="h-4 w-4" />
                      </Button>
                    </div>
                  </div>
                );
              })
            )}
          </div>
        </CardContent>
      </Card>
    </div>
  );
};
