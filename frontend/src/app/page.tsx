"use client";

import React, { useState, useEffect } from "react";
import { useRouter } from "next/navigation";
import Badge from "@/components/ui/badge/Badge";
import Button from "@/components/ui/button/Button";

// Simple Card component using Tailwind
const Card = ({ children, className = "" }: { children: React.ReactNode; className?: string }) => (
  <div className={`bg-white dark:bg-gray-800 rounded-xl border border-gray-200 dark:border-gray-700 shadow-sm ${className}`}>
    {children}
  </div>
);

// Mock data for demonstration - will be replaced with API calls
const mockStats = {
  signalsToday: 12,
  companiesTracked: 45,
  opportunities: 8,
  highPriority: 3,
};

const mockSignals = [
  {
    id: "1",
    company: "TechCorp Rio",
    type: "HIRING_FINANCE",
    title: "VP de Finanças - Série B",
    location: "Rio de Janeiro, RJ",
    score: 85,
    time: "2h atrás",
  },
  {
    id: "2",
    company: "StartupBR",
    type: "FUNDING",
    title: "Raised $10M Series A",
    location: "São Paulo, SP",
    score: 92,
    time: "5h atrás",
  },
  {
    id: "3",
    company: "FintechRJ",
    type: "HIRING_OPS",
    title: "Head de Operações",
    location: "Rio de Janeiro, RJ",
    score: 78,
    time: "1d atrás",
  },
];

const locationHierarchy = {
  continent: "Américas",
  subregion: "América do Sul",
  country: "Brasil",
  region: "Sudeste",
  state: "RJ",
  city: "Rio de Janeiro",
};

export default function DashboardPage() {
  const router = useRouter();
  const [selectedLocation, setSelectedLocation] = useState(locationHierarchy);
  const [activeFilter, setActiveFilter] = useState<"all" | "hiring" | "funding">("all");

  return (
    <div className="space-y-6">
      {/* Header with Location Filter */}
      <div className="flex flex-col lg:flex-row lg:items-center lg:justify-between gap-4">
        <div>
          <h1 className="text-2xl font-bold text-gray-900 dark:text-white">
            AI Consultancy Monitor
          </h1>
          <p className="text-gray-500 dark:text-gray-400">
            Prospecção de empresas para consultoria estratégica
          </p>
        </div>
        
        {/* Location Breadcrumb Filter */}
        <Card className="p-3 flex items-center gap-2 flex-wrap">
          <span className="text-sm text-gray-500">Localização:</span>
          {Object.entries(selectedLocation).map(([key, value], index, arr) => (
            <React.Fragment key={key}>
              <Badge 
                color={key === 'city' ? 'primary' : 'light'}
              >
                {value}
              </Badge>
              {index < arr.length - 1 && (
                <span className="text-gray-400">›</span>
              )}
            </React.Fragment>
          ))}
          <Button 
            variant="outline" 
            size="sm"
            onClick={() => router.push('/settings/location')}
          >
            Alterar
          </Button>
        </Card>
      </div>

      {/* Stats Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        <Card className="p-4 border-l-4 border-blue-500">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-gray-500 dark:text-gray-400">Sinais Hoje</p>
              <p className="text-2xl font-bold text-gray-900 dark:text-white">
                {mockStats.signalsToday}
              </p>
            </div>
            <div className="p-3 bg-blue-100 dark:bg-blue-900 rounded-full">
              <svg className="w-6 h-6 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
              </svg>
            </div>
          </div>
        </Card>

        <Card className="p-4 border-l-4 border-purple-500">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-gray-500 dark:text-gray-400">Empresas Trackeadas</p>
              <p className="text-2xl font-bold text-gray-900 dark:text-white">
                {mockStats.companiesTracked}
              </p>
            </div>
            <div className="p-3 bg-purple-100 dark:bg-purple-900 rounded-full">
              <svg className="w-6 h-6 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4" />
              </svg>
            </div>
          </div>
        </Card>

        <Card className="p-4 border-l-4 border-green-500">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-gray-500 dark:text-gray-400">Oportunidades</p>
              <p className="text-2xl font-bold text-gray-900 dark:text-white">
                {mockStats.opportunities}
              </p>
            </div>
            <div className="p-3 bg-green-100 dark:bg-green-900 rounded-full">
              <svg className="w-6 h-6 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
            </div>
          </div>
        </Card>

        <Card className="p-4 border-l-4 border-red-500">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-gray-500 dark:text-gray-400">Alta Prioridade</p>
              <p className="text-2xl font-bold text-gray-900 dark:text-white">
                {mockStats.highPriority}
              </p>
            </div>
            <div className="p-3 bg-red-100 dark:bg-red-900 rounded-full">
              <svg className="w-6 h-6 text-red-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
              </svg>
            </div>
          </div>
        </Card>
      </div>

      {/* Signal Type Filters */}
      <div className="flex gap-2">
        <Button
          variant={activeFilter === "all" ? "primary" : "outline"}
          size="sm"
          onClick={() => setActiveFilter("all")}
        >
          Todos os Sinais
        </Button>
        <Button
          variant={activeFilter === "hiring" ? "primary" : "outline"}
          size="sm"
          onClick={() => setActiveFilter("hiring")}
        >
          Contratações
        </Button>
        <Button
          variant={activeFilter === "funding" ? "primary" : "outline"}
          size="sm"
          onClick={() => setActiveFilter("funding")}
        >
          Funding
        </Button>
      </div>

      {/* Recent Signals Table */}
      <Card>
        <div className="p-4 border-b border-gray-200 dark:border-gray-700">
          <div className="flex items-center justify-between">
            <h2 className="text-lg font-semibold text-gray-900 dark:text-white">
              Sinais Recentes - {selectedLocation.city}
            </h2>
            <Button variant="outline" size="sm" onClick={() => router.push('/signals')}>
              Ver Todos
            </Button>
          </div>
        </div>
        <div className="overflow-x-auto">
          <table className="w-full">
            <thead className="bg-gray-50 dark:bg-gray-800">
              <tr>
                <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Empresa</th>
                <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Tipo</th>
                <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Sinal</th>
                <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Local</th>
                <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Score</th>
                <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Ações</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-gray-200 dark:divide-gray-700">
              {mockSignals.map((signal) => (
                <tr key={signal.id} className="hover:bg-gray-50 dark:hover:bg-gray-800">
                  <td className="px-4 py-3 font-medium text-gray-900 dark:text-white">
                    {signal.company}
                  </td>
                  <td className="px-4 py-3">
                    <Badge 
                      color={signal.type.includes('HIRING') ? 'success' : signal.type.includes('FUNDING') ? 'primary' : 'warning'}
                    >
                      {signal.type.replace('_', ' ')}
                    </Badge>
                  </td>
                  <td className="px-4 py-3 text-gray-600 dark:text-gray-300">
                    {signal.title}
                  </td>
                  <td className="px-4 py-3 text-gray-500 dark:text-gray-400">
                    {signal.location}
                  </td>
                  <td className="px-4 py-3">
                    <span className={`font-semibold ${
                      signal.score >= 80 ? 'text-green-600' : 
                      signal.score >= 60 ? 'text-yellow-600' : 'text-gray-600'
                    }`}>
                      {signal.score}
                    </span>
                  </td>
                  <td className="px-4 py-3">
                    <Button 
                      variant="outline" 
                      size="sm"
                      onClick={() => router.push(`/companies/${signal.id}`)}
                    >
                      Analisar
                    </Button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </Card>

      {/* Quick Actions */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <Card className="p-4 text-center">
          <div className="p-3 bg-blue-100 dark:bg-blue-900 rounded-full w-12 h-12 mx-auto mb-3">
            <svg className="w-6 h-6 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
            </svg>
          </div>
          <h3 className="font-semibold mb-2">Scan Nova Empresa</h3>
          <p className="text-sm text-gray-500 mb-3">Adicione uma empresa para monitoramento</p>
          <Button variant="primary" size="sm" className="w-full" onClick={() => router.push('/companies/scan')}>
            Iniciar Scan
          </Button>
        </Card>

        <Card className="p-4 text-center">
          <div className="p-3 bg-green-100 dark:bg-green-900 rounded-full w-12 h-12 mx-auto mb-3">
            <svg className="w-6 h-6 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
            </svg>
          </div>
          <h3 className="font-semibold mb-2">Ver Oportunidades</h3>
          <p className="text-sm text-gray-500 mb-3">Empresas com alto potencial</p>
          <Button variant="outline" size="sm" className="w-full" onClick={() => router.push('/opportunities')}>
            Explorar
          </Button>
        </Card>

        <Card className="p-4 text-center">
          <div className="p-3 bg-purple-100 dark:bg-purple-900 rounded-full w-12 h-12 mx-auto mb-3">
            <svg className="w-6 h-6 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
            </svg>
          </div>
          <h3 className="font-semibold mb-2">Templates de Email</h3>
          <p className="text-sm text-gray-500 mb-3">Engajamento automatizado</p>
          <Button variant="outline" size="sm" className="w-full" onClick={() => router.push('/engagement/templates')}>
            Ver Templates
          </Button>
        </Card>
      </div>
    </div>
  );
}
