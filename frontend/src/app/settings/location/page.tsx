"use client";

import React, { useState } from "react";
import { useRouter } from "next/navigation";
import Button from "@/components/ui/button/Button";

// Simple Card component using Tailwind
const Card = ({ children, className = "" }: { children: React.ReactNode; className?: string }) => (
  <div className={`bg-white dark:bg-gray-800 rounded-xl border border-gray-200 dark:border-gray-700 shadow-sm ${className}`}>
    {children}
  </div>
);

// Location hierarchy for Brazil > Sudeste > RJ > Rio de Janeiro
const locationHierarchy = {
  continents: ["Américas"],
  subregions: {
    "Américas": ["América do Norte", "América Central", "América do Sul", "Caribe"],
  },
  countries: {
    "América do Sul": ["Brasil", "Argentina", "Chile", "Colômbia", "Peru", "Uruguai"],
  },
  regions: {
    "Brasil": ["Norte", "Nordeste", "Centro-Oeste", "Sudeste", "Sul"],
  },
  states: {
    "Sudeste": ["RJ", "SP", "MG", "ES"],
  },
  cities: {
    "RJ": ["Rio de Janeiro", "Niterói", "Petrópolis", "Duque de Caxias", "Nova Iguaçu", "São Gonçalo"],
  },
};

const defaultSelection = {
  continent: "Américas",
  subregion: "América do Sul",
  country: "Brasil",
  region: "Sudeste",
  state: "RJ",
  city: "Rio de Janeiro",
};

export default function LocationSettingsPage() {
  const router = useRouter();
  const [selection, setSelection] = useState(defaultSelection);
  const [saved, setSaved] = useState(false);

  const handleSave = () => {
    // Save to localStorage or API
    localStorage.setItem("prospecting_location", JSON.stringify(selection));
    setSaved(true);
    setTimeout(() => setSaved(false), 2000);
  };

  return (
    <div className="max-w-2xl mx-auto space-y-6">
      {/* Header */}
      <div className="text-center">
        <h1 className="text-2xl font-bold text-gray-900 dark:text-white">
          Filtro Geográfico
        </h1>
        <p className="text-gray-500 dark:text-gray-400 mt-2">
          Defina a localização para prospecção de empresas
        </p>
      </div>

      {/* Current Selection Card */}
      <Card className="p-6">
        <h2 className="text-lg font-semibold mb-4 text-gray-900 dark:text-white">
          Localização Atual
        </h2>
        <div className="flex flex-wrap items-center gap-2 text-sm">
          {Object.entries(selection).map(([key, value], index, arr) => (
            <React.Fragment key={key}>
              <span className="px-3 py-1 bg-blue-100 dark:bg-blue-900 text-blue-800 dark:text-blue-200 rounded-full font-medium capitalize">
                {value}
              </span>
              {index < arr.length - 1 && (
                <span className="text-gray-400">›</span>
              )}
            </React.Fragment>
          ))}
        </div>
      </Card>

      {/* Selection Form */}
      <Card className="p-6">
        <h2 className="text-lg font-semibold mb-6 text-gray-900 dark:text-white">
          Selecionar Localização
        </h2>

        <div className="space-y-4">
          {/* Continent */}
          <div>
            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
              Continente
            </label>
            <select
              value={selection.continent}
              onChange={(e) => setSelection({ ...selection, continent: e.target.value })}
              className="w-full px-3 py-2 border rounded-lg dark:bg-gray-800 dark:border-gray-700"
            >
              {locationHierarchy.continents.map((c) => (
                <option key={c} value={c}>{c}</option>
              ))}
            </select>
          </div>

          {/* Subregion */}
          <div>
            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
              Subdivisão Continental
            </label>
            <select
              value={selection.subregion}
              onChange={(e) => setSelection({ ...selection, subregion: e.target.value })}
              className="w-full px-3 py-2 border rounded-lg dark:bg-gray-800 dark:border-gray-700"
            >
              {locationHierarchy.subregions[selection.continent]?.map((s) => (
                <option key={s} value={s}>{s}</option>
              ))}
            </select>
          </div>

          {/* Country */}
          <div>
            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
              País
            </label>
            <select
              value={selection.country}
              onChange={(e) => setSelection({ ...selection, country: e.target.value })}
              className="w-full px-3 py-2 border rounded-lg dark:bg-gray-800 dark:border-gray-700"
            >
              {locationHierarchy.countries[selection.subregion]?.map((c) => (
                <option key={c} value={c}>{c}</option>
              ))}
            </select>
          </div>

          {/* Region */}
          <div>
            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
              Região
            </label>
            <select
              value={selection.region}
              onChange={(e) => setSelection({ ...selection, region: e.target.value })}
              className="w-full px-3 py-2 border rounded-lg dark:bg-gray-800 dark:border-gray-700"
            >
              {locationHierarchy.regions[selection.country]?.map((r) => (
                <option key={r} value={r}>{r}</option>
              ))}
            </select>
          </div>

          {/* State */}
          <div>
            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
              Estado/Província
            </label>
            <select
              value={selection.state}
              onChange={(e) => setSelection({ ...selection, state: e.target.value })}
              className="w-full px-3 py-2 border rounded-lg dark:bg-gray-800 dark:border-gray-700"
            >
              {locationHierarchy.states[selection.region]?.map((s) => (
                <option key={s} value={s}>{s}</option>
              ))}
            </select>
          </div>

          {/* City */}
          <div>
            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
              Cidade
            </label>
            <select
              value={selection.city}
              onChange={(e) => setSelection({ ...selection, city: e.target.value })}
              className="w-full px-3 py-2 border rounded-lg dark:bg-gray-800 dark:border-gray-700"
            >
              {locationHierarchy.cities[selection.state]?.map((c) => (
                <option key={c} value={c}>{c}</option>
              ))}
            </select>
          </div>
        </div>

        {/* Actions */}
        <div className="flex gap-4 mt-6">
          <Button 
            variant="primary" 
            className="flex-1"
            onClick={handleSave}
          >
            {saved ? "✓ Salvo!" : "Salvar Localização"}
          </Button>
          <Button 
            variant="outline"
            onClick={() => setSelection(defaultSelection)}
          >
            Resetar
          </Button>
        </div>
      </Card>

      {/* Info Card */}
      <Card className="p-6 bg-blue-50 dark:bg-blue-900/20 border-blue-200">
        <h3 className="font-semibold text-blue-900 dark:text-blue-200 mb-2">
          💡 Dica de Prospecção
        </h3>
        <p className="text-sm text-blue-800 dark:text-blue-300">
          Para prospecção de consultoria no Rio de Janeiro, recomendamos focar em empresas 
          de Série A/B na região Sudeste, especialmente startups de fintech e SaaS que 
          estão em fase de crescimento e podem precisar de estruturação financeira e operacional.
        </p>
      </Card>

      {/* Quick Navigation */}
      <div className="flex justify-center gap-4">
        <Button variant="outline" onClick={() => router.push('/')}>
          ← Voltar ao Dashboard
        </Button>
        <Button variant="outline" onClick={() => router.push('/companies')}>
          Ver Empresas →
        </Button>
      </div>
    </div>
  );
}
