"use client"

import { useState, useEffect } from "react"
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Progress } from "@/components/ui/progress"
import { 
    ShieldAlert, 
    Send, 
    Map as MapIcon, 
    Activity, 
    Zap,
    FileText,
    CheckCircle2
} from "lucide-react"
import { toast } from "sonner"
import type { DetectionData } from "@/lib/types"

const API_URL = "http://127.0.0.1:8000/api/v1"

interface SentinelHubProps {
    currentData: DetectionData | null
    videoId: string | null
}

export function SentinelHub({ currentData, videoId }: SentinelHubProps) {
    const [globalMap, setGlobalMap] = useState<any>(null)
    const [isDispatching, setIsDispatching] = useState(false)
    const [isGeneratingReport, setIsGeneratingReport] = useState(false)

    useEffect(() => {
        const fetchGlobalMap = async () => {
            try {
                const res = await fetch(`${API_URL}/analytics/global-map`)
                const data = await res.json()
                setGlobalMap(data)
            } catch (e) {
                console.error("Failed to fetch global map", e)
            }
        }
        fetchGlobalMap()
    }, [currentData])

    const handleDispatch = async (potholeId: number) => {
        setIsDispatching(true)
        try {
            const res = await fetch(`${API_URL}/dispatch/repair?pothole_id=${potholeId}`, { method: 'POST' })
            const data = await res.json()
            toast.success(`Unit ${data.unit_id} dispatched! ETA: ${data.eta}`, {
                icon: <Zap className="h-4 w-4 text-yellow-500" />
            })
        } catch (e) {
            toast.error("Dispatch failed")
        } finally {
            setIsDispatching(false)
        }
    }

    const handleGenerateReport = async () => {
        if (!videoId) return
        setIsGeneratingReport(true)
        try {
            const res = await fetch(`${API_URL}/city/report/${videoId}`)
            const data = await res.json()
            toast.success(`Report ${data.report_id} generated for city authorities!`, {
                description: `Recommendation: ${data.recommendation}`
            })
        } catch (e) {
            toast.error("Report generation failed")
        } finally {
            setIsGeneratingReport(false)
        }
    }

    if (!currentData) return (
        <Card className="border-dashed border-2 opacity-50">
            <CardContent className="flex flex-col items-center justify-center py-10">
                <ShieldAlert className="h-10 w-10 text-muted-foreground mb-2" />
                <p className="text-sm font-medium">Sentinel Hub Waiting for Data...</p>
            </CardContent>
        </Card>
    )

    const urgency = currentData.urgency_score || 0
    const severity = currentData.summary.severity_breakdown || { LOW: 0, MEDIUM: 0, CRITICAL: 0 }

    return (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
            {/* Urgency Gauge */}
            <Card className="col-span-1 border-indigo-500/20 bg-indigo-50/30 dark:bg-indigo-950/10">
                <CardHeader className="pb-2">
                    <CardTitle className="text-sm font-bold flex items-center gap-2">
                        <Activity className="h-4 w-4 text-indigo-500" />
                        Maintenance Urgency
                    </CardTitle>
                </CardHeader>
                <CardContent>
                    <div className="text-4xl font-black text-indigo-600 dark:text-indigo-400 mb-2">{urgency}%</div>
                    <Progress value={urgency} className="h-2 bg-indigo-200 dark:bg-indigo-900" />
                    <p className="text-[10px] text-muted-foreground mt-2">
                        {urgency > 70 ? "🔴 IMMEDIATE ACTION REQUIRED" : urgency > 40 ? "🟡 MONITORING NECESSARY" : "🟢 STABLE CONDITION"}
                    </p>
                </CardContent>
            </Card>

            {/* Global Context */}
            <Card className="col-span-1">
                <CardHeader className="pb-2">
                    <CardTitle className="text-sm font-bold flex items-center gap-2">
                        <MapIcon className="h-4 w-4 text-blue-500" />
                        Lagos Infrastructure Network
                    </CardTitle>
                </CardHeader>
                <CardContent>
                    <div className="text-2xl font-bold">{globalMap?.stats?.total_detected || 0}</div>
                    <p className="text-[10px] text-muted-foreground">Total potholes across Lagos detected by network</p>
                    <div className="mt-3 flex gap-1">
                        {[...Array(5)].map((_, i) => (
                            <div key={i} className={`h-1.5 flex-1 rounded-full ${i < 3 ? 'bg-blue-500' : 'bg-gray-200'}`} />
                        ))}
                    </div>
                </CardContent>
            </Card>

            {/* Severity Breakdown */}
            <Card className="col-span-1">
                <CardHeader className="pb-2">
                    <CardTitle className="text-sm font-bold flex items-center gap-2">
                        <ShieldAlert className="h-4 w-4 text-red-500" />
                        Hazard Breakdown
                    </CardTitle>
                </CardHeader>
                <CardContent className="space-y-2">
                    <div className="flex justify-between text-[10px]">
                        <span>Critical Hazards</span>
                        <span className="font-bold text-red-500">{severity.CRITICAL}</span>
                    </div>
                    <Progress value={(severity.CRITICAL / (currentData.summary.unique_pothole || 1)) * 100} className="h-1 bg-red-100 dark:bg-red-950" />
                    
                    <div className="flex justify-between text-[10px]">
                        <span>Medium Hazards</span>
                        <span className="font-bold text-yellow-500">{severity.MEDIUM}</span>
                    </div>
                    <Progress value={(severity.MEDIUM / (currentData.summary.unique_pothole || 1)) * 100} className="h-1 bg-yellow-100 dark:bg-yellow-950" />
                </CardContent>
            </Card>

            {/* AI Control Actions */}
            <Card className="col-span-1 border-emerald-500/20 bg-emerald-50/30 dark:bg-emerald-950/10">
                <CardHeader className="pb-2">
                    <CardTitle className="text-sm font-bold flex items-center gap-2">
                        <Zap className="h-4 w-4 text-emerald-500" />
                        Autonomous Actions
                    </CardTitle>
                </CardHeader>
                <CardContent className="flex flex-col gap-2">
                    <Button 
                        size="sm" 
                        variant="default" 
                        className="bg-emerald-600 hover:bg-emerald-700 text-[10px] h-8"
                        onClick={handleGenerateReport}
                        disabled={isGeneratingReport}
                    >
                        <FileText className="h-3 w-3 mr-1" />
                        Generate City Report
                    </Button>
                    <Button 
                        size="sm" 
                        variant="outline" 
                        className="text-[10px] h-8 border-emerald-600/50"
                        onClick={() => handleDispatch(currentData.pothole_list?.[0]?.pothole_id || 0)}
                        disabled={isDispatching || !currentData.pothole_list?.length}
                    >
                        <Send className="h-3 w-3 mr-1" />
                        Dispatch Repair Bot
                    </Button>
                </CardContent>
            </Card>
        </div>
    )
}
