"use client";

import React, { useState } from "react";
import { useRouter } from "next/navigation";
// Simple Card component using Tailwind
const Card = ({ children, className = "" }: { children: React.ReactNode; className?: string }) => (
  <div className={`bg-white dark:bg-gray-800 rounded-xl border border-gray-200 dark:border-gray-700 shadow-sm ${className}`}>
    {children}
  </div>
);

import Badge from "@/components/ui/badge/Badge";
import Button from "@/components/ui/button/Button";

// Mock opportunities data
const mockOpportunities = [
  {
    id: "1",
    company: "TechCorp Rio",
    industry: "Software",
    funding: "Série B",
    diagnosis: "Finance Immaturity",
    services: ["Financial Structuring", "FP&A"],
    priorityScore: 92,
    urgencyScore: 85,
    revenuePotential: "Alto",
    status: "new",
    location: "Rio de Janeiro, RJ",
  },
  {
    id: "2",
    company: "FintechRJ",
    industry: "Fintech",
    funding: "Série A",
    diagnosis: "Operational Chaos",
    services: ["Operations Processes", "Financial Structuring"],
    priorityScore: 88,
    urgencyScore: 78,
    revenuePotential: "Médio-Alto",
    status: "contacted",
    location: "Rio de Janeiro, RJ",
  },
  {
    id: "3",
    company: "StartupBR",
    industry: "SaaS",
    funding: "Seed",
    diagnosis: "Growth Scaling",
    services: ["Growth Strategy"],
    priorityScore: 75,
    urgencyScore: 65,
    revenuePotential: "Médio",
    status: "new",
    location: "São Paulo, SP",
  },
];

const getScoreColor = (score: number) => {
  if (score >= 80) return "text-green-600 bg-green-50";
  if (score >= 60) return "text-yellow-600 bg-yellow-50";
  return "text-gray-600 bg-gray-50";
};

const getStatusBadge = (status: string): "light" | "primary" | "success" | "warning" | "error" => {
  const colors: Record<string, "light" | "primary" | "success" | "warning" | "error"> = {
    new: "warning",
    contacted: "primary",
    meeting: "success",
    won: "success",
    lost: "error",
  };
  return colors[status] || "light";
};

export default function OpportunitiesPage() {
  const router = useRouter();
  const [filter, setFilter] = useState<"all" | "new" | "contacted">("all");
  const [sortBy, setSortBy] = useState<"priority" | "urgency">("priority");

  const filteredOpportunities = mockOpportunities
    .filter((opp) => (filter === "all" ? true : opp.status === filter))
    .sort((a, b) => 
      sortBy === "priority" 
        ? b.priorityScore - a.priorityScore 
        : b.urgencyScore - a.urgencyScore
    );

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col lg:flex-row lg:items-center lg:justify-between gap-4">
        <div>
          <h1 className="text-2xl font-bold text-gray-900 dark:text-white">
            Oportunidades de Consultoria
          </h1>
          <p className="text-gray-500 dark:text-gray-400">
            Empresas priorizadas por potencial de consultoria
          </p>
        </div>
        <div className="flex gap-2">
          <select
            value={filter}
            onChange={(e) => setFilter(e.target.value as any)}
            className="px-3 py-2 border rounded-lg text-sm"
          >
            <option value="all">Todas</option>
            <option value="new">Novas</option>
            <option value="contacted">Contactadas</option>
          </select>
          <select
            value={sortBy}
            onChange={(e) => setSortBy(e.target.value as any)}
            className="px-3 py-2 border rounded-lg text-sm"
          >
            <option value="priority">Prioridade</option>
            <option value="urgency">Urgência</option>
          </select>
        </div>
      </div>

      {/* Stats */}
      <div className="grid grid-cols-1 sm:grid-cols-4 gap-4">
        <Card className="p-4 text-center">
          <p className="text-3xl font-bold text-blue-600">{mockOpportunities.length}</p>
          <p className="text-sm text-gray-500">Total</p>
        </Card>
        <Card className="p-4 text-center">
          <p className="text-3xl font-bold text-yellow-600">
            {mockOpportunities.filter(o => o.status === "new").length}
          </p>
          <p className="text-sm text-gray-500">Novas</p>
        </Card>
        <Card className="p-4 text-center">
          <p className="text-3xl font-bold text-green-600">
            {mockOpportunities.filter(o => o.priorityScore >= 80).length}
          </p>
          <p className="text-sm text-gray-500">Alta Prioridade</p>
        </Card>
        <Card className="p-4 text-center">
          <p className="text-3xl font-bold text-purple-600">Rio</p>
          <p className="text-sm text-gray-500">Foco Geográfico</p>
        </Card>
      </div>

      {/* Opportunities Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {filteredOpportunities.map((opp) => (
          <Card key={opp.id} className="p-6">
            <div className="flex justify-between items-start mb-4">
              <div>
                <h3 className="text-lg font-semibold text-gray-900 dark:text-white">
                  {opp.company}
                </h3>
                <p className="text-sm text-gray-500">
                  {opp.industry} • {opp.funding}
                </p>
              </div>
              <Badge color={getStatusBadge(opp.status)}>
                {opp.status.toUpperCase()}
              </Badge>
            </div>

            <div className="mb-4">
              <p className="text-sm text-gray-600 dark:text-gray-300 mb-2">
                <span className="font-medium">Diagnóstico:</span> {opp.diagnosis}
              </p>
              <div className="flex flex-wrap gap-2">
                {opp.services.map((service) => (
                  <Badge key={service} color="primary" size="sm">
                    {service}
                  </Badge>
                ))}
              </div>
            </div>

            <div className="grid grid-cols-3 gap-4 mb-4 p-3 bg-gray-50 dark:bg-gray-800 rounded-lg">
              <div className="text-center">
                <p className={`text-xl font-bold rounded ${getScoreColor(opp.priorityScore)}`}>
                  {opp.priorityScore}
                </p>
                <p className="text-xs text-gray-500 mt-1">Prioridade</p>
              </div>
              <div className="text-center">
                <p className={`text-xl font-bold rounded ${getScoreColor(opp.urgencyScore)}`}>
                  {opp.urgencyScore}
                </p>
                <p className="text-xs text-gray-500 mt-1">Urgência</p>
              </div>
              <div className="text-center">
                <p className="text-sm font-semibold text-gray-700 dark:text-gray-300">
                  {opp.revenuePotential}
                </p>
                <p className="text-xs text-gray-500 mt-1">Receita</p>
              </div>
            </div>

            <div className="flex gap-2">
              <Button
                variant="primary"
                size="sm"
                className="flex-1"
                onClick={() => router.push(`/engagement/angles/${opp.id}`)}
              >
                Gerar Ângulos
              </Button>
              <Button
                variant="outline"
                size="sm"
                className="flex-1"
                onClick={() => router.push(`/companies/${opp.id}`)}
              >
                Ver Empresa
              </Button>
            </div>
          </Card>
        ))}
      </div>
    </div>
  );
}
