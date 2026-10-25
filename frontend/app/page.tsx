"use client";

import React, { useState } from "react";
import { ShieldCheck, AlertTriangle, Cpu, DollarSign, Send, RefreshCw } from "lucide-react";
import axios from "axios";

const BACKEND_URL = "https://llm-finops-gateway.onrender.com";

interface GuardrailResponse {
  status: string;
  is_safe: boolean;
  token_count?: number;
  estimated_cost?: number;
  violation_reason?: string;
  analyzed_prompt?: string;
}

export default function FinOpsGatewayDashboard() {
  const [prompt, setPrompt] = useState<string>("");
  const [loading, setLoading] = useState<boolean>(false);
  const [result, setResult] = useState<GuardrailResponse | null>(null);
  const [error, setError] = useState<string | null>(null);

  const handleAnalyze = async () => {
    if (!prompt.trim()) return;

    setLoading(true);
    setError(null);
    setResult(null);

    try {
      const response = await axios.post(
        `${BACKEND_URL}/guardrail`,
        { prompt: prompt },
        {
          headers: { "Content-Type": "application/json" },
          timeout: 45000,
        }
      );

      setResult(response.data);
    } catch (err: any) {
      if (err.code === "ECONNABORTED") {
        setError("⏱️ Render server cold-start in progress. Please retry in 20 seconds.");
      } else {
        setError(err.response?.data?.message || "Failed to connect to LLM FinOps Gateway.");
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="min-h-screen bg-slate-950 text-slate-100 p-8 font-sans">
      <div className="max-w-4xl mx-auto space-y-8">
        {/* Header Section */}
        <header className="border-b border-slate-800 pb-6 flex items-center justify-between">
          <div>
            <h1 className="text-3xl font-extrabold tracking-tight flex items-center gap-3 text-indigo-400">
              <ShieldCheck className="w-8 h-8 text-indigo-500" />
              LLM FinOps & Guardrail Gateway
            </h1>
            <p className="text-slate-400 text-sm mt-1">
              Enterprise Pre-Flight Cost Estimation & Prompt Security Inspection
            </p>
          </div>
          <span className="px-3 py-1 bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 text-xs font-semibold rounded-full flex items-center gap-1.5">
            <span className="w-2 h-2 rounded-full bg-emerald-500 animate-pulse"></span>
            Render API Live
          </span>
        </header>

        {/* Input Form Section */}
        <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 shadow-xl space-y-4">
          <label className="block text-sm font-medium text-slate-300">
            Enter Proposed LLM Prompt / Query:
          </label>
          <textarea
            rows={4}
            value={prompt}
            onChange={(e) => setPrompt(e.target.value)}
            placeholder="e.g., Explain quantum computing, or analyze this dataset..."
            className="w-full bg-slate-950 border border-slate-800 rounded-lg p-4 text-slate-200 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent resize-none placeholder:text-slate-600"
          />

          <button
            onClick={handleAnalyze}
            disabled={loading || !prompt.trim()}
            className="w-full py-3 bg-indigo-600 hover:bg-indigo-500 disabled:opacity-50 disabled:cursor-not-allowed text-white font-semibold rounded-lg flex items-center justify-center gap-2 transition-all shadow-lg shadow-indigo-600/20"
          >
            {loading ? (
              <>
                <RefreshCw className="w-5 h-5 animate-spin" />
                Inspecting Guardrails & Calculating Cost...
              </>
            ) : (
              <>
                <Send className="w-5 h-5" />
                Analyze Prompt
              </>
            )}
          </button>
        </div>

        {/* Error Handling UI */}
        {error && (
          <div className="p-4 bg-rose-500/10 border border-rose-500/30 rounded-lg flex items-center gap-3 text-rose-400 text-sm">
            <AlertTriangle className="w-5 h-5 shrink-0" />
            <p>{error}</p>
          </div>
        )}

        {/* Result Dashboard Cards */}
        {result && (
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            {/* Safety Guardrail Status Card */}
            <div
              className={`p-5 rounded-xl border ${
                result.is_safe
                  ? "bg-emerald-500/5 border-emerald-500/20"
                  : "bg-rose-500/5 border-rose-500/20"
              }`}
            >
              <div className="flex items-center gap-2 text-xs font-semibold text-slate-400 uppercase tracking-wider mb-2">
                <ShieldCheck className="w-4 h-4" /> Safety Status
              </div>
              <div
                className={`text-xl font-bold ${
                  result.is_safe ? "text-emerald-400" : "text-rose-400"
                }`}
              >
                {result.is_safe ? "PASSED (Safe)" : "BLOCKED (Violation)"}
              </div>
              {result.violation_reason && (
                <p className="text-xs text-rose-300 mt-2">{result.violation_reason}</p>
              )}
            </div>

            {/* Token Metrics Card */}
            <div className="p-5 bg-slate-900 border border-slate-800 rounded-xl">
              <div className="flex items-center gap-2 text-xs font-semibold text-slate-400 uppercase tracking-wider mb-2">
                <Cpu className="w-4 h-4 text-indigo-400" /> Token Count
              </div>
              <div className="text-xl font-bold text-slate-100">
                {result.token_count ?? "N/A"}{" "}
                <span className="text-xs text-slate-500 font-normal">tokens</span>
              </div>
            </div>

            {/* FinOps Cost Estimation Card */}
            <div className="p-5 bg-slate-900 border border-slate-800 rounded-xl">
              <div className="flex items-center gap-2 text-xs font-semibold text-slate-400 uppercase tracking-wider mb-2">
                <DollarSign className="w-4 h-4 text-amber-400" /> Estimated Cost
              </div>
              <div className="text-xl font-bold text-amber-400">
                ${result.estimated_cost?.toFixed(6) ?? "0.000000"}
              </div>
            </div>
          </div>
        )}
      </div>
    </main>
  );
}