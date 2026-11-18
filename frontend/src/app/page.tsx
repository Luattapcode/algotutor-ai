"use client";

import React, { useState, useEffect } from "react";
import Editor from "@monaco-editor/react";
import axios from "axios";
import {
  Sparkles,
  Lightbulb,
  Play,
  MessageSquare,
  CheckCircle2,
  Clock,
  Cpu,
  BookOpen,
  Search,
  ExternalLink,
} from "lucide-react";

const BACKEND_URL = "http://127.0.0.1:8000";

const FEATURED_PROBLEMS = [
  { slug: "two-sum", name: "1. Two Sum (Easy)" },
  { slug: "valid-parentheses", name: "20. Valid Parentheses (Easy)" },
  { slug: "longest-substring-without-repeating-characters", name: "3. Longest Substring Without Repeating Characters (Medium)" },
  { slug: "container-with-most-water", name: "11. Container With Most Water (Medium)" },
  { slug: "lru-cache", name: "146. LRU Cache (Medium)" },
  { slug: "trapping-rain-water", name: "42. Trapping Rain Water (Hard)" },
];

export default function InterviewRoom() {
  // Problem State
  const [currentSlug, setCurrentSlug] = useState<string>("two-sum");
  const [customSlugInput, setCustomSlugInput] = useState<string>("");
  const [problemData, setProblemData] = useState<any>(null);
  const [isLoadingProblem, setIsLoadingProblem] = useState<boolean>(false);

  // Editor & Candidate State
  const [code, setCode] = useState<string>("# Loading starter code...");
  const [explanation, setExplanation] = useState<string>("");

  // Hint State
  const [currentTier, setCurrentTier] = useState<number>(0);
  const [hints, setHints] = useState<Array<{ tier: number; name: string; msg: string }>>([]);
  const [isLoadingHint, setIsLoadingHint] = useState<boolean>(false);

  // Complexity & Evaluation State
  const [complexityReport, setComplexityReport] = useState<any>(null);
  const [aiEvaluation, setAiEvaluation] = useState<any>(null);
  const [isEvaluating, setIsEvaluating] = useState<boolean>(false);

  // 1. Fetch Problem Details from Backend (LeetCode GraphQL)
  const loadProblem = async (slug: string) => {
    setIsLoadingProblem(true);
    setHints([]);
    setCurrentTier(0);
    setComplexityReport(null);
    setAiEvaluation(null);

    try {
      const res = await axios.get(`${BACKEND_URL}/api/leetcode/${slug}`);
      setProblemData(res.data);
      setCode(res.data.starter_code || "def solution():\n    pass\n");
      setCurrentSlug(slug);
    } catch (err: any) {
      alert(`Could not load problem '${slug}'. Make sure backend is running.`);
    } finally {
      setIsLoadingProblem(false);
    }
  };

  // Load Two Sum by default on startup
  useEffect(() => {
    loadProblem("two-sum");
  }, []);

  // 2. Request Next Progressive Hint
  const handleGetHint = async () => {
    setIsLoadingHint(true);
    try {
      const res = await axios.post(`${BACKEND_URL}/api/hints/next`, {
        problem_id: currentSlug,
        current_code: code,
        current_tier: currentTier,
      });

      setHints((prev) => [
        ...prev,
        { tier: res.data.tier, name: res.data.tier_name, msg: res.data.hint_message },
      ]);
      setCurrentTier(res.data.tier);
    } catch (err: any) {
      alert("Failed to fetch hint: " + err.message);
    } finally {
      setIsLoadingHint(false);
    }
  };

  // 3. Submit English Thinking-Out-Loud Explanation
  const handleEvaluateExplanation = async () => {
    if (!explanation.trim()) {
      alert("Please articulate your thought process in English first!");
      return;
    }
    setIsEvaluating(true);
    try {
      const res = await axios.post(`${BACKEND_URL}/api/evaluation/verbal-ai`, {
        problem_id: currentSlug,
        problem_title: problemData?.title || currentSlug,
        explanation_text: explanation,
      });
      setAiEvaluation(res.data.interviewer_coaching);
    } catch (err: any) {
      alert("Evaluation failed: " + err.message);
    } finally {
      setIsEvaluating(false);
    }
  };

  // 4. Analyze Big-O Complexity
  const handleAnalyzeComplexity = async () => {
    try {
      const res = await axios.post(`${BACKEND_URL}/api/complexity/analyze`, {
        code: code,
      });
      setComplexityReport(res.data);
    } catch (err: any) {
      alert("Complexity analysis failed: " + err.message);
    }
  };

  const getDifficultyBadge = (diff: string) => {
    if (diff === "Easy") return "bg-emerald-950 text-emerald-400 border-emerald-800";
    if (diff === "Medium") return "bg-amber-950 text-amber-400 border-amber-800";
    return "bg-rose-950 text-rose-400 border-rose-800";
  };

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 flex flex-col font-sans">
      {/* Top Header & Problem Selector */}
      <header className="border-b border-slate-800 bg-slate-900/60 backdrop-blur px-6 py-3 flex flex-wrap items-center justify-between gap-4">
        <div className="flex items-center gap-3">
          <div className="p-2 bg-indigo-600 rounded-lg text-white font-black text-xl tracking-wider">
            AT
          </div>
          <div>
            <h1 className="font-bold text-lg leading-tight">AlgoTutor AI</h1>
            <p className="text-xs text-slate-400">Big Tech Mock Interview Simulator & English Coach</p>
          </div>
        </div>

        {/* Dynamic LeetCode Selector Bar */}
        <div className="flex items-center gap-2">
          <select
            value={currentSlug}
            onChange={(e) => loadProblem(e.target.value)}
            className="bg-slate-900 border border-slate-700 text-xs text-slate-200 rounded-lg px-3 py-1.5 focus:outline-none focus:border-indigo-500"
          >
            {FEATURED_PROBLEMS.map((p) => (
              <option key={p.slug} value={p.slug}>
                {p.name}
              </option>
            ))}
          </select>

          {/* Custom Slug Input */}
          <div className="flex items-center bg-slate-900 border border-slate-700 rounded-lg overflow-hidden">
            <input
              type="text"
              placeholder="Custom slug (e.g. coin-change)"
              value={customSlugInput}
              onChange={(e) => setCustomSlugInput(e.target.value)}
              onKeyDown={(e) => {
                if (e.key === "Enter" && customSlugInput.trim()) {
                  loadProblem(customSlugInput.trim().toLowerCase());
                }
              }}
              className="bg-transparent px-3 py-1.5 text-xs text-slate-200 placeholder-slate-500 focus:outline-none w-44"
            />
            <button
              onClick={() => customSlugInput.trim() && loadProblem(customSlugInput.trim().toLowerCase())}
              className="p-1.5 bg-indigo-600 hover:bg-indigo-500 text-white transition"
              title="Load custom problem from LeetCode"
            >
              <Search size={14} />
            </button>
          </div>

          {problemData && (
            <span className={`px-2.5 py-1 text-xs rounded-full border font-semibold ${getDifficultyBadge(problemData.difficulty)}`}>
              {problemData.difficulty}
            </span>
          )}
        </div>
      </header>

      {/* Main Split Layout */}
      <main className="flex-1 grid grid-cols-1 lg:grid-cols-2 gap-4 p-4 overflow-hidden">
        {/* Left Column: Problem, Thinking Out Loud, & Hints */}
        <div className="flex flex-col gap-4 overflow-y-auto pr-2">
          {/* Problem Card */}
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 shadow-sm">
            <div className="flex items-center justify-between mb-2">
              <div className="flex items-center gap-2 text-indigo-400 font-semibold">
                <BookOpen size={18} />
                <h2>{problemData?.title || "Loading Problem..."}</h2>
              </div>
              <a
                href={`https://leetcode.com/problems/${currentSlug}/`}
                target="_blank"
                rel="noreferrer"
                className="text-slate-400 hover:text-indigo-400 text-xs flex items-center gap-1 transition"
              >
                LeetCode <ExternalLink size={12} />
              </a>
            </div>

            {/* Problem HTML Description */}
            <div className="text-xs text-slate-300 leading-relaxed max-h-48 overflow-y-auto pr-1 space-y-2 border-t border-slate-800/80 pt-3">
              {isLoadingProblem ? (
                <p className="text-slate-400 italic">Fetching problem details from LeetCode...</p>
              ) : problemData?.content_html ? (
                <div
                  className="prose prose-invert prose-xs max-w-none"
                  dangerouslySetInnerHTML={{ __html: problemData.content_html }}
                />
              ) : (
                <p>{problemData?.description}</p>
              )}
            </div>
          </div>

          {/* Thinking Out Loud (English Articulation Coach) */}
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 shadow-sm">
            <div className="flex items-center justify-between mb-2">
              <div className="flex items-center gap-2 text-pink-400 font-semibold">
                <MessageSquare size={18} />
                <h2>Thinking Out Loud (English Articulation)</h2>
              </div>
              <span className="text-xs text-slate-400">Explain your intuition in English first</span>
            </div>

            <textarea
              value={explanation}
              onChange={(e) => setExplanation(e.target.value)}
              placeholder="e.g. To avoid an O(N^2) brute force check, I will iterate through the array once and store seen elements in a hash map..."
              className="w-full h-20 bg-slate-950 border border-slate-800 rounded-lg p-3 text-sm text-slate-200 placeholder-slate-500 focus:outline-none focus:border-indigo-500 transition resize-none mb-3"
            />

            <button
              onClick={handleEvaluateExplanation}
              disabled={isEvaluating}
              className="w-full py-2 bg-gradient-to-r from-pink-600 to-indigo-600 hover:from-pink-500 hover:to-indigo-500 text-white font-medium text-sm rounded-lg flex items-center justify-center gap-2 transition disabled:opacity-50"
            >
              <Sparkles size={16} />
              {isEvaluating ? "Analyzing Communication..." : "Evaluate My English Explanation"}
            </button>

            {/* AI Coaching Output */}
            {aiEvaluation && (
              <div className="mt-4 p-4 bg-slate-950 border border-indigo-900/60 rounded-lg text-xs space-y-2">
                <div className="flex items-center gap-2 text-indigo-400 font-bold uppercase tracking-wider">
                  <CheckCircle2 size={14} /> Interviewer Feedback
                </div>
                <div className="text-slate-300 whitespace-pre-line leading-relaxed">
                  {aiEvaluation}
                </div>
              </div>
            )}
          </div>

          {/* Progressive Hint Timeline */}
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 shadow-sm flex-1">
            <div className="flex items-center justify-between mb-3">
              <div className="flex items-center gap-2 text-amber-400 font-semibold">
                <Lightbulb size={18} />
                <h2>Socratic Progressive Hints</h2>
              </div>
              <button
                onClick={handleGetHint}
                disabled={isLoadingHint || currentTier >= 4}
                className="px-3 py-1.5 bg-amber-600 hover:bg-amber-500 text-white text-xs font-semibold rounded-lg flex items-center gap-1.5 transition disabled:opacity-50"
              >
                <Sparkles size={14} />
                {isLoadingHint ? "Thinking..." : currentTier >= 4 ? "Max Tier Reached" : "Request Hint"}
              </button>
            </div>

            {hints.length === 0 ? (
              <p className="text-xs text-slate-500 italic">No hints unlocked yet. Try solving it independently first!</p>
            ) : (
              <div className="space-y-3">
                {hints.map((h, idx) => (
                  <div key={idx} className="p-3 bg-slate-950 border border-slate-800 rounded-lg text-xs space-y-1">
                    <span className="text-[10px] font-bold tracking-wider uppercase px-1.5 py-0.5 bg-amber-950 text-amber-400 border border-amber-800 rounded">
                      Level {h.tier}: {h.name}
                    </span>
                    <p className="text-slate-300 mt-1 leading-relaxed">{h.msg}</p>
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>

        {/* Right Column: Monaco Code Editor & Complexity Profiler */}
        <div className="flex flex-col gap-4">
          {/* Code Editor Container */}
          <div className="flex-1 bg-slate-900 border border-slate-800 rounded-xl overflow-hidden flex flex-col shadow-sm">
            <div className="bg-slate-900 px-4 py-2 border-b border-slate-800 flex items-center justify-between">
              <span className="text-xs font-medium text-slate-400">solution.py (Python 3)</span>
              <button
                onClick={handleAnalyzeComplexity}
                className="px-3 py-1 bg-emerald-600 hover:bg-emerald-500 text-white text-xs font-semibold rounded-md flex items-center gap-1.5 transition"
              >
                <Play size={12} fill="currentColor" />
                Analyze Complexity (O(N))
              </button>
            </div>

            {/* Monaco Editor */}
            <div className="flex-1 min-h-[350px]">
              <Editor
                height="100%"
                defaultLanguage="python"
                theme="vs-dark"
                value={code}
                onChange={(val) => setCode(val || "")}
                options={{
                  fontSize: 14,
                  minimap: { enabled: false },
                  scrollBeyondLastLine: false,
                  automaticLayout: true,
                }}
              />
            </div>
          </div>

          {/* Complexity Report Card */}
          {complexityReport && (
            <div className="bg-slate-900 border border-slate-800 rounded-xl p-4 shadow-sm space-y-2">
              <div className="flex items-center gap-2 text-emerald-400 font-semibold text-sm">
                <Cpu size={16} />
                <h3>Static AST Complexity Profile</h3>
              </div>
              <div className="grid grid-cols-2 gap-3 text-xs">
                <div className="p-2.5 bg-slate-950 rounded-lg border border-slate-800">
                  <span className="text-slate-400 flex items-center gap-1"><Clock size={12} /> Time Complexity</span>
                  <p className="font-bold text-amber-400 text-sm mt-0.5">{complexityReport.estimated_time_complexity}</p>
                </div>
                <div className="p-2.5 bg-slate-950 rounded-lg border border-slate-800">
                  <span className="text-slate-400 flex items-center gap-1"><Cpu size={12} /> Space Complexity</span>
                  <p className="font-bold text-emerald-400 text-sm mt-0.5">{complexityReport.estimated_space_complexity}</p>
                </div>
              </div>
              <p className="text-xs text-slate-400 bg-slate-950 p-2 rounded-lg border border-slate-800 leading-relaxed">
                {complexityReport.explanation}
              </p>
            </div>
          )}
        </div>
      </main>
    </div>
  );
}