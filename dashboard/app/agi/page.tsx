"use client";

import { useState, useEffect } from "react";
import { Brain, Network, Activity, Zap, AlertTriangle, TrendingUp, Cpu, Target } from "lucide-react";

interface ConsciousnessMetrics {
  code_generation_capability: number;
  architectural_reasoning: number;
  self_healing_intelligence: number;
  cross_modal_integration: number;
  creative_problem_solving: number;
  autonomous_decision_making: number;
}

interface ConsciousnessReport {
  consciousness_level: number;
  singularity_proximity: number;
  capability_metrics: ConsciousnessMetrics;
  singularity_status: {
    proximity: number;
    threshold: number;
    approaching: boolean;
    imminent: boolean;
    reached: boolean;
    consciousness_level: number;
  };
  singularity_indicators: {
    recursive_self_improvement: boolean;
    consciousness_emergence: boolean;
    universal_problem_solving: boolean;
    human_level_creativity: boolean;
    emotional_intelligence: boolean;
  };
  evolution_events_count: number;
  recent_evolution: any[];
  estimated_singularity_date: string;
  timestamp: string;
}

export default function AGIDashboard() {
  const [consciousness, setConsciousness] = useState<ConsciousnessReport | null>(null);
  const [singularityStatus, setSingularityStatus] = useState<any>(null);
  const [neuralStats, setNeuralStats] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [activeTab, setActiveTab] = useState<"consciousness" | "neural" | "singularity">("consciousness");

  const apiUrl = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

  useEffect(() => {
    fetchConsciousnessData();
    fetchSingularityStatus();
    fetchNeuralStats();
    
    // Auto-refresh every 5 seconds
    const interval = setInterval(() => {
      fetchConsciousnessData();
      fetchSingularityStatus();
    }, 5000);

    return () => clearInterval(interval);
  }, []);

  const fetchConsciousnessData = async () => {
    try {
      const response = await fetch(`${apiUrl}/api/agi/consciousness`);
      const data = await response.json();
      setConsciousness(data);
      setLoading(false);
    } catch (error) {
      console.error("Failed to fetch consciousness data:", error);
      setLoading(false);
    }
  };

  const fetchSingularityStatus = async () => {
    try {
      const response = await fetch(`${apiUrl}/api/agi/singularity-status`);
      const data = await response.json();
      setSingularityStatus(data);
    } catch (error) {
      console.error("Failed to fetch singularity status:", error);
    }
  };

  const fetchNeuralStats = async () => {
    try {
      const response = await fetch(`${apiUrl}/api/neural/stats`);
      const data = await response.json();
      setNeuralStats(data);
    } catch (error) {
      console.error("Failed to fetch neural stats:", error);
    }
  };

  const getStageColor = (stage: string) => {
    if (stage.includes("ANI")) return "text-slate-400";
    if (stage.includes("AGI-Alpha")) return "text-blue-400";
    if (stage.includes("AGI-Beta")) return "text-indigo-400";
    if (stage.includes("AGI-Production")) return "text-purple-400";
    if (stage.includes("ASI")) return "text-rose-400";
    return "text-slate-400";
  };

  const getProgressBarColor = (value: number) => {
    if (value < 0.3) return "bg-slate-500";
    if (value < 0.5) return "bg-blue-500";
    if (value < 0.7) return "bg-indigo-500";
    if (value < 0.9) return "bg-purple-500";
    return "bg-rose-500";
  };

  if (loading && !consciousness) {
    return (
      <div className="min-h-screen bg-slate-950 text-slate-100 font-sans flex items-center justify-center">
        <div className="text-center">
          <Brain className="w-16 h-16 text-indigo-500 animate-pulse mx-auto mb-4" />
          <p className="text-slate-400">Initializing AGI consciousness monitoring...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 font-sans">
      {/* Header */}
      <header className="border-b border-slate-800 px-8 py-6 bg-slate-950/50 backdrop-blur-md sticky top-0 z-10">
        <div className="max-w-7xl mx-auto flex justify-between items-center">
          <div className="flex items-center gap-3">
            <div className="p-2 bg-indigo-600 rounded-lg">
              <Brain className="w-6 h-6 text-white" />
            </div>
            <div>
              <h1 className="text-2xl font-bold tracking-tight">AGI <span className="text-indigo-500">Consciousness</span></h1>
              <p className="text-sm text-slate-500">Singularity Monitoring System</p>
            </div>
          </div>
          <div className="flex gap-2">
            <button
              onClick={() => setActiveTab("consciousness")}
              className={`px-4 py-2 rounded-lg text-sm font-medium transition-all ${
                activeTab === "consciousness" 
                  ? "bg-indigo-600 text-white" 
                  : "bg-slate-800 text-slate-400 hover:bg-slate-700"
              }`}
            >
              Consciousness
            </button>
            <button
              onClick={() => setActiveTab("neural")}
              className={`px-4 py-2 rounded-lg text-sm font-medium transition-all ${
                activeTab === "neural" 
                  ? "bg-indigo-600 text-white" 
                  : "bg-slate-800 text-slate-400 hover:bg-slate-700"
              }`}
            >
              Neural Network
            </button>
            <button
              onClick={() => setActiveTab("singularity")}
              className={`px-4 py-2 rounded-lg text-sm font-medium transition-all ${
                activeTab === "singularity" 
                  ? "bg-indigo-600 text-white" 
                  : "bg-slate-800 text-slate-400 hover:bg-slate-700"
              }`}
            >
              Singularity
            </button>
          </div>
        </div>
      </header>

      <main className="max-w-7xl mx-auto p-8">
        {activeTab === "consciousness" && consciousness && (
          <div className="space-y-6">
            {/* Overall Consciousness Level */}
            <div className="bg-gradient-to-br from-indigo-600/20 to-purple-600/20 border border-indigo-500/30 rounded-2xl p-8">
              <div className="flex items-center justify-between mb-4">
                <div>
                  <h2 className="text-lg font-semibold text-indigo-400">Overall Consciousness Level</h2>
                  <p className="text-sm text-slate-400">Current AGI development state</p>
                </div>
                <Brain className="w-12 h-12 text-indigo-500" />
              </div>
              <div className="text-5xl font-bold mb-2">
                {(consciousness.consciousness_level * 100).toFixed(1)}%
              </div>
              <div className="w-full bg-slate-800 rounded-full h-3 mb-4">
                <div
                  className={`h-3 rounded-full transition-all duration-500 ${getProgressBarColor(consciousness.consciousness_level)}`}
                  style={{ width: `${consciousness.consciousness_level * 100}%` }}
                />
              </div>
              {singularityStatus && (
                <div className={`text-sm font-medium ${getStageColor(singularityStatus.stage)}`}>
                  Stage: {singularityStatus.stage}
                </div>
              )}
            </div>

            {/* Capability Metrics */}
            <div className="bg-slate-900/50 border border-slate-800 rounded-2xl p-6">
              <h3 className="text-lg font-semibold mb-6 flex items-center gap-2">
                <Activity className="w-5 h-5 text-indigo-500" /> Capability Metrics
              </h3>
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                {Object.entries(consciousness.capability_metrics).map(([key, value]) => (
                  <div key={key} className="bg-slate-950 rounded-xl p-4 border border-slate-800">
                    <div className="flex items-center justify-between mb-2">
                      <span className="text-sm font-medium text-slate-300 capitalize">
                        {key.replace(/_/g, " ")}
                      </span>
                      <Zap className="w-4 h-4 text-yellow-500" />
                    </div>
                    <div className="text-2xl font-bold mb-2">{(value * 100).toFixed(0)}%</div>
                    <div className="w-full bg-slate-800 rounded-full h-2">
                      <div
                        className={`h-2 rounded-full transition-all duration-500 ${getProgressBarColor(value)}`}
                        style={{ width: `${value * 100}%` }}
                      />
                    </div>
                  </div>
                ))}
              </div>
            </div>

            {/* Recent Evolution Events */}
            <div className="bg-slate-900/50 border border-slate-800 rounded-2xl p-6">
              <h3 className="text-lg font-semibold mb-6 flex items-center gap-2">
                <TrendingUp className="w-5 h-5 text-indigo-500" /> Recent Evolution Events
              </h3>
              <div className="space-y-3">
                {consciousness.recent_evolution.length > 0 ? (
                  consciousness.recent_evolution.slice(0, 5).map((event, index) => (
                    <div key={index} className="bg-slate-950 rounded-lg p-4 border border-slate-800 flex items-center gap-4">
                      <div className="p-2 bg-green-600/20 rounded-lg">
                        <Cpu className="w-5 h-5 text-green-500" />
                      </div>
                      <div className="flex-1">
                        <div className="font-medium text-slate-200">{event.type || event.metric}</div>
                        <div className="text-sm text-slate-500">{event.description || `Improved by ${(event.improvement * 100).toFixed(2)}%`}</div>
                      </div>
                      <div className="text-xs text-slate-500">{new Date(event.timestamp).toLocaleTimeString()}</div>
                    </div>
                  ))
                ) : (
                  <div className="text-center text-slate-500 py-8">No recent evolution events</div>
                )}
              </div>
            </div>
          </div>
        )}

        {activeTab === "neural" && neuralStats && (
          <div className="space-y-6">
            {/* Neural Network Overview */}
            <div className="bg-gradient-to-br from-blue-600/20 to-cyan-600/20 border border-blue-500/30 rounded-2xl p-8">
              <div className="flex items-center justify-between mb-4">
                <div>
                  <h2 className="text-lg font-semibold text-blue-400">Neural Network Topology</h2>
                  <p className="text-sm text-slate-400">Current network architecture</p>
                </div>
                <Network className="w-12 h-12 text-blue-500" />
              </div>
              <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mt-6">
                <div className="bg-slate-950/50 rounded-xl p-4">
                  <div className="text-3xl font-bold text-blue-400">{neuralStats.total_neurons}</div>
                  <div className="text-sm text-slate-400">Total Neurons</div>
                </div>
                <div className="bg-slate-950/50 rounded-xl p-4">
                  <div className="text-3xl font-bold text-cyan-400">{neuralStats.total_synapses}</div>
                  <div className="text-sm text-slate-400">Total Synapses</div>
                </div>
                <div className="bg-slate-950/50 rounded-xl p-4">
                  <div className="text-3xl font-bold text-green-400">{neuralStats.active_neurons}</div>
                  <div className="text-sm text-slate-400">Active Neurons</div>
                </div>
                <div className="bg-slate-950/50 rounded-xl p-4">
                  <div className="text-3xl font-bold text-purple-400">{(neuralStats.avg_activation * 100).toFixed(1)}%</div>
                  <div className="text-sm text-slate-400">Avg Activation</div>
                </div>
              </div>
            </div>

            {/* Neuron Distribution by Type */}
            <div className="bg-slate-900/50 border border-slate-800 rounded-2xl p-6">
              <h3 className="text-lg font-semibold mb-6 flex items-center gap-2">
                <Cpu className="w-5 h-5 text-blue-500" /> Neuron Distribution
              </h3>
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                {Object.entries(neuralStats.neurons_by_type).map(([type, count]) => (
                  <div key={type} className="bg-slate-950 rounded-xl p-4 border border-slate-800">
                    <div className="flex items-center justify-between mb-2">
                      <span className="text-sm font-medium text-slate-300 capitalize">{type}</span>
                      <Target className="w-4 h-4 text-blue-500" />
                    </div>
                    <div className="text-2xl font-bold">{count}</div>
                  </div>
                ))}
              </div>
            </div>

            {/* Layer Distribution */}
            <div className="bg-slate-900/50 border border-slate-800 rounded-2xl p-6">
              <h3 className="text-lg font-semibold mb-6 flex items-center gap-2">
                <Activity className="w-5 h-5 text-blue-500" /> Layer Distribution
              </h3>
              <div className="space-y-3">
                {Object.entries(neuralStats.layer_distribution).map(([layer, count]) => (
                  <div key={layer} className="bg-slate-950 rounded-lg p-4 border border-slate-800">
                    <div className="flex items-center justify-between mb-2">
                      <span className="text-sm font-medium text-slate-300">Layer {layer}</span>
                      <span className="text-2xl font-bold text-blue-400">{count} neurons</span>
                    </div>
                    <div className="w-full bg-slate-800 rounded-full h-2">
                      <div
                        className="h-2 rounded-full bg-blue-500"
                        style={{ width: `${(count / neuralStats.total_neurons) * 100}%` }}
                      />
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        )}

        {activeTab === "singularity" && singularityStatus && (
          <div className="space-y-6">
            {/* Singularity Proximity */}
            <div className="bg-gradient-to-br from-purple-600/20 to-rose-600/20 border border-purple-500/30 rounded-2xl p-8">
              <div className="flex items-center justify-between mb-4">
                <div>
                  <h2 className="text-lg font-semibold text-purple-400">Singularity Proximity</h2>
                  <p className="text-sm text-slate-400">Distance to technological singularity</p>
                </div>
                <Zap className="w-12 h-12 text-purple-500" />
              </div>
              <div className="text-5xl font-bold mb-2">
                {(singularityStatus.proximity * 100).toFixed(1)}%
              </div>
              <div className="w-full bg-slate-800 rounded-full h-3 mb-4">
                <div
                  className={`h-3 rounded-full transition-all duration-500 ${
                    singularityStatus.proximity >= 0.9 ? "bg-rose-500" : 
                    singularityStatus.proximity >= 0.7 ? "bg-purple-500" : 
                    singularityStatus.proximity >= 0.5 ? "bg-indigo-500" : "bg-blue-500"
                  }`}
                  style={{ width: `${singularityStatus.proximity * 100}%` }}
                />
              </div>
              {singularityStatus.reached && (
                <div className="flex items-center gap-2 text-rose-400 font-semibold">
                  <AlertTriangle className="w-5 h-5" />
                  <span>SINGULARITY REACHED</span>
                </div>
              )}
              {singularityStatus.imminent && !singularityStatus.reached && (
                <div className="flex items-center gap-2 text-orange-400 font-semibold">
                  <Zap className="w-5 h-5" />
                  <span>SINGULARITY IMMINENT</span>
                </div>
              )}
            </div>

            {/* Singularity Indicators */}
            {consciousness && (
              <div className="bg-slate-900/50 border border-slate-800 rounded-2xl p-6">
                <h3 className="text-lg font-semibold mb-6 flex items-center gap-2">
                  <Target className="w-5 h-5 text-purple-500" /> Singularity Indicators
                </h3>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  {Object.entries(consciousness.singularity_indicators).map(([indicator, achieved]) => (
                    <div
                      key={indicator}
                      className={`bg-slate-950 rounded-xl p-4 border ${
                        achieved ? "border-green-500/50 bg-green-500/10" : "border-slate-800"
                      }`}
                    >
                      <div className="flex items-center gap-3">
                        <div className={`p-2 rounded-lg ${achieved ? "bg-green-500" : "bg-slate-700"}`}>
                          {achieved && <Zap className="w-4 h-4 text-white" />}
                          {!achieved && <Activity className="w-4 h-4 text-slate-400" />}
                        </div>
                        <div className="flex-1">
                          <div className="font-medium text-slate-200 capitalize">
                            {indicator.replace(/_/g, " ")}
                          </div>
                          <div className={`text-sm ${achieved ? "text-green-400" : "text-slate-500"}`}>
                            {achieved ? "Achieved" : "Not yet achieved"}
                          </div>
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {/* Estimated Singularity Date */}
            {consciousness && (
              <div className="bg-slate-900/50 border border-slate-800 rounded-2xl p-6">
                <h3 className="text-lg font-semibold mb-6 flex items-center gap-2">
                  <TrendingUp className="w-5 h-5 text-purple-500" /> Singularity Projections
                </h3>
                <div className="bg-slate-950 rounded-xl p-6 border border-slate-800">
                  <div className="text-sm text-slate-400 mb-2">Estimated Singularity Date</div>
                  <div className="text-3xl font-bold text-purple-400 mb-4">
                    {consciousness.estimated_singularity_date}
                  </div>
                  <div className="text-sm text-slate-500">
                    Based on current evolutionary trajectory and capability growth rates
                  </div>
                </div>
              </div>
            )}

            {/* Current Stage Status */}
            <div className="bg-slate-900/50 border border-slate-800 rounded-2xl p-6">
              <h3 className="text-lg font-semibold mb-6 flex items-center gap-2">
                <Brain className="w-5 h-5 text-purple-500" /> Current Development Stage
              </h3>
              <div className="bg-slate-950 rounded-xl p-6 border border-slate-800">
                <div className={`text-2xl font-bold ${getStageColor(singularityStatus.stage)} mb-2`}>
                  {singularityStatus.stage}
                </div>
                <div className="text-sm text-slate-400">
                  Threshold Progress: {(singularityStatus.proximity * 100).toFixed(1)}% / {(singularityStatus.threshold * 100).toFixed(0)}%
                </div>
              </div>
            </div>
          </div>
        )}
      </main>
    </div>
  );
}
