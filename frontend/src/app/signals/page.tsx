"use client";

import React, { useEffect, useState } from "react";
import { apiClient, Signal } from "@/lib/api";
import Badge from "@/components/ui/badge/Badge";
import Button from "@/components/ui/button/Button";

// Simple Card component using Tailwind
const Card = ({ children, className = "" }: { children: React.ReactNode; className?: string }) => (
  <div className={`bg-white dark:bg-gray-800 rounded-xl border border-gray-200 dark:border-gray-700 shadow-sm ${className}`}>
    {children}
  </div>
);

export default function SignalsPage() {
  const [signals, setSignals] = useState<Signal[]>([]);
  const [loading, setLoading] = useState(true);
  const [filter, setFilter] = useState("");

  useEffect(() => {
    async function loadSignals() {
      try {
        const data = await apiClient.getSignals();
        setSignals(data);
      } catch (error) {
        console.error("Failed to load signals:", error);
      } finally {
        setLoading(false);
      }
    }
    loadSignals();
  }, []);

  const filteredSignals = signals.filter((s) =>
    s.title.toLowerCase().includes(filter.toLowerCase()) ||
    s.signal_type.toLowerCase().includes(filter.toLowerCase())
  );

  const getSignalTypeColor = (type: string): "success" | "primary" | "warning" | "light" => {
    if (type.includes("HIRING")) return "success";
    if (type.includes("FUNDING")) return "primary";
    if (type.includes("LEADERSHIP")) return "warning";
    return "light";
  };

  if (loading) {
    return <div className="p-6">Loading signals...</div>;
  }

  return (
    <div className="p-6">
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-2xl font-bold">Signals</h1>
        <input
          type="text"
          placeholder="Filter signals..."
          value={filter}
          onChange={(e) => setFilter(e.target.value)}
          className="px-4 py-2 border rounded-lg w-64"
        />
      </div>

      <div className="space-y-4">
        {filteredSignals.length === 0 ? (
          <Card className="p-6 text-center text-gray-500">
            No signals found. Start by scanning a company.
          </Card>
        ) : (
          filteredSignals.map((signal) => (
            <Card key={signal.id} className="p-4">
              <div className="flex justify-between items-start">
                <div className="flex-1">
                  <div className="flex items-center gap-2 mb-2">
                    <Badge color={getSignalTypeColor(signal.signal_type)}>
                      {signal.signal_type}
                    </Badge>
                    <span className="text-sm text-gray-500">{signal.source}</span>
                  </div>
                  <h3 className="font-semibold text-lg mb-2">{signal.title}</h3>
                  <p className="text-gray-600 text-sm mb-2">{signal.content}</p>
                  <div className="text-xs text-gray-400">
                    Discovered: {new Date(signal.discovered_at).toLocaleDateString()}
                  </div>
                </div>
                {signal.url && (
                  <a
                    href={signal.url}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="text-blue-600 hover:underline text-sm"
                  >
                    View Source →
                  </a>
                )}
              </div>
            </Card>
          ))
        )}
      </div>
    </div>
  );
}
