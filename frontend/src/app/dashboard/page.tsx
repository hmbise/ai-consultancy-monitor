"use client";

import React, { useEffect, useState } from "react";
import { apiClient, Signal, Company, Opportunity } from "@/lib/api";
import Card from "@/components/ui/Card";
import Button from "@/components/ui/Button";

export default function DashboardPage() {
  const [stats, setStats] = useState({
    signals: 0,
    companies: 0,
    opportunities: 0,
    health: null as any,
  });
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function loadStats() {
      try {
        const [signals, companies, opportunities, health] = await Promise.all([
          apiClient.getSignals(),
          apiClient.getCompanies(),
          apiClient.getOpportunities(),
          apiClient.getHealth(),
        ]);
        setStats({
          signals: signals.length,
          companies: companies.length,
          opportunities: opportunities.length,
          health,
        });
      } catch (error) {
        console.error("Failed to load stats:", error);
      } finally {
        setLoading(false);
      }
    }
    loadStats();
  }, []);

  if (loading) {
    return <div className="p-6">Loading dashboard...</div>;
  }

  return (
    <div className="p-6">
      <h1 className="text-2xl font-bold mb-6">AI Consultancy Monitor Dashboard</h1>
      
      {/* Status Bar */}
      <div className="mb-6 p-4 bg-green-50 border border-green-200 rounded-lg">
        <div className="flex items-center gap-2">
          <div className="w-3 h-3 bg-green-500 rounded-full"></div>
          <span className="text-green-800 font-medium">
            API Status: {stats.health?.status} | Schema: {stats.health?.schema}
          </span>
        </div>
      </div>

      {/* Stats Grid */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
        <Card className="p-6">
          <div className="text-3xl font-bold text-blue-600">{stats.signals}</div>
          <div className="text-gray-600">Total Signals</div>
          <Button href="/signals" variant="outline" className="mt-4 w-full">
            View Signals
          </Button>
        </Card>

        <Card className="p-6">
          <div className="text-3xl font-bold text-purple-600">{stats.companies}</div>
          <div className="text-gray-600">Companies Tracked</div>
          <Button href="/companies" variant="outline" className="mt-4 w-full">
            View Companies
          </Button>
        </Card>

        <Card className="p-6">
          <div className="text-3xl font-bold text-green-600">{stats.opportunities}</div>
          <div className="text-gray-600">Opportunities</div>
          <Button href="/opportunities" variant="outline" className="mt-4 w-full">
            View Opportunities
          </Button>
        </Card>
      </div>

      {/* Quick Actions */}
      <div className="bg-white rounded-lg shadow p-6">
        <h2 className="text-xl font-semibold mb-4">Quick Actions</h2>
        <div className="flex gap-4">
          <Button href="/companies/scan" variant="primary">
            Scan New Company
          </Button>
          <Button href="/signals" variant="secondary">
            Browse Signals
          </Button>
        </div>
      </div>
    </div>
  );
}
