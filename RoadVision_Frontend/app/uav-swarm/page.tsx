"use client"

import { useState, useEffect } from "react"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Progress } from "@/components/ui/progress"
import { Badge } from "@/components/ui/badge"
import { Plane, AlertTriangle, MapPin, Activity } from "lucide-react"
import { Button } from "@/components/ui/button"

export default function UAVSwarmPage() {
  const [swarmData, setSwarmData] = useState<any>(null)
  const [alerts, setAlerts] = useState<any[]>([])
  const [loading, setLoading] = useState(true)

  const fetchData = async () => {
    try {
      const [swarmRes, alertsRes] = await Promise.all([
        fetch("http://127.0.0.1:8000/api/v1/uav/swarm-status"),
        fetch("http://127.0.0.1:8000/api/v1/uav/critical-alerts")
      ])
      const swarm = await swarmRes.json()
      const criticalAlerts = await alertsRes.json()
      setSwarmData(swarm)
      setAlerts(prev => [...criticalAlerts, ...prev].slice(0, 5))
      setLoading(false)
    } catch (error) {
      console.error("Failed to fetch UAV data:", error)
    }
  }

  useEffect(() => {
    fetchData()
    const interval = setInterval(fetchData, 5000)
    return () => clearInterval(interval)
  }, [])

  if (loading) return <div className="p-8 text-center">Initializing Coordinated UAV Swarm...</div>

  return (
    <div className="container mx-auto p-6 space-y-8">
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-4xl font-bold tracking-tight">🚁 Coordinated UAV Swarm</h1>
          <p className="text-muted-foreground mt-2">Real-time autonomous mapping of all 20 Lagos LGAs</p>
        </div>
        <Badge variant="outline" className="text-green-500 animate-pulse border-green-500 py-1 px-3">
          <Activity className="w-4 h-4 mr-2" /> Live Sentinel Link
        </Badge>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <Card className="bg-blue-900/10 border-blue-500/50">
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Active UAVs</CardTitle>
            <Plane className="h-4 w-4 text-blue-500" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{swarmData.active_uavs} / {swarmData.total_uavs}</div>
            <p className="text-xs text-muted-foreground">Operating across metropolitan Lagos</p>
          </CardContent>
        </Card>

        <Card className="bg-green-900/10 border-green-500/50">
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Mapping Completion</CardTitle>
            <Activity className="h-4 w-4 text-green-500" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{(swarmData.total_mapping_completion * 100).toFixed(2)}%</div>
            <Progress value={swarmData.total_mapping_completion * 100} className="mt-2" />
          </CardContent>
        </Card>

        <Card className="bg-red-900/10 border-red-500/50">
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Critical Alerts</CardTitle>
            <AlertTriangle className="h-4 w-4 text-red-500" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-red-500">{alerts.length}</div>
            <p className="text-xs text-muted-foreground">Requiring immediate government intervention</p>
          </CardContent>
        </Card>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center">
              <MapPin className="mr-2 h-5 w-5" /> LGA Mapping Progress
            </CardTitle>
          </CardHeader>
          <CardContent className="h-[400px] overflow-y-auto">
            <div className="space-y-4">
              {Object.entries(swarmData.lga_progress).map(([lga, progress]: [string, any]) => (
                <div key={lga} className="space-y-1">
                  <div className="flex justify-between text-sm">
                    <span className="font-semibold">{lga}</span>
                    <span>{progress.toFixed(1)}%</span>
                  </div>
                  <Progress value={progress} className="h-1" />
                </div>
              ))}
            </div>
          </CardContent>
        </Card>

        <Card className="border-red-500/20">
          <CardHeader>
            <CardTitle className="flex items-center text-red-500">
              <AlertTriangle className="mr-2 h-5 w-5" /> Live Intelligence Feed
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              {alerts.length === 0 ? (
                <p className="text-muted-foreground italic">Scanning for anomalies...</p>
              ) : (
                alerts.map((alert, i) => (
                  <div key={i} className="p-4 rounded-lg bg-red-500/5 border border-red-500/10 flex gap-4">
                    <div className="bg-red-500 p-2 rounded-full h-fit mt-1">
                      <AlertTriangle className="h-4 w-4 text-white" />
                    </div>
                    <div>
                      <h4 className="font-bold text-red-500">{alert.lga}: {alert.issue}</h4>
                      <p className="text-sm">{alert.recommended_action}</p>
                      <span className="text-xs text-muted-foreground">
                        Verified by AI Swarm • {new Date(alert.timestamp * 1000).toLocaleTimeString()}
                      </span>
                    </div>
                  </div>
                ))
              )}
            </div>
            <Button className="w-full mt-6 bg-red-600 hover:bg-red-700">
              Transmit to Ministry of Works
            </Button>
          </CardContent>
        </Card>
      </div>
    </div>
  )
}
