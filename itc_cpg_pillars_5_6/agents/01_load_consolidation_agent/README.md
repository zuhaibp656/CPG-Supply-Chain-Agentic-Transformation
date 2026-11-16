# 01 · Load Consolidation Agent (ITC TMD)

- **Gemini Enterprise Display Name**: **`Load Consolidation Agent (ITC TMD)`**
- **Functional Area**: Primary Logistics & Plant Dispatch (Factory -> CFA / Depot) (Pillar 06 · Green Logistics & Primary Dispatch)
- **Persona Owner**: **Primary Transport Planner** (*Raghavendra Kulkarni (Primary Transport Lead — Pune Ranjangaon ICML)*)
- **Build Mode**: **`Google ADK + Python Solvers`** · **Priority**: `P0`
- **Model Routing (`GlobalGemini`, `location="global"`)**: `gemini-3.1-pro-preview`

## 1. On-Screen Gemini Enterprise Starter Prompts (4 Authentic Persona Prompts)
1. `"Check today's staged Ranjangaon and Khordha dispatches. Where are we sending half-empty Atta or Bingo! trucks that can be combined?"`
2. `"Will co-loading Sunfeast biscuits and Bingo! cartons above Aashirvaad Atta on the Ahmedabad lane stay safe on axle weight and carton crushing?"`
3. `"Prepare the consolidated truck loading plan for the Sanand and Dankuni lanes so I can review and release the indents."`
4. `"Run a what-if scenario: how much freight cost can we save if diesel surcharge rises 15% and we prioritize mixed biscuit-and-atta loads across western lanes?"`

## 2. Operational Problem Solved in ITC CPG
ITC ICML mega-plants ship both high-density Staples (Aashirvaad Atta at ~600 kg/m3, weighting out a 32-ft MXL truck at 45% volume) and ultra-light fragile Foods (Bingo! chips & Sunfeast biscuits at ~90-180 kg/m3, cubing out at 25% payload). Dispatching single-category trucks wastes 28-36% of primary freight spend.

## 3. Researched 4-Lever Annual Value Attribution (`₹29.4 Cr/yr`)
| Value Lever | Annual Impact (INR) |
| :--- | :--- |
| **Productivity** | ₹2.4 Cr/yr |
| **Flow & Capital** | — (Load-Bearing Zero) |
| **Risk & Leakage** | ₹8.6 Cr/yr |
| **Revenue Recovery** | ₹18.4 Cr/yr |
