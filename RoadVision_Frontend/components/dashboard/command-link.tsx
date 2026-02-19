"use client"

import { useState, useEffect, useRef } from "react"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Input } from "@/components/ui/input"
import { Button } from "@/components/ui/button"
import { ScrollArea } from "@/components/ui/scroll-area"
import { 
    MessageSquare, 
    Send, 
    Terminal, 
    User,
    ShieldCheck
} from "lucide-react"

const WS_URL = "ws://127.0.0.1:8000/api/v1"

interface Message {
    id: string
    user: string
    message: string
    timestamp: string
}

export function CommandLink() {
    const [messages, setMessages] = useState<Message[]>([])
    const [inputValue, setInputValue] = useState("")
    const [userName, setUserName] = useState("Field-Unit-01")
    const wsRef = useRef<WebSocket | null>(null)
    const scrollRef = useRef<HTMLDivElement>(null)

    useEffect(() => {
        const ws = new WebSocket(`${WS_URL}/ws/command-link`)
        wsRef.current = ws

        ws.onmessage = (event) => {
            const data = JSON.parse(event.data)
            if (data.type === "history") {
                setMessages(data.messages)
            } else if (data.type === "feedback") {
                setMessages(prev => [...prev, data])
            }
        }

        return () => ws.close()
    }, [])

    useEffect(() => {
        if (scrollRef.current) {
            scrollRef.current.scrollTop = scrollRef.current.scrollHeight
        }
    }, [messages])

    const sendMessage = () => {
        if (!inputValue.trim() || !wsRef.current) return
        
        wsRef.current.send(JSON.stringify({
            type: "message",
            user: userName,
            message: inputValue
        }))
        setInputValue("")
    }

    return (
        <Card className="h-[400px] flex flex-col border-indigo-500/30 shadow-lg shadow-indigo-500/10">
            <CardHeader className="py-3 border-b bg-gray-50/50 dark:bg-gray-950/50">
                <CardTitle className="text-sm font-bold flex items-center justify-between">
                    <div className="flex items-center gap-2">
                        <Terminal className="h-4 w-4 text-indigo-500" />
                        Sentinel Command Link
                    </div>
                    <div className="flex items-center gap-1 px-2 py-0.5 rounded-full bg-green-500/10 text-green-500 text-[10px] animate-pulse">
                        <div className="h-1.5 w-1.5 rounded-full bg-green-500" />
                        LIVE
                    </div>
                </CardTitle>
            </CardHeader>
            <CardContent className="flex-1 overflow-hidden p-0 flex flex-col">
                <ScrollArea className="flex-1 p-4" ref={scrollRef}>
                    <div className="space-y-4">
                        {messages.map((msg) => (
                            <div key={msg.id} className={`flex flex-col ${msg.user === "SYSTEM" ? "items-center" : "items-start"}`}>
                                {msg.user === "SYSTEM" ? (
                                    <div className="bg-indigo-500/10 text-indigo-500 text-[10px] px-3 py-1 rounded-full border border-indigo-500/20 font-bold tracking-tight">
                                        <ShieldCheck className="h-3 w-3 inline mr-1" />
                                        {msg.message}
                                    </div>
                                ) : (
                                    <div className="max-w-[80%]">
                                        <div className="flex items-center gap-1.5 mb-1">
                                            <span className="text-[10px] font-bold text-indigo-600 dark:text-indigo-400">{msg.user}</span>
                                            <span className="text-[8px] text-muted-foreground">{new Date(msg.timestamp).toLocaleTimeString()}</span>
                                        </div>
                                        <div className="bg-white dark:bg-gray-900 border border-gray-100 dark:border-gray-800 rounded-2xl rounded-tl-none px-3 py-2 text-xs shadow-sm">
                                            {msg.message}
                                        </div>
                                    </div>
                                )}
                            </div>
                        ))}
                    </div>
                </ScrollArea>
                
                <div className="p-3 border-t bg-gray-50/50 dark:bg-gray-950/50 flex gap-2">
                    <Input 
                        placeholder="Type command or feedback..." 
                        className="h-9 text-xs bg-white dark:bg-gray-900 border-gray-200"
                        value={inputValue}
                        onChange={(e) => setInputValue(e.target.value)}
                        onKeyDown={(e) => e.key === 'Enter' && sendMessage()}
                    />
                    <Button size="sm" onClick={sendMessage} className="bg-indigo-600 hover:bg-indigo-700 h-9">
                        <Send className="h-3.5 w-3.5" />
                    </Button>
                </div>
            </CardContent>
        </Card>
    )
}
