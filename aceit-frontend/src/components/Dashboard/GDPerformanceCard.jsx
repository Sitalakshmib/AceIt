import React, { useState, useEffect } from 'react';
import {
  LineChart, Line, XAxis, YAxis, Tooltip, ResponsiveContainer,
  ReferenceLine
} from 'recharts';
import { MessageSquare, TrendingUp, AlertCircle, CheckCircle, Loader2, Calendar } from 'lucide-react';
import { analyticsAPI } from '../../services/api';

/* ------------------------------------------------------------------ */
/* Custom Tooltip for the sparkline                                     */
/* ------------------------------------------------------------------ */
const SparkTooltip = ({ active, payload }) => {
  if (!active || !payload?.length) return null;
  const d = payload[0]?.payload;
  return (
    <div className="bg-white border border-violet-100 rounded-xl shadow-lg p-3 text-xs max-w-[180px]">
      <p className="font-bold text-violet-700 truncate">{d?.topic}</p>
      <p className="text-gray-500">{d?.date}</p>
      <div className="mt-1 space-y-0.5">
        <p className="text-gray-700">Overall: <span className="font-bold">{d?.overall_score}/10</span></p>
        <p className="text-gray-500">Clarity: {d?.clarity_score} · Coherence: {d?.coherence_score} · Relevance: {d?.relevance_score}</p>
      </div>
    </div>
  );
};

/* ------------------------------------------------------------------ */
/* Dimension bar (mini visual)                                          */
/* ------------------------------------------------------------------ */
const DimensionBar = ({ label, score, color }) => {
  const pct = Math.min(100, (score / 10) * 100);
  return (
    <div>
      <div className="flex justify-between items-center mb-1">
        <span className="text-xs font-semibold text-gray-500">{label}</span>
        <span className="text-xs font-black text-gray-800">{score.toFixed(1)}<span className="text-gray-400">/10</span></span>
      </div>
      <div className="w-full h-2 bg-gray-100 rounded-full overflow-hidden">
        <div
          className={`h-full rounded-full transition-all duration-1000 ${color}`}
          style={{ width: `${pct}%` }}
        />
      </div>
    </div>
  );
};

/* ------------------------------------------------------------------ */
/* Main Component                                                        */
/* ------------------------------------------------------------------ */
const GDPerformanceCard = () => {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetch = async () => {
      try {
        const res = await analyticsAPI.getGDAnalytics(30);
        setData(res.data?.data ?? null);
      } catch (e) {
        console.error('[GDPerformanceCard] fetch error:', e);
        setError('Could not load GD data.');
      } finally {
        setLoading(false);
      }
    };
    fetch();
  }, []);

  /* ── Loading ── */
  if (loading) {
    return (
      <div className="bg-white rounded-[2.5rem] shadow-xl border border-gray-100 p-8 flex items-center justify-center min-h-[280px]">
        <Loader2 className="h-8 w-8 text-violet-500 animate-spin" />
      </div>
    );
  }

  /* ── Error ── */
  if (error) {
    return (
      <div className="bg-white rounded-[2.5rem] shadow-xl border border-red-100 p-8 flex items-center justify-center min-h-[280px]">
        <div className="text-center">
          <AlertCircle className="h-8 w-8 text-red-400 mx-auto mb-2" />
          <p className="text-sm text-gray-500">{error}</p>
        </div>
      </div>
    );
  }

  /* ── No Data State ── */
  if (!data?.has_data) {
    return (
      <div className="bg-white rounded-[2.5rem] shadow-xl border border-gray-100 p-8 flex flex-col min-h-[280px] relative overflow-hidden">
        {/* Decorative blob */}
        <div className="absolute -top-10 -right-10 w-40 h-40 bg-violet-50 rounded-full opacity-60 pointer-events-none" />
        <div className="relative z-10 flex flex-col h-full">
          <div className="flex justify-between items-start mb-6">
            <div className="p-4 rounded-2xl bg-gradient-to-br from-violet-500 to-purple-600 text-white shadow-lg">
              <MessageSquare className="h-6 w-6" />
            </div>
            <span className="text-xs font-black uppercase tracking-wider px-3 py-1 rounded-full bg-gray-100 text-gray-400">
              No Data
            </span>
          </div>
          <h3 className="text-xl font-black text-gray-900 mb-1">GD Practice</h3>
          <p className="text-sm text-gray-500 mb-6 font-medium">0 sessions completed</p>
          <div className="mt-auto text-center py-8 bg-violet-50/50 rounded-2xl border border-dashed border-violet-200">
            <MessageSquare className="h-10 w-10 text-violet-300 mx-auto mb-2" />
            <p className="text-sm text-gray-500 font-medium">Complete your first GD session<br />to see analytics here.</p>
          </div>
        </div>
      </div>
    );
  }

  /* ── Score colour helper ── */
  const scoreColor = (s) =>
    s >= 7.5 ? 'text-emerald-600' : s >= 6 ? 'text-amber-500' : 'text-red-500';

  const levelLabel = (s) =>
    s >= 7.5 ? 'Good' : s >= 6 ? 'Moderate' : 'Low';

  const levelBadgeClass = (s) =>
    s >= 7.5
      ? 'bg-green-100 text-green-600'
      : s >= 6
      ? 'bg-orange-100 text-orange-600'
      : 'bg-gray-100 text-gray-400';

  const lastDate = data.last_practiced
    ? new Date(data.last_practiced).toLocaleDateString(undefined, { month: 'short', day: 'numeric', year: 'numeric' })
    : '—';

  return (
    <div className="bg-white rounded-[2.5rem] shadow-xl shadow-gray-100 border border-gray-100 p-8 flex flex-col relative overflow-hidden hover:scale-[1.02] transition-all duration-300">
      {/* Decorative blob */}
      <div className="absolute -top-10 -right-10 w-48 h-48 bg-violet-50 rounded-full opacity-50 pointer-events-none" />

      <div className="relative z-10 flex flex-col h-full">

        {/* ── Card Header ── */}
        <div className="flex justify-between items-start mb-6">
          <div className="p-4 rounded-2xl bg-gradient-to-br from-violet-500 to-purple-600 text-white shadow-lg">
            <MessageSquare className="h-6 w-6" />
          </div>
          <span className={`text-xs font-black uppercase tracking-wider px-3 py-1 rounded-full ${levelBadgeClass(data.average_score)}`}>
            {levelLabel(data.average_score)}
          </span>
        </div>

        <h3 className="text-xl font-black text-gray-900 mb-1">GD Practice</h3>
        <p className="text-sm text-gray-500 mb-5 font-medium">
          {data.total_sessions} session{data.total_sessions !== 1 ? 's' : ''} completed
          {data.sessions_in_window < data.total_sessions && (
            <span className="text-xs text-gray-400 ml-1">({data.sessions_in_window} in last {data.days_window}d)</span>
          )}
        </p>

        {/* ── Avg Score Hero ── */}
        <div className="flex items-end gap-3 mb-6">
          <span className={`text-5xl font-black leading-none ${scoreColor(data.average_score)}`}>
            {data.average_score.toFixed(1)}
          </span>
          <span className="text-gray-400 font-bold mb-1">/10 avg</span>
          <div className="ml-auto flex items-center gap-1 text-xs text-gray-400 font-semibold">
            <Calendar className="h-3.5 w-3.5" />
            {lastDate}
          </div>
        </div>

        {/* ── Dimension Bars ── */}
        <div className="space-y-3 mb-6">
          <DimensionBar label="Clarity" score={data.average_clarity} color="bg-gradient-to-r from-sky-400 to-blue-500" />
          <DimensionBar label="Coherence" score={data.average_coherence} color="bg-gradient-to-r from-violet-400 to-purple-500" />
          <DimensionBar label="Relevance" score={data.average_relevance} color="bg-gradient-to-r from-fuchsia-400 to-pink-500" />
        </div>

        {/* ── Weakest Dimension Insight ── */}
        {data.weakest_dimension && (
          <div className="flex items-start gap-2 bg-amber-50 border border-amber-100 rounded-2xl px-4 py-3 mb-6">
            <AlertCircle className="h-4 w-4 text-amber-500 mt-0.5 flex-shrink-0" />
            <p className="text-xs text-amber-700 font-medium leading-snug">
              <span className="font-black">{data.weakest_dimension}</span> is your weakest dimension.
              Focus on structured arguments to improve it.
            </p>
          </div>
        )}

        {/* ── Score Trend Sparkline ── */}
        {data.trend.length > 1 && (
          <div className="mb-6">
            <p className="text-xs font-bold text-gray-400 uppercase tracking-widest mb-2 flex items-center gap-1">
              <TrendingUp className="h-3.5 w-3.5" /> Score Trend
            </p>
            <div className="h-20">
              <ResponsiveContainer width="100%" height="100%">
                <LineChart data={data.trend}>
                  <XAxis dataKey="date" hide />
                  <YAxis domain={[0, 10]} hide />
                  <Tooltip content={<SparkTooltip />} />
                  <ReferenceLine y={7.5} stroke="#d1d5db" strokeDasharray="4 4" />
                  <Line
                    type="monotone"
                    dataKey="overall_score"
                    stroke="#8b5cf6"
                    strokeWidth={2.5}
                    dot={{ r: 3, fill: '#8b5cf6', strokeWidth: 0 }}
                    activeDot={{ r: 5 }}
                  />
                </LineChart>
              </ResponsiveContainer>
            </div>
          </div>
        )}

        {/* ── Top Topics ── */}
        {data.topic_breakdown.length > 0 && (
          <div className="mb-6">
            <p className="text-xs font-bold text-gray-400 uppercase tracking-widest mb-3">Top Topics</p>
            <div className="space-y-2">
              {data.topic_breakdown.slice(0, 3).map((t, i) => (
                <div key={i} className="flex items-center justify-between text-xs bg-gray-50 rounded-xl px-3 py-2">
                  <span className="font-medium text-gray-700 truncate max-w-[65%]">{t.topic}</span>
                  <span className="font-black text-violet-600 flex-shrink-0">{t.avg_score.toFixed(1)}/10 · {t.sessions}×</span>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* ── Action Button ── */}
        <button
          onClick={() => window.location.href = '/group-discussion'}
          className="mt-auto flex items-center justify-center w-full py-4 rounded-2xl font-bold border-2 border-gray-100 text-gray-600 hover:border-violet-200 hover:bg-violet-50 hover:text-violet-700 transition-all"
        >
          Go to GD Practice
        </button>
      </div>
    </div>
  );
};

export default GDPerformanceCard;
