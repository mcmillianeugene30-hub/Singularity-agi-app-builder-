"use client";

import { useState, useEffect } from "react";
import { Terminal, Shield, Cpu, Cloud, Settings, Play, CheckCircle, AlertCircle } from "lucide-react";

export default function SingularityDashboard() {
  const [prompt, setPrompt] = useState("");
  const [status, setStatus] = useState({
    gemini: "Active",
    groq: "Active",
    openrouter: "Active",
  });
  const [deployTarget, setDeployTarget] = useState("netlify");
  const [monitorStatus, setMonitorStatus] = useState<any[]>([]);

  useEffect(() => {
    const fetchMonitor = async () => {
      try {
        const res = await fetch("http://localhost:8000/monitor");
        const data = await res.json();
        setMonitorStatus(data);
      } catch (err) {
        console.error("Failed to fetch monitor status");
      }
    };
    fetchMonitor();
    const interval = setInterval(fetchMonitor, 10000);
    return () => clearInterval(interval);
  }, []);

  const startBuild = async () => {
    setIsBuilding(true);
    setLogs(["[*] Initializing WebSocket connection..."]);
    
    const socket = new WebSocket("ws://localhost:8000/ws/build");
    
    socket.onopen = () => {
        socket.send(JSON.stringify({ prompt, deploy: deployTarget, heal: true, docs: true }));
        setLogs(prev => [...prev, `[+] Connected. Starting build for ${deployTarget}...`]);
    };
    
    socket.onmessage = (event) => {
        const message = event.data;
        setLogs(prev => [...prev, message]);
        if (message.includes("[SUCCESS]")) {
            setIsBuilding(false);
        }
    };
    
    socket.onerror = (error) => {
        setLogs(prev => [...prev, "[!] WebSocket error occurred."]);
        setIsBuilding(false);
    };
    
    socket.onclose = () => {
        setLogs(prev => [...prev, "[*] Build connection closed."]);
        setIsBuilding(false);
    };
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
              <div className="flex items-center gap-4">
                <select 
                  value={deployTarget}
                  onChange={(e) => setDeployTarget(e.target.value)}
                  className="bg-slate-950 border border-slate-800 rounded-lg px-3 py-1.5 text-sm text-slate-300 outline-none focus:ring-1 focus:ring-indigo-500"
                >
                  <option value="netlify">Netlify (Serverless)</option>
                  <option value="railway">Railway (Full-stack)</option>
                  <option value="fly">Fly.io (Persistent)</option>
                </select>
                <p className="text-xs text-slate-500 italic">Target: {deployTarget}</p>
              </div>
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

          {/* Monitoring Dashboard */}
          <section className="bg-slate-900/50 border border-slate-800 rounded-2xl p-6 space-y-4">
            <h2 className="text-lg font-semibold flex items-center gap-2">
              <Cloud className="w-5 h-5 text-indigo-500" /> Live Deployment Health
            </h2>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              {monitorStatus.length === 0 ? (
                <p className="text-sm text-slate-600 col-span-2">No apps monitored yet.</p>
              ) : (
                monitorStatus.map((app, i) => (
                  <div key={i} className="p-4 bg-slate-950 border border-slate-800 rounded-xl flex flex-col gap-1">
                    <div className="flex justify-between items-center">
                      <span className="font-bold text-indigo-400">{app.name}</span>
                      <span className={`text-xs px-2 py-0.5 rounded-full ${app.status === 'Healthy' ? 'bg-green-500/20 text-green-400' : 'bg-red-500/20 text-red-400'}`}>
                        {app.status}
                      </span>
                    </div>
                    <a href={app.url} target="_blank" className="text-xs text-slate-500 truncate hover:text-indigo-400 transition-colors">{app.url}</a>
                    <div className="flex justify-between items-center mt-2 text-[10px] text-slate-600 font-mono">
                      <span>LATENCY: {app.latency}</span>
                      <span>LAST CHECK: {app.last_check}</span>
                    </div>
                  </div>
                ))
              )}
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
