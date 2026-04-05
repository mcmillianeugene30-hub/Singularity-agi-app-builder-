"use client";

import { useState, useEffect } from "react";
import { Terminal, Shield, Cpu, Cloud, Settings, Play, CheckCircle, AlertCircle, MessageSquare, Image as ImageIcon, Layout, Mic, Code, RotateCcw } from "lucide-react";

export default function SingularityDashboard() {
  const [prompt, setPrompt] = useState("");
  const [deployTarget, setDeployTarget] = useState("netlify");
  const [status, setStatus] = useState({ gemini: "Active", groq: "Active", openrouter: "Active" });
  const [logs, setLogs] = useState<string[]>([]);
  const [isBuilding, setIsBuilding] = useState(false);
  const [monitorStatus, setMonitorStatus] = useState<any[]>([]);
  
  // Advanced AI Features State
  const [reasoning, setReasoning] = useState({ explanation: "", suggestions: [] });
  const [multimodal, setMultimodal] = useState({ mockup: "", diagram: "" });
  const [liveCode, setLiveCode] = useState("");

  const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";
  const WS_URL = API_URL.replace("http", "ws");

  useEffect(() => {
    const fetchMonitor = async () => {
      try {
        const res = await fetch(`${API_URL}/monitor`);
        const data = await res.json();
        setMonitorStatus(data);
      } catch (err) { console.error("Monitor fetch failed"); }
    };
    fetchMonitor();
    const interval = setInterval(fetchMonitor, 15000);
    return () => clearInterval(interval);
  }, []);

  const startBuild = async () => {
    setIsBuilding(true);
    setLogs(["[*] Initializing WebSocket connection..."]);
    setReasoning({ explanation: "", suggestions: [] });
    setMultimodal({ mockup: "", diagram: "" });

    const socket = new WebSocket(`${WS_URL}/ws/build`);
    
    socket.onopen = () => {
        socket.send(JSON.stringify({ prompt, deploy: deployTarget, heal: true, docs: true, refine: true, lint: true }));
        setLogs(prev => [...prev, `[+] Connected. Starting autonomous build for ${deployTarget}...`]);
    };
    
    socket.onmessage = (event) => {
        try {
            const data = JSON.parse(event.data);
            if (data.type === "reasoning") setReasoning({ explanation: data.explanation, suggestions: data.suggestions });
            else if (data.type === "multimodal") setMultimodal({ mockup: data.mockup, diagram: data.diagram });
        } catch (e) {
            const message = event.data;
            setLogs(prev => [...prev, message]);
            if (message.includes("[SUCCESS]")) setIsBuilding(false);
        }
    };
    
    socket.onclose = () => {
        setLogs(prev => [...prev, "[*] Build connection closed."]);
        setIsBuilding(false);
    };
  };

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 font-sans pb-20">
      {/* Header */}
      <header className="border-b border-slate-800 px-8 py-6 flex justify-between items-center bg-slate-950/50 backdrop-blur-md sticky top-0 z-10">
        <div className="flex items-center gap-3">
          <div className="p-2 bg-indigo-600 rounded-lg"><Cpu className="w-6 h-6 text-white" /></div>
          <h1 className="text-2xl font-bold tracking-tight text-white">Singularity <span className="text-indigo-500">AGI</span></h1>
        </div>
        <div className="flex gap-4">
          <div className="flex items-center gap-2 px-4 py-1.5 bg-slate-900 border border-slate-800 rounded-full text-xs font-medium text-slate-300">
            <span className="w-2 h-2 bg-green-500 rounded-full animate-pulse"></span> SYSTEM ONLINE (PHASE 8)
          </div>
          <button className="p-2 hover:bg-slate-900 rounded-lg transition-colors"><Settings className="w-5 h-5 text-slate-400" /></button>
        </div>
      </header>

      <main className="p-8 max-w-[1600px] mx-auto grid grid-cols-12 gap-8">
        {/* Left Column: Build & Logs */}
        <div className="col-span-12 lg:col-span-7 space-y-8">
          <section className="bg-slate-900/50 border border-slate-800 rounded-2xl p-6 space-y-4 shadow-xl">
            <div className="flex justify-between items-center">
                <h2 className="text-lg font-semibold flex items-center gap-2 text-white"><Play className="w-5 h-5 text-indigo-500" /> Autonomous Build Engine</h2>
                <div className="flex gap-2">
                    <button className="p-2 bg-slate-950 border border-slate-800 rounded-lg hover:border-indigo-500 transition-all" title="Voice Command"><Mic className="w-4 h-4 text-slate-400" /></button>
                    <button className="p-2 bg-slate-950 border border-slate-800 rounded-lg hover:border-indigo-500 transition-all" title="Rollback"><RotateCcw className="w-4 h-4 text-slate-400" /></button>
                </div>
            </div>
            <textarea
              className="w-full h-32 bg-slate-950 border border-slate-800 rounded-xl p-4 text-slate-200 focus:ring-2 focus:ring-indigo-500 focus:border-transparent transition-all outline-none resize-none font-medium"
              placeholder="Describe your vision (e.g., A multi-user SaaS for real-time inventory tracking with AI-driven analytics)..."
              value={prompt}
              onChange={(e) => setPrompt(e.target.value)}
            />
            <div className="flex justify-between items-center">
              <div className="flex items-center gap-4">
                <select value={deployTarget} onChange={(e) => setDeployTarget(e.target.value)} className="bg-slate-950 border border-slate-800 rounded-lg px-3 py-1.5 text-xs text-slate-300 outline-none focus:ring-1 focus:ring-indigo-500">
                  <option value="netlify">Netlify (Serverless)</option>
                  <option value="railway">Railway (Full-stack)</option>
                  <option value="render">Render (Docker)</option>
                </select>
                <div className="flex gap-2 text-[10px] uppercase tracking-wider font-bold">
                    <span className="text-indigo-400">SELF-HEALING ON</span>
                    <span className="text-emerald-400">REFINEMENT ON</span>
                </div>
              </div>
              <button onClick={startBuild} disabled={isBuilding || !prompt} className={`px-8 py-2.5 rounded-xl font-bold flex items-center gap-2 transition-all shadow-lg ${isBuilding ? 'bg-slate-800 text-slate-500 cursor-not-allowed' : 'bg-indigo-600 hover:bg-indigo-500 text-white hover:scale-105 active:scale-95'}`}>
                {isBuilding ? 'BUILDING...' : 'LAUNCH SINGULARITY'} <Play className="w-4 h-4 fill-current" />
              </button>
            </div>
          </section>

          {/* Real-time Preview & Terminal */}
          <div className="grid grid-cols-2 gap-6">
            <section className="bg-slate-950 border border-slate-800 rounded-2xl overflow-hidden flex flex-col h-[400px] shadow-lg">
                <div className="bg-slate-900 border-b border-slate-800 px-6 py-3 flex justify-between items-center">
                    <h2 className="text-xs font-bold text-slate-400 flex items-center gap-2"><Terminal className="w-4 h-4" /> AGI TERMINAL</h2>
                    <div className="flex gap-1.5"><div className="w-2.5 h-2.5 rounded-full bg-slate-700"></div><div className="w-2.5 h-2.5 rounded-full bg-slate-700"></div><div className="w-2.5 h-2.5 rounded-full bg-slate-700"></div></div>
                </div>
                <div className="p-6 font-mono text-[13px] overflow-y-auto space-y-1 flex-1 scrollbar-hide">
                    {logs.length === 0 ? <p className="text-slate-600 italic opacity-50">Standby...</p> : logs.map((log, i) => <p key={i} className={log.includes("[SUCCESS]") ? "text-green-400 font-bold" : log.includes("[ERROR]") ? "text-red-400" : "text-slate-300"}>{log}</p>)}
                </div>
            </section>
            
            <section className="bg-slate-950 border border-slate-800 rounded-2xl overflow-hidden flex flex-col h-[400px] shadow-lg">
                <div className="bg-slate-900 border-b border-slate-800 px-6 py-3 flex justify-between items-center">
                    <h2 className="text-xs font-bold text-slate-400 flex items-center gap-2"><Code className="w-4 h-4" /> REAL-TIME PREVIEW</h2>
                    <span className="text-[10px] text-slate-600 font-mono uppercase">Live Code Gen</span>
                </div>
                <div className="p-6 font-mono text-[12px] overflow-y-auto flex-1 bg-[#0d1117] text-slate-300 scrollbar-hide">
                    <pre><code>{liveCode || "// Code will appear here during build..."}</code></pre>
                </div>
            </section>
          </div>
        </div>

        {/* Right Column: Advanced AI Features */}
        <div className="col-span-12 lg:col-span-5 space-y-6">
          {/* Reasoning & Suggestions */}
          <section className="bg-slate-900/50 border border-slate-800 rounded-2xl p-6 space-y-4 shadow-xl">
            <h2 className="font-bold flex items-center gap-2 text-white"><MessageSquare className="w-5 h-5 text-indigo-500" /> Architectural Reasoning</h2>
            <div className="p-4 bg-slate-950 border border-slate-800 rounded-xl min-h-[100px] text-sm text-slate-300 leading-relaxed overflow-y-auto max-h-[200px] scrollbar-hide">
                {reasoning.explanation || "The AGI will explain its architectural decisions here."}
            </div>
            {reasoning.suggestions.length > 0 && (
                <div className="space-y-2">
                    <p className="text-[10px] font-bold text-slate-500 uppercase tracking-widest">Predictive Suggestions</p>
                    <div className="flex flex-wrap gap-2">
                        {reasoning.suggestions.map((s, i) => <span key={i} className="px-3 py-1 bg-indigo-600/20 border border-indigo-500/30 text-indigo-400 rounded-full text-xs font-medium">+ {s}</span>)}
                    </div>
                </div>
            )}
          </section>

          {/* Visual Architect & Multi-Modal */}
          <div className="grid grid-cols-2 gap-4">
            <section className="bg-slate-900/50 border border-slate-800 rounded-2xl p-5 space-y-3 shadow-xl h-[280px] flex flex-col">
                <h3 className="text-xs font-bold flex items-center gap-2 text-white"><ImageIcon className="w-4 h-4 text-indigo-500" /> UI MOCKUP</h3>
                <div className="flex-1 bg-slate-950 rounded-xl border border-slate-800 overflow-hidden relative flex items-center justify-center">
                    {multimodal.mockup ? <img src={multimodal.mockup} className="w-full h-full object-cover opacity-80" alt="UI Mockup" /> : <p className="text-[10px] text-slate-700 text-center px-4">AI-generated visual mockup will appear here.</p>}
                </div>
            </section>
            <section className="bg-slate-900/50 border border-slate-800 rounded-2xl p-5 space-y-3 shadow-xl h-[280px] flex flex-col">
                <h3 className="text-xs font-bold flex items-center gap-2 text-white"><Layout className="w-4 h-4 text-indigo-500" /> ARCHITECTURE</h3>
                <div className="flex-1 bg-slate-950 rounded-xl border border-slate-800 p-3 font-mono text-[9px] overflow-hidden">
                    {multimodal.diagram ? <pre className="text-indigo-400">{multimodal.diagram}</pre> : <p className="text-[10px] text-slate-700 text-center mt-10 px-4 italic">Mermaid.js diagram of the system stack.</p>}
                </div>
            </section>
          </div>

          {/* Live Deployment Monitor */}
          <section className="bg-slate-900/50 border border-slate-800 rounded-2xl p-6 space-y-4 shadow-xl">
            <h2 className="font-bold flex items-center gap-2 text-white"><Cloud className="w-5 h-5 text-indigo-500" /> Production Fleet Health</h2>
            <div className="space-y-3 max-h-[300px] overflow-y-auto pr-2 scrollbar-hide">
              {monitorStatus.length === 0 ? <p className="text-xs text-slate-600 italic">No apps currently deployed.</p> : monitorStatus.map((app, i) => (
                <div key={i} className="p-4 bg-slate-950 border border-slate-800 rounded-xl flex flex-col gap-1 hover:border-indigo-500 transition-all group">
                  <div className="flex justify-between items-center">
                    <span className="font-bold text-sm text-indigo-400 group-hover:text-white transition-colors">{app.name}</span>
                    <span className={`text-[10px] px-2 py-0.5 rounded-full font-bold uppercase ${app.status === 'Healthy' ? 'bg-green-500/20 text-green-400' : 'bg-red-500/20 text-red-400'}`}>{app.status}</span>
                  </div>
                  <div className="flex justify-between items-center mt-2 text-[10px] text-slate-600 font-mono">
                    <span className="truncate w-32">{app.url}</span>
                    <span>LATENCY: {app.latency}</span>
                  </div>
                </div>
              ))}
            </div>
          </section>
        </div>
      </main>
    </div>
  );
}
