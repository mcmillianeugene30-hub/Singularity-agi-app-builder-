"use client";

import { useState, useEffect } from "react";
import { Terminal, Shield, Cpu, Cloud, Settings, Play, CheckCircle, AlertCircle, RefreshCw, Brain } from "lucide-react";

export default function SingularityDashboard() {
  const [prompt, setPrompt] = useState("");
  const [status, setStatus] = useState({
    gemini: "Active",
    groq: "Active",
    openrouter: "Active",
  });
  const [logs, setLogs] = useState<string[]>([]);
  const [isBuilding, setIsBuilding] = useState(false);
  const [connectionStatus, setConnectionStatus] = useState<"unknown" | "connected" | "disconnected">("unknown");
  const [isTestingConnection, setIsTestingConnection] = useState(false);

  const testConnection = async () => {
    setIsTestingConnection(true);
    const apiUrl = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";
    const healthUrl = apiUrl.replace(/^http/, "https") + "/health";

    try {
      const response = await fetch(healthUrl);
      if (response.ok) {
        const data = await response.json();
        setConnectionStatus("connected");
        setLogs(prev => [...prev, `[✓] Backend connected successfully`, `[✓] API URL: ${healthUrl}`, `[✓] Status: ${data.status}`]);
      } else {
        throw new Error(`HTTP ${response.status}`);
      }
    } catch (error) {
      setConnectionStatus("disconnected");
      setLogs(prev => [...prev, `[✗] Connection failed`, `[✗] API URL: ${healthUrl}`, `[✗] Error: ${error instanceof Error ? error.message : 'Unknown error'}`]);
    } finally {
      setIsTestingConnection(false);
    }
  };

  const startBuild = async () => {
    setIsBuilding(true);
    setLogs(["[*] Initializing WebSocket connection..."]);

    const apiUrl = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";
    const wsUrl = apiUrl.replace(/^http/, "ws") + "/ws/build";

    try {
      setLogs(prev => [...prev, `[*] Connecting to: ${wsUrl}`]);
      const socket = new WebSocket(wsUrl);

      socket.onopen = () => {
        socket.send(JSON.stringify({ prompt, deploy: true, heal: true }));
        setLogs(prev => [...prev, "[+] WebSocket connected. Sending build request..."]);
      };

      socket.onmessage = (event) => {
        const message = event.data;
        setLogs(prev => [...prev, message]);
        if (message.includes("[SUCCESS]") || message.includes("[FAILURE]")) {
          setIsBuilding(false);
        }
      };

      socket.onerror = (error) => {
        setLogs(prev => [...prev, "[!] WebSocket error occurred. Is the backend running?"]);
        setLogs(prev => [...prev, `[!] URL: ${wsUrl}`]);
        setIsBuilding(false);
      };

      socket.onclose = () => {
        setLogs(prev => [...prev, "[*] Build connection closed."]);
        setIsBuilding(false);
      };
    } catch (error) {
      setLogs(prev => [...prev, "[!] Failed to connect to WebSocket. Make sure the backend is running."]);
      setLogs(prev => [...prev, `[!] Error: ${error instanceof Error ? error.message : 'Unknown error'}`]);
      setLogs(prev => [...prev, `[!] URL: ${wsUrl}`]);
      setIsBuilding(false);
    }
  };

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 font-sans">
      {/* Header */}
      <header className="border-b border-slate-800 px-8 py-6 flex justify-between items-center bg-slate-950/50 backdrop-blur-md sticky top-0 z-10">
        <div className="flex items-center gap-3">
          <div className="p-2 bg-indigo-600 rounded-lg">
            <Cpu className="w-6 h-6 text-white" />
          </div>
          <h1 className="text-2xl font-bold tracking-tight">Singularity <span className="text-indigo-500">AGI</span></h1>
        </div>
        <div className="flex gap-4">
          <a
            href="/agi"
            className="flex items-center gap-2 px-3 py-1.5 bg-indigo-600 hover:bg-indigo-500 rounded-full text-sm font-medium transition-all text-white"
          >
            <Brain className="w-4 h-4" />
            AGI Consciousness
          </a>
          <button
            onClick={testConnection}
            disabled={isTestingConnection}
            className={`flex items-center gap-2 px-3 py-1.5 border rounded-full text-sm font-medium transition-all ${
              connectionStatus === "connected"
                ? "bg-green-950/30 border-green-800 text-green-400"
                : connectionStatus === "disconnected"
                ? "bg-red-950/30 border-red-800 text-red-400"
                : "bg-slate-900 border-slate-800 text-slate-400"
            }`}
          >
            {isTestingConnection ? (
              <RefreshCw className="w-4 h-4 animate-spin" />
            ) : connectionStatus === "connected" ? (
              <CheckCircle className="w-4 h-4" />
            ) : connectionStatus === "disconnected" ? (
              <AlertCircle className="w-4 h-4" />
            ) : (
              <RefreshCw className="w-4 h-4" />
            )}
            {connectionStatus === "connected" ? "Connected" : connectionStatus === "disconnected" ? "Disconnected" : isTestingConnection ? "Testing..." : "Test Connection"}
          </button>
          <div className="flex items-center gap-2 px-3 py-1 bg-slate-900 border border-slate-800 rounded-full text-sm">
            <span className="w-2 h-2 bg-green-500 rounded-full"></span>
            System Online
          </div>
          <button className="p-2 hover:bg-slate-900 rounded-lg transition-colors">
            <Settings className="w-5 h-5 text-slate-400" />
          </button>
        </div>
      </header>

      <main className="p-8 max-w-7xl mx-auto grid grid-cols-12 gap-8">
        {/* Left Column: Input & Controls */}
        <div className="col-span-12 lg:col-span-8 space-y-8">
          <section className="bg-slate-900/50 border border-slate-800 rounded-2xl p-6 space-y-4">
            <h2 className="text-lg font-semibold flex items-center gap-2">
              <Play className="w-5 h-5 text-indigo-500" /> Build a New Application
            </h2>
            <textarea
              className="w-full h-32 bg-slate-950 border border-slate-800 rounded-xl p-4 text-slate-200 focus:ring-2 focus:ring-indigo-500 focus:border-transparent transition-all outline-none resize-none"
              placeholder="Describe the app you want to build (e.g., A fitness tracker with progress charts and Supabase auth)..."
              value={prompt}
              onChange={(e) => setPrompt(e.target.value)}
            />
            <div className="flex justify-between items-center">
              <p className="text-sm text-slate-500 italic">Singularity will architect, code, heal, and deploy your app automatically.</p>
              <button 
                onClick={startBuild}
                disabled={isBuilding || !prompt}
                className={`px-6 py-2 rounded-xl font-semibold flex items-center gap-2 transition-all ${
                  isBuilding ? 'bg-slate-800 text-slate-500 cursor-not-allowed' : 'bg-indigo-600 hover:bg-indigo-500 text-white'
                }`}
              >
                {isBuilding ? 'Building...' : 'Launch App'} <Play className="w-4 h-4" />
              </button>
            </div>
          </section>

          <section className="bg-slate-950 border border-slate-800 rounded-2xl overflow-hidden flex flex-col h-[400px]">
            <div className="bg-slate-900 border-b border-slate-800 px-6 py-3 flex justify-between items-center">
              <h2 className="text-sm font-mono text-slate-400 flex items-center gap-2">
                <Terminal className="w-4 h-4" /> Real-time AGI Logs
              </h2>
              <div className="flex gap-1.5">
                <div className="w-2.5 h-2.5 rounded-full bg-slate-700"></div>
                <div className="w-2.5 h-2.5 rounded-full bg-slate-700"></div>
                <div className="w-2.5 h-2.5 rounded-full bg-slate-700"></div>
              </div>
            </div>
            <div className="p-6 font-mono text-sm overflow-y-auto space-y-1 flex-1 scrollbar-hide">
              {logs.length === 0 ? (
                <p className="text-slate-600 italic">No active build. Enter a prompt to start.</p>
              ) : (
                logs.map((log, i) => (
                  <p key={i} className={log.includes("[SUCCESS]") ? "text-green-400 font-bold" : "text-slate-300"}>
                    {log}
                  </p>
                ))
              )}
            </div>
          </section>
        </div>

        {/* Right Column: Status & Info */}
        <div className="col-span-12 lg:col-span-4 space-y-6">
          <div className="bg-slate-900/50 border border-slate-800 rounded-2xl p-6 space-y-6">
            <h2 className="font-semibold flex items-center gap-2">
              <Shield className="w-5 h-5 text-indigo-500" /> Provider Status
            </h2>
            <div className="space-y-4">
              {Object.entries(status).map(([provider, state]) => (
                <div key={provider} className="flex justify-between items-center p-3 bg-slate-950 rounded-xl border border-slate-800">
                  <div className="capitalize font-medium">{provider}</div>
                  <div className="flex items-center gap-2 text-sm text-green-400">
                    <CheckCircle className="w-4 h-4" /> {state}
                  </div>
                </div>
              ))}
            </div>
          </div>

          <div className="bg-indigo-600/10 border border-indigo-500/20 rounded-2xl p-6 space-y-4">
            <h3 className="font-semibold text-indigo-400 flex items-center gap-2">
              <Cloud className="w-5 h-5" /> 2026 Free Stack
            </h3>
            <ul className="text-sm text-slate-400 space-y-2">
              <li className="flex items-center gap-2">
                <span className="w-1.5 h-1.5 bg-indigo-500 rounded-full"></span>
                Next.js + Supabase Backend
              </li>
              <li className="flex items-center gap-2">
                <span className="w-1.5 h-1.5 bg-indigo-500 rounded-full"></span>
                Automated Netlify Deploy
              </li>
              <li className="flex items-center gap-2">
                <span className="w-1.5 h-1.5 bg-indigo-500 rounded-full"></span>
                Self-Healing AI Logic
              </li>
              <li className="flex items-center gap-2">
                <span className="w-1.5 h-1.5 bg-indigo-500 rounded-full"></span>
                Multi-Agent Specialization
              </li>
            </ul>
          </div>
        </div>
      </main>
    </div>
  );
}
