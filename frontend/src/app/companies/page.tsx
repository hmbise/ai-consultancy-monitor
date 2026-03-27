"use client";

import React, { useEffect, useState } from "react";
import { apiClient, Company } from "@/lib/api";
import Card from "@/components/ui/Card";
import Button from "@/components/ui/Button";
import Badge from "@/components/ui/Badge";

export default function CompaniesPage() {
  const [companies, setCompanies] = useState<Company[]>([]);
  const [loading, setLoading] = useState(true);
  const [search, setSearch] = useState("");

  useEffect(() => {
    async function loadCompanies() {
      try {
        const data = await apiClient.getCompanies();
        setCompanies(data);
      } catch (error) {
        console.error("Failed to load companies:", error);
      } finally {
        setLoading(false);
      }
    }
    loadCompanies();
  }, []);

  const filteredCompanies = companies.filter((c) =>
    c.name.toLowerCase().includes(search.toLowerCase()) ||
    c.industry?.toLowerCase().includes(search.toLowerCase())
  );

  const getStageColor = (stage?: string) => {
    const stages: Record<string, string> = {
      "seed": "warning",
      "series_a": "primary",
      "series_b": "success",
      "series_c": "success",
      "ipo": "primary",
    };
    return stages[stage || "" ] || "default";
  };

  if (loading) {
    return <div className="p-6">Loading companies...</div>;
  }

  return (
    <div className="p-6">
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-2xl font-bold">Companies</h1>
        <div className="flex gap-4">
          <input
            type="text"
            placeholder="Search companies..."
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            className="px-4 py-2 border rounded-lg w-64"
          />
          <Button href="/companies/scan" variant="primary">
            + Scan Company
          </Button>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {filteredCompanies.length === 0 ? (
          <Card className="col-span-full p-6 text-center text-gray-500">
            No companies found. Start by scanning one.
          </Card>
        ) : (
          filteredCompanies.map((company) => (
            <Card key={company.id} className="p-4">
              <div className="flex justify-between items-start mb-3">
                <h3 className="font-semibold text-lg">{company.name}</h3>
                {company.funding_stage && (
                  <Badge color={getStageColor(company.funding_stage)}>
                    {company.funding_stage.replace("_", " ").toUpperCase()}
                  </Badge>
                )}
              </div>
              
              <div className="space-y-2 text-sm text-gray-600">
                {company.industry && (
                  <div>Industry: {company.industry}</div>
                )}
                {company.location_country && (
                  <div>Location: {company.location_country}</div>
                )}
                {company.last_signal_at && (
                  <div className="text-xs text-gray-400">
                    Last signal: {new Date(company.last_signal_at).toLocaleDateString()}
                  </div>
                )}
              </div>

              <div className="mt-4 pt-4 border-t flex gap-2">
                <Button 
                  href={`/companies/${company.id}`} 
                  variant="outline" 
                  size="sm"
                  className="flex-1"
                >
                  View
                </Button>
                <Button 
                  href={`/signals?company=${company.id}`} 
                  variant="secondary" 
                  size="sm"
                  className="flex-1"
                >
                  Signals
                </Button>
              </div>
            </Card>
          ))
        )}
      </div>
    </div>
  );
}
