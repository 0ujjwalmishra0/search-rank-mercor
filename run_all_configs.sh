#!/usr/bin/env bash
# Mercor Re-Ranking Evaluation Runner for All Configs (macOS compatible)

mkdir -p results

# Define configs and queries as parallel arrays
CONFIGS=(
  "tax_lawyer.yml"
  "junior_corporate_lawyer.yml"
  "radiology.yml"
  "doctors_md.yml"
  "biology_expert.yml"
  "anthropology.yml"
  "mathematics_phd.yml"
  "quantitative_finance.yml"
  "bankers.yml"
  "mechanical_engineers.yml"
)

QUERIES=(
  "Seasoned tax lawyer with JD from a top US law school and 3+ years of experience"
  "Corporate lawyer with 2+ years experience at a top-tier international law firm specializing in M&A and contracts"
  "Radiologist with MD from India experienced in reading CT and MRI scans"
  "US-trained physician with over two years of clinical experience as a general practitioner"
  "Biologist with PhD from a top US university specializing in molecular biology and genetics"
  "PhD student in anthropology at a top US university focusing on labor migration and cultural identity"
  "Mathematician with PhD from a top US university specializing in statistical inference and stochastic processes"
  "MBA from a top US program with 3+ years experience in quantitative finance and algorithmic trading"
  "Healthcare investment banker with 2+ years experience in M&A and corporate finance"
  "Mechanical engineer with 3+ years experience in product development and SolidWorks"
)

# Loop through configs
for i in "${!CONFIGS[@]}"; do
  config="${CONFIGS[$i]}"
  query="${QUERIES[$i]}"

  echo "======================================================"
  echo "Running evaluation for: $config"
  echo "Query: $query"
  echo "======================================================"

  ./run_all.sh "$query" "$config" 50 > "results/${config%.yml}.log" 2>&1

  if [ -f top10.json ]; then
    cp top10.json "results/${config%.yml}_top10.json"
  fi

  echo "Saved logs and results for $config in results/${config%.yml}.log"
  echo ""
done

echo "✅ All configurations evaluated. Check the 'results/' folder for outputs."
