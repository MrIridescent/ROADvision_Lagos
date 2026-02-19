"use client"

import { useState, useEffect } from "react"
import { SidebarNavigation } from "@/components/sidebar-navigation"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Globe, MapPin, AlertCircle, ShieldCheck, Activity } from "lucide-react"

const API_URL = "http://127.0.0.1:8000/api/v1"

export default function SatelliteSentinelPage() {
    const [cityHealth, setCityHealth] = useState<any>(null)
    const [isLoading, setIsLoading] = useState(true)

    useEffect(() => {
        const fetchCityHealth = async () => {
            try {
                const res = await fetch(`${API_URL}/satellite/city-health`)
                const data = await res.json()
                setCityHealth(data)
            } catch (e) {
                console.error("Failed to fetch satellite health", e)
            } finally {
                setIsLoading(false)
            }
        }
        fetchCityHealth()
    }, [])

    return (
        <div className="min-h-screen bg-slate-50 dark:bg-slate-950">
            <SidebarNavigation />
            <main className="ml-20 p-8">
                <header className="mb-12">
                    <h1 className="text-4xl font-black bg-gradient-to-r from-indigo-500 to-blue-600 bg-clip-text text-transparent mb-2">
                        Lagos Satellite Sentinel
                    </h1>
                    <p className="text-slate-500 dark:text-slate-400 font-medium">
                        Macro-scale Road Degradation Analysis | Specialized for Lagos State Infrastructure
                    </p>
                </header>

                <div className="grid grid-cols-1 lg:grid-cols-3 gap-8 mb-12">
                    <Card className="border-none shadow-xl bg-gradient-to-br from-indigo-600 to-blue-700 text-white">
                        <CardHeader>
                            <CardTitle className="flex items-center gap-2 text-white/90">
                                <Activity className="h-5 w-5" /> City Health Index
                            </CardTitle>
                        </CardHeader>
                        <CardContent>
                            <div className="text-6xl font-black mb-2">
                                {isLoading ? "..." : cityHealth?.average_infrastructure_score}%
                            </div>
                            <p className="text-white/70 text-sm font-medium uppercase tracking-widest">Aggregate Infrastructure Integrity</p>
                        </CardContent>
                    </Card>

                    <Card className="border-none shadow-xl bg-white dark:bg-slate-900">
                        <CardHeader>
                            <CardTitle className="flex items-center gap-2 text-indigo-500">
                                <Globe className="h-5 w-5" /> Macro Failures
                            </CardTitle>
                        </CardHeader>
                        <CardContent>
                            <div className="text-6xl font-black mb-2 text-slate-900 dark:text-white">
                                {isLoading ? "..." : cityHealth?.total_macro_failures}
                            </div>
                            <p className="text-slate-400 text-sm font-medium uppercase tracking-widest">Detected Road Failures via Satellite</p>
                        </CardContent>
                    </Card>

                    <Card className="border-none shadow-xl bg-white dark:bg-slate-900">
                        <CardHeader>
                            <CardTitle className="flex items-center gap-2 text-emerald-500">
                                <ShieldCheck className="h-5 w-5" /> Active Monitors
                            </CardTitle>
                        </CardHeader>
                        <CardContent>
                            <div className="text-6xl font-black mb-2 text-slate-900 dark:text-white">5</div>
                            <p className="text-slate-400 text-sm font-medium uppercase tracking-widest">Key Lagos Regions under Surveillance</p>
                        </CardContent>
                    </Card>
                </div>

                <div className="grid grid-cols-1 gap-8">
                    <Card className="border-none shadow-xl bg-white dark:bg-slate-900">
                        <CardHeader>
                            <CardTitle>Regional Infrastructure Breakdown</CardTitle>
                        </CardHeader>
                        <CardContent>
                            <div className="space-y-6">
                                {isLoading ? (
                                    <div className="h-48 flex items-center justify-center text-slate-400">Loading Lagos Regional Data...</div>
                                ) : (
                                    Object.entries(cityHealth?.regional_breakdown || {}).map(([name, scan]: [string, any]) => (
                                        <div key={name} className="p-6 rounded-2xl bg-slate-50 dark:bg-slate-800/50 border border-slate-100 dark:border-slate-800 flex flex-col md:flex-row md:items-center justify-between gap-6">
                                            <div>
                                                <h3 className="text-xl font-bold flex items-center gap-2 mb-1">
                                                    <MapPin className="h-4 w-4 text-indigo-500" /> {name}
                                                </h3>
                                                <p className="text-xs text-slate-400 font-mono">LAT: {scan.coordinates.lat} | LON: {scan.coordinates.lon}</p>
                                            </div>
                                            
                                            <div className="flex-1 max-w-md">
                                                <div className="flex justify-between mb-2 text-xs font-bold text-slate-500">
                                                    <span>Infrastructure Score</span>
                                                    <span>{scan.infrastructure_score}%</span>
                                                </div>
                                                <div className="w-full bg-slate-200 dark:bg-slate-700 h-2 rounded-full overflow-hidden">
                                                    <div 
                                                        className={`h-full ${scan.infrastructure_score < 40 ? 'bg-red-500' : 'bg-emerald-500'}`} 
                                                        style={{width: `${scan.infrastructure_score}%`}}
                                                    ></div>
                                                </div>
                                            </div>

                                            <div className="flex items-center gap-4">
                                                <div className="px-4 py-2 rounded-xl bg-indigo-500/10 text-indigo-500 text-sm font-bold border border-indigo-500/20">
                                                    {scan.failures_detected.length} Failures Detected
                                                </div>
                                                {scan.failures_detected.some((f: any) => f.severity === "CRITICAL") && (
                                                    <div className="flex items-center gap-1 text-red-500 text-xs font-black animate-pulse">
                                                        <AlertCircle className="h-4 w-4" /> CRITICAL
                                                    </div>
                                                )}
                                            </div>
                                        </div>
                                    ))
                                )}
                            </div>
                        </CardContent>
                    </Card>
                </div>

                <footer className="mt-16 text-center text-slate-400 text-sm font-medium">
                    ROADvision_Lagos | Created by David Akpoviroro Oke (MrIridescent)
                </footer>
            </main>
        </div>
    )
}
