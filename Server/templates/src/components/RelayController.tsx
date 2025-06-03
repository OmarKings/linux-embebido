
import React, { useState } from 'react';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Lightbulb, Fan, Tv, Coffee, Power } from 'lucide-react';
import { useToast } from '@/hooks/use-toast';

interface Device {
  id: number;
  name: string;
  icon: React.ComponentType<{ className?: string }>;
  status: boolean;
  pin: number;
}

export const RelayController = () => {
  const { toast } = useToast();
  
  const [devices, setDevices] = useState<Device[]>([
    { id: 1, name: 'Foco Principal', icon: Lightbulb, status: false, pin: 18 },
    { id: 2, name: 'Ventilador', icon: Fan, status: false, pin: 19 },
    { id: 3, name: 'TV/Monitor', icon: Tv, status: false, pin: 20 },
    { id: 4, name: 'Cafetera', icon: Coffee, status: false, pin: 21 }
  ]);

  const toggleDevice = (id: number) => {
    setDevices(prev => 
      prev.map(device => 
        device.id === id 
          ? { ...device, status: !device.status }
          : device
      )
    );

    const device = devices.find(d => d.id === id);
    if (device) {
      toast({
        title: device.status ? "Dispositivo Apagado" : "Dispositivo Encendido",
        description: `${device.name} ${device.status ? 'desactivado' : 'activado'} en pin GPIO ${device.pin}`,
      });
    }
  };

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
      {devices.map((device) => {
        const IconComponent = device.icon;
        return (
          <Card key={device.id} className="bg-slate-800/50 border-slate-700 hover:bg-slate-800/70 transition-all duration-200">
            <CardHeader className="pb-3">
              <CardTitle className="flex items-center justify-between text-white">
                <div className="flex items-center space-x-3">
                  <div className={`p-2 rounded-lg ${device.status ? 'bg-green-500' : 'bg-slate-600'}`}>
                    <IconComponent className="h-5 w-5 text-white" />
                  </div>
                  <span className="text-lg">{device.name}</span>
                </div>
                <div className={`px-2 py-1 rounded-full text-xs font-medium ${
                  device.status 
                    ? 'bg-green-500/20 text-green-300 border border-green-500/30' 
                    : 'bg-red-500/20 text-red-300 border border-red-500/30'
                }`}>
                  {device.status ? 'ON' : 'OFF'}
                </div>
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-3">
                <div className="text-sm text-slate-400">
                  Pin GPIO: <span className="font-mono text-blue-400">{device.pin}</span>
                </div>
                <Button
                  onClick={() => toggleDevice(device.id)}
                  className={`w-full transition-all duration-200 ${
                    device.status
                      ? 'bg-red-500 hover:bg-red-600 text-white'
                      : 'bg-green-500 hover:bg-green-600 text-white'
                  }`}
                >
                  <Power className="h-4 w-4 mr-2" />
                  {device.status ? 'Apagar' : 'Encender'}
                </Button>
              </div>
            </CardContent>
          </Card>
        );
      })}
    </div>
  );
};
