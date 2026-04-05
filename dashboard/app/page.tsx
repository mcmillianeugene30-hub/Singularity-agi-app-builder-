"use client";

import { useState, useEffect } from "react";
import { 
  Terminal, Shield, Cpu, Cloud, Settings, Play, CheckCircle, 
  AlertCircle, MessageSquare, Image as ImageIcon, Layout, 
  Mic, Code, RotateCcw, History, Star, ExternalLink, 
  Zap, Database, Lock, Box, Send
} from "lucide-react";

export default function SingularityDashboard() {
  const [prompt, setPrompt] = useState("");
  const [deployTarget, setDeployTarget] = useState("netlify");
  const [status, setStatus] = useState({ gemini: "Active", groq: "Active", openrouter: "Active" });
  const [logs, setLogs] = useState<string[]>([]);
  const [isBuilding, setIsBuilding] = useState(false);
  const [monitorStatus, setMonitorStatus] = useState<any[]>([]);
  const [projects, setProjects] = useState<any[]>([]);
  const [selectedProject, setSelectedProject] = useState<any>(null);
  
  // Advanced Build Options
  const [options, setOptions] = useState({
    heal: true,
    docs: true,
    refine: true,
    lint: true,
    reason: true,
    multimodal: true
  });

  // Advanced AI Features State (Current Build)
  const [reasoning, setReasoning] = useState({ explanation: "", suggestions: [] });
  const [multimodal, setMultimodal] = useState({ mockup: "", diagram: "" });
  const [liveCode, setLiveCode] = useState("");

  const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";
  const WS_URL = API_URL.replace("http", "ws");

  useEffect(() => {
    fetchHistory();
    fetchMonitor();
    const interval = setInterval(() => {
        fetchMonitor();
        fetchHistory();
    }, 20000);
    return () => clearInterval(interval);
  }, []);

  const fetchHistory = async () => {
    try {
      const res = await fetch(`${API_URL}/projects`);
      const data = await res.json();
      setProjects(data);
    } catch (err) { console.error("History fetch failed"); }
  };

  const fetchMonitor = async () => {
    try {
      const res = await fetch(`${API_URL}/monitor`);
      const data = await res.json();
      setMonitorStatus(data);
    } catch (err) { console.error("Monitor fetch failed"); }
  };

  const startBuild = async () => {
    setIsBuilding(true);
    setLogs(["[*] Initializing WebSocket connection..."]);
    setReasoning({ explanation: "", suggestions: [] });
    setMultimodal({ mockup: "", diagram: "" });
    setSelectedProject(null);

    const socket = new WebSocket(`${WS_URL}/ws/build`);
    
    socket.onopen = () => {
        socket.send(JSON.stringify({ prompt, deploy: deployTarget, ...options }));
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
            if (message.includes("[SUCCESS]")) {
                setIsBuilding(false);
                fetchHistory();
            }
        }
    };
    
    socket.onclose = () => {
        setLogs(prev => [...prev, "[*] Build connection closed."]);
        setIsBuilding(false);
    };
  };

  const submitFeedback = async (id: string, rating: number, feedback: string) => {
    try {
        await fetch(`${API_URL}/rate`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ project_id: id, rating, feedback })
        });
        fetchHistory();
    } catch (err) { console.error("Feedback submission failed"); }
  };

  return (
    <div className="min-h-screen bg-[#05070a] text-slate-100 font-sans selection:bg-indigo-500/30">
      {/* Sidebar: Project History */}
      <aside className="fixed left-0 top-0 bottom-0 w-72 bg-[#0a0d14] border-r border-slate-800 p-6 overflow-y-auto z-20 hidden xl:block">
        <div className="flex items-center gap-3 mb-8">
            <History className="w-5 h-5 text-indigo-500" />
            <h2 className="text-sm font-bold uppercase tracking-widest text-slate-400">Project History</h2>
        </div>
        <div className="space-y-3">
            {projects.length === 0 ? (
                <p className="text-xs text-slate-600 italic">No builds recorded yet.</p>
            ) : projects.map((p) => (
                <button 
                    key={p.id} 
                    onClick={() => setSelectedProject(p)}
                    className={`w-full text-left p-3 rounded-xl border transition-all group ${selectedProject?.id === p.id ? 'bg-indigo-600/10 border-indigo-500/50' : 'bg-slate-900/30 border-slate-800 hover:border-slate-700'}`}
                >
                    <div className="flex justify-between items-start mb-1">
                        <span className="text-xs font-bold text-slate-300 truncate w-40 group-hover:text-white">{p.name}</span>
                        <span className={`text-[9px] px-1.5 py-0.5 rounded-full uppercase font-bold ${p.status === 'live' ? 'bg-green-500/20 text-green-400' : 'bg-red-500/20 text-red-400'}`}>{p.status}</span>
                    </div>
                    <p className="text-[10px] text-slate-500 truncate">{p.prompt}</p>
                </button>
            ))}
        </div>
      </aside>

      {/* Main Content Area */}
      <div className="xl:pl-72">
        {/* Header */}
        <header className="border-b border-slate-800 px-8 py-5 flex justify-between items-center bg-[#05070a]/80 backdrop-blur-xl sticky top-0 z-10">
            <div className="flex items-center gap-3">
                <div className="p-2 bg-indigo-600 rounded-xl shadow-lg shadow-indigo-500/20"><Cpu className="w-6 h-6 text-white" /></div>
                <div>
                    <h1 className="text-xl font-black tracking-tighter text-white">SINGULARITY <span className="text-indigo-500">AGI</span></h1>
                    <p className="text-[10px] font-bold text-slate-500 tracking-[0.2em] uppercase">Phase 8: Evolutionary Architecture</p>
                </div>
            </div>
            <div className="flex gap-4">
                <div className="flex items-center gap-2 px-4 py-2 bg-slate-900/50 border border-slate-800 rounded-xl text-[11px] font-bold text-slate-300">
                    <span className="w-2 h-2 bg-green-500 rounded-full animate-pulse shadow-[0_0_8px_rgba(34,197,94,0.6)]"></span>
                    PLATFORM ONLINE
                </div>
                <button className="p-2.5 bg-slate-900/50 border border-slate-800 rounded-xl hover:bg-slate-800 transition-all group">
                    <Settings className="w-5 h-5 text-slate-400 group-hover:rotate-90 transition-transform duration-500" />
                </button>
            </div>
        </header>

        <main className="p-8 max-w-[1400px] mx-auto grid grid-cols-12 gap-8">
            {/* Build Section */}
            <div className="col-span-12 lg:col-span-8 space-y-8">
                <section className="bg-slate-900/20 border border-slate-800/50 rounded-3xl p-8 space-y-6 backdrop-blur-sm relative overflow-hidden group">
                    <div className="absolute top-0 right-0 p-8 opacity-5 group-hover:opacity-10 transition-opacity">
                        <Zap className="w-32 h-32 text-indigo-500" />
                    </div>
                    
                    <div className="flex justify-between items-center relative z-10">
                        <h2 className="text-lg font-bold flex items-center gap-2 text-white italic"><Play className="w-5 h-5 text-indigo-500 fill-current" /> Initialize Neural Build</h2>
                        <div className="flex gap-2">
                            <button className="flex items-center gap-2 px-3 py-1.5 bg-slate-950 border border-slate-800 rounded-xl text-[10px] font-bold text-slate-400 hover:border-indigo-500 transition-all"><Mic className="w-3.5 h-3.4 text-indigo-500" /> VOICE COMMAND</button>
                        </div>
                    </div>

                    <textarea
                        className="w-full h-36 bg-slate-950/50 border border-slate-800 rounded-2xl p-6 text-slate-200 focus:ring-2 focus:ring-indigo-500/50 focus:border-indigo-500 transition-all outline-none resize-none font-medium text-lg leading-relaxed placeholder:text-slate-700 relative z-10"
                        placeholder="Describe the application you want the AGI to architect, code, and deploy..."
                        value={prompt}
                        onChange={(e) => setPrompt(e.target.value)}
                    />

                    <div className="grid grid-cols-3 gap-4 relative z-10">
                        {Object.entries(options).map(([key, val]) => (
                            <button 
                                key={key}
                                onClick={() => setOptions(prev => ({...prev, [key]: !val}))}
                                className={`flex items-center justify-between px-4 py-2.5 rounded-xl border text-[10px] font-black uppercase tracking-widest transition-all ${val ? 'bg-indigo-600/10 border-indigo-500/50 text-indigo-400' : 'bg-slate-950 border-slate-800 text-slate-600'}`}
                            >
                                {key.replace(/([A-Z])/g, ' $1')}
                                {val ? <CheckCircle className="w-3 h-3" /> : <Box className="w-3 h-3" />}
                            </button>
                        ))}
                    </div>

                    <div className="flex justify-between items-center pt-4 relative z-10 border-t border-slate-800/50">
                        <div className="flex items-center gap-4">
                            <select 
                                value={deployTarget} 
                                onChange={(e) => setDeployTarget(e.target.value)} 
                                className="bg-slate-950 border border-slate-800 rounded-xl px-4 py-2.5 text-xs font-bold text-slate-300 outline-none focus:ring-2 focus:ring-indigo-500/50 appearance-none min-w-[160px] text-center"
                            >
                                <option value="netlify">NETLIFY SERVERLESS</option>
                                <option value="railway">RAILWAY FULLSTACK</option>
                                <option value="vercel">VERCEL PRODUCTION</option>
                                <option value="render">RENDER DOCKER</option>
                            </select>
                        </div>
                        <button 
                            onClick={startBuild} 
                            disabled={isBuilding || !prompt} 
                            className={`px-10 py-3.5 rounded-2xl font-black text-sm uppercase tracking-[0.15em] flex items-center gap-3 transition-all shadow-2xl ${isBuilding ? 'bg-slate-800 text-slate-500 cursor-not-allowed' : 'bg-indigo-600 hover:bg-indigo-500 text-white hover:scale-[1.02] active:scale-[0.98] shadow-indigo-500/20'}`}
                        >
                            {isBuilding ? 'Neural Link Active...' : 'Launch Singularity'} 
                            <Zap className={`w-4 h-4 ${isBuilding ? 'animate-pulse' : 'fill-current'}`} />
                        </button>
                    </div>
                </section>

                {/* Real-time AGI Engine Logs */}
                <section className="bg-slate-950 border border-slate-800 rounded-3xl overflow-hidden flex flex-col h-[500px] shadow-2xl relative group">
                    <div className="bg-[#0a0d14] border-b border-slate-800 px-8 py-4 flex justify-between items-center">
                        <div className="flex items-center gap-3">
                            <Terminal className="w-4 h-4 text-indigo-500" />
                            <h2 className="text-[11px] font-black uppercase tracking-[0.2em] text-slate-400">AGI Engine Core Terminal</h2>
                        </div>
                        <div className="flex gap-2">
                            <span className="w-2.5 h-2.5 rounded-full bg-slate-800"></span>
                            <span className="w-2.5 h-2.5 rounded-full bg-slate-800"></span>
                            <span className="w-2.5 h-2.5 rounded-full bg-slate-800"></span>
                        </div>
                    </div>
                    <div className="p-8 font-mono text-[13px] overflow-y-auto space-y-2 flex-1 bg-[#05070a] scrollbar-thin scrollbar-thumb-slate-800">
                        {logs.length === 0 ? (
                            <div className="h-full flex flex-col items-center justify-center opacity-20 grayscale scale-90 transition-all group-hover:grayscale-0 group-hover:opacity-40">
                                <Cpu className="w-16 h-16 text-indigo-500 mb-4 animate-slow-spin" />
                                <p className="text-xs font-bold uppercase tracking-widest">Waiting for neural prompt...</p>
                            </div>
                        ) : logs.map((log, i) => (
                            <div key={i} className="flex gap-4 border-l border-slate-800 pl-4 py-0.5 hover:bg-white/5 transition-colors">
                                <span className="text-slate-600 shrink-0 select-none w-10">[{i.toString().padStart(3, '0')}]</span>
                                <p className={log.includes("[SUCCESS]") ? "text-green-400 font-bold" : log.includes("[ERROR]") ? "text-red-400" : log.includes("[*]") ? "text-indigo-400" : "text-slate-300"}>{log}</p>
                            </div>
                        ))}
                    </div>
                </section>
            </div>

            {/* Right Column: Advanced AGI Status & Details */}
            <div className="col-span-12 lg:col-span-4 space-y-8">
                {/* Reasoning & Feature Predictions */}
                <section className="bg-indigo-600/5 border border-indigo-500/20 rounded-3xl p-7 space-y-6 shadow-xl">
                    <div className="flex items-center gap-3">
                        <MessageSquare className="w-5 h-5 text-indigo-500" />
                        <h2 className="font-black text-[11px] uppercase tracking-[0.2em] text-white">Architectural Reasoning</h2>
                    </div>
                    <div className="p-5 bg-slate-950 border border-slate-800/50 rounded-2xl min-h-[120px] text-[13px] text-slate-400 leading-relaxed font-medium italic">
                        {reasoning.explanation || selectedProject?.blueprint?.reasoning || "The AGI will explain its evolutionary logic here."}
                    </div>
                    {reasoning.suggestions.length > 0 && (
                        <div className="space-y-3">
                            <p className="text-[9px] font-black text-slate-500 uppercase tracking-[0.2em]">Predictive Suggestions</p>
                            <div className="flex flex-wrap gap-2">
                                {reasoning.suggestions.map((s, i) => (
                                    <span key={i} className="px-3 py-1.5 bg-indigo-600/10 border border-indigo-500/20 text-indigo-400 rounded-lg text-[10px] font-bold">+ {s}</span>
                                ))}
                            </div>
                        </div>
                    )}
                </section>

                {/* Multi-Modal Generation Visuals */}
                <div className="grid grid-cols-1 gap-6">
                    <section className="bg-slate-900/20 border border-slate-800 rounded-3xl p-6 space-y-4">
                        <h3 className="text-[10px] font-black uppercase tracking-[0.2em] flex items-center gap-2 text-white"><ImageIcon className="w-4 h-4 text-indigo-500" /> Neural UI Mockup</h3>
                        <div className="aspect-video bg-slate-950 rounded-2xl border border-slate-800 overflow-hidden flex items-center justify-center relative group">
                            {multimodal.mockup ? (
                                <img src={multimodal.mockup} className="w-full h-full object-cover opacity-80 group-hover:scale-110 transition-transform duration-700" alt="UI Mockup" />
                            ) : (
                                <div className="text-center p-6">
                                    <ImageIcon className="w-8 h-8 text-slate-800 mx-auto mb-2" />
                                    <p className="text-[9px] font-bold text-slate-700 uppercase tracking-widest">Visual Asset Standby</p>
                                </div>
                            )}
                        </div>
                    </section>

                    <section className="bg-slate-900/20 border border-slate-800 rounded-3xl p-6 space-y-4">
                        <h3 className="text-[10px] font-black uppercase tracking-[0.2em] flex items-center gap-2 text-white"><Layout className="w-4 h-4 text-indigo-500" /> System Topology</h3>
                        <div className="p-5 bg-slate-950 rounded-2xl border border-slate-800 min-h-[150px] font-mono text-[10px] overflow-x-auto text-indigo-400/80">
                            {multimodal.diagram ? <pre>{multimodal.diagram}</pre> : <p className="text-slate-800 italic">Mermaid diagram of the stack...</p>}
                        </div>
                    </section>
                </div>

                {/* Production Fleet Health */}
                <section className="bg-slate-900/20 border border-slate-800 rounded-3xl p-7 space-y-6">
                    <div className="flex justify-between items-center">
                        <h2 className="font-black text-[11px] uppercase tracking-[0.2em] flex items-center gap-2 text-white"><Cloud className="w-5 h-5 text-indigo-500" /> Production Fleet</h2>
                        <span className="text-[9px] font-bold text-slate-500 px-2 py-1 bg-slate-950 rounded-lg border border-slate-800">{monitorStatus.length} APPS</span>
                    </div>
                    <div className="space-y-4 max-h-[350px] overflow-y-auto pr-2 scrollbar-hide">
                        {monitorStatus.map((app, i) => (
                            <div key={i} className="p-5 bg-slate-950 border border-slate-800 rounded-2xl hover:border-indigo-500/50 transition-all group relative overflow-hidden">
                                <div className="absolute top-0 right-0 p-4 opacity-0 group-hover:opacity-100 transition-opacity">
                                    <ExternalLink className="w-4 h-4 text-indigo-500" />
                                </div>
                                <div className="flex justify-between items-center mb-3">
                                    <span className="font-black text-xs text-indigo-400 uppercase tracking-widest">{app.name}</span>
                                    <span className={`text-[9px] px-2 py-0.5 rounded-full font-black uppercase tracking-tighter ${app.status === 'Healthy' ? 'bg-green-500/20 text-green-400' : 'bg-red-500/20 text-red-400'}`}>{app.status}</span>
                                </div>
                                <div className="flex flex-col gap-2">
                                    <div className="flex justify-between text-[10px] font-mono text-slate-600">
                                        <span>LATENCY</span>
                                        <span className="text-slate-400 font-bold">{app.latency}</span>
                                    </div>
                                    <div className="flex justify-between text-[10px] font-mono text-slate-600">
                                        <span>DB NODES</span>
                                        <span className="text-indigo-500 font-bold">{app.tables || 0} TABLES</span>
                                    </div>
                                </div>
                            </div>
                        ))}
                    </div>
                </section>
            </div>
        </main>

        {/* Selected Project Detail / Feedback Overlay */}
        {selectedProject && (
            <div className="fixed inset-0 bg-[#05070a]/95 backdrop-blur-2xl z-50 flex items-center justify-center p-8 overflow-y-auto">
                <div className="max-w-5xl w-full bg-[#0a0d14] border border-slate-800 rounded-[40px] shadow-[0_0_100px_rgba(79,70,229,0.15)] overflow-hidden flex flex-col max-h-[90vh]">
                    <div className="p-10 border-b border-slate-800 flex justify-between items-start">
                        <div>
                            <div className="flex items-center gap-3 mb-2">
                                <span className="text-[10px] font-black uppercase tracking-[0.3em] text-indigo-500">Project Archive</span>
                                <span className="w-1.5 h-1.5 bg-slate-700 rounded-full"></span>
                                <span className="text-[10px] font-black uppercase tracking-[0.3em] text-slate-500">{new Date(selectedProject.created_at).toLocaleDateString()}</span>
                            </div>
                            <h2 className="text-4xl font-black tracking-tighter text-white uppercase">{selectedProject.name}</h2>
                        </div>
                        <button onClick={() => setSelectedProject(null)} className="p-4 bg-slate-900 rounded-full hover:bg-slate-800 text-slate-400 transition-all">&times;</button>
                    </div>
                    
                    <div className="p-10 grid grid-cols-2 gap-12 overflow-y-auto">
                        <div className="space-y-8">
                            <div>
                                <h3 className="text-xs font-black uppercase tracking-[0.2em] text-slate-500 mb-4">Original Prompt</h3>
                                <p className="text-lg text-slate-300 font-medium leading-relaxed italic">"{selectedProject.prompt}"</p>
                            </div>
                            <div className="grid grid-cols-2 gap-4">
                                <a href={selectedProject.deploy_url} target="_blank" className="flex items-center justify-center gap-3 py-4 bg-indigo-600 hover:bg-indigo-500 text-white rounded-2xl font-bold transition-all shadow-xl shadow-indigo-500/20 uppercase text-xs tracking-widest"><ExternalLink className="w-4 h-4" /> Visit Live Site</a>
                                <a href={selectedProject.github_url} target="_blank" className="flex items-center justify-center gap-3 py-4 bg-slate-900 border border-slate-800 hover:border-slate-700 text-slate-300 rounded-2xl font-bold transition-all uppercase text-xs tracking-widest"><Code className="w-4 h-4" /> Source Code</a>
                            </div>
                            <div className="p-8 bg-slate-950 rounded-3xl border border-slate-800 space-y-6">
                                <h3 className="text-xs font-black uppercase tracking-[0.2em] text-indigo-500 flex items-center gap-2"><Star className="w-4 h-4" /> Feedback Integration</h3>
                                <div className="flex gap-2">
                                    {[1,2,3,4,5].map((star) => (
                                        <button 
                                            key={star} 
                                            onClick={() => submitFeedback(selectedProject.id, star, "")}
                                            className={`p-3 rounded-xl border transition-all ${selectedProject.rating >= star ? 'bg-amber-500/10 border-amber-500/50 text-amber-500' : 'bg-slate-900 border-slate-800 text-slate-700 hover:border-slate-600'}`}
                                        >
                                            <Star className={`w-6 h-6 ${selectedProject.rating >= star ? 'fill-current' : ''}`} />
                                        </button>
                                    ))}
                                </div>
                                <div className="relative">
                                    <textarea 
                                        className="w-full h-24 bg-slate-900 border border-slate-800 rounded-2xl p-4 text-sm text-slate-300 outline-none focus:border-indigo-500 transition-all resize-none"
                                        placeholder="Add comments to help the AGI evolve..."
                                        defaultValue={selectedProject.feedback}
                                        onBlur={(e) => submitFeedback(selectedProject.id, selectedProject.rating, e.target.value)}
                                    />
                                    <button className="absolute bottom-4 right-4 text-indigo-500"><Send className="w-4 h-4" /></button>
                                </div>
                            </div>
                        </div>
                        <div className="space-y-8">
                            <div className="p-8 bg-[#05070a] rounded-3xl border border-slate-800 h-full">
                                <h3 className="text-xs font-black uppercase tracking-[0.2em] text-slate-500 mb-6 flex items-center gap-2"><Box className="w-4 h-4 text-indigo-500" /> Blueprint Metadata</h3>
                                <pre className="text-[10px] text-slate-500 overflow-x-auto font-mono scrollbar-hide">
                                    {JSON.stringify(selectedProject.blueprint, null, 2)}
                                </pre>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        )}
      </div>

      <style jsx global>{`
        @keyframes slow-spin {
            from { transform: rotate(0deg); }
            to { transform: rotate(360deg); }
        }
        .animate-slow-spin {
            animation: slow-spin 8s linear infinite;
        }
        ::-webkit-scrollbar {
            width: 6px;
        }
        ::-webkit-scrollbar-track {
            background: transparent;
        }
        ::-webkit-scrollbar-thumb {
            background: #1e293b;
            border-radius: 10px;
        }
        ::-webkit-scrollbar-thumb:hover {
            background: #334155;
        }
      `}</style>
    </div>
  );
}
