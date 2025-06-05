
import React, { useState } from 'react';
import { RelayController } from '../components/RelayController';
import { FileManager } from '../components/FileManager';
import { Zap, HardDrive, Wifi } from 'lucide-react';

const Index = () => {
  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-blue-900 to-slate-800">
      {/* Header */}
      <header className="bg-slate-800/50 backdrop-blur-sm border-b border-slate-700">
        <div className="container mx-auto px-6 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-3">
              <div className="p-2 bg-blue-500 rounded-lg">
                <Zap className="h-6 w-6 text-white" />
              </div>
              <div>
                <h1 className="text-2xl font-bold text-white">Sistema Domótico</h1>
                <p className="text-slate-300 text-sm">Control inteligente del hogar</p>
              </div>
            </div>
            <div className="flex items-center space-x-2 text-green-400">
              <Wifi className="h-5 w-5" />
              <span className="text-sm font-medium">Conectado</span>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="container mx-auto px-6 py-8">
        <div className="grid grid-cols-1 xl:grid-cols-2 gap-8">
          {/* Relay Control Section */}
          <div className="space-y-6">
            <div className="flex items-center space-x-3 mb-6">
              <Zap className="h-6 w-6 text-blue-400" />
              <h2 className="text-xl font-semibold text-white">Control de Dispositivos</h2>
            </div>
            <RelayController />
          </div>

          {/* File Management Section */}
          <div className="space-y-6">
            <div className="flex items-center space-x-3 mb-6">
              <HardDrive className="h-6 w-6 text-green-400" />
              <h2 className="text-xl font-semibold text-white">Gestión de Archivos</h2>
            </div>
            <FileManager />
          </div>
        </div>
      </main>

      {/* Footer */}
      <footer className="bg-slate-800/50 backdrop-blur-sm border-t border-slate-700 mt-16">
        <div className="container mx-auto px-6 py-4">
          <div className="text-center text-slate-400 text-sm">
            <p>Raspberry Pi - Sistema Domótico v1.0</p>
            <p className="mt-1">192.168.1.100:5000</p>
          </div>
        </div>
      </footer>
    </div>
  );
};

export default Index;
