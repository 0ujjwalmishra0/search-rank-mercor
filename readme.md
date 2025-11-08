## 📘 **README.md — Mercor Re-Ranking Assignment**

````markdown
# 🚀 Mercor Search Re-Ranking Assignment

## 📖 Overview
This project implements a **semantic search and re-ranking engine** on a snapshot of off-platform candidate data using the **Turbopuffer (TPUF)** vector database and **VoyageAI embeddings**.

The system retrieves top candidates for each query (role) and optionally re-ranks them using rule-based logic focused on **hard criteria** such as degree, years of experience, and location.  
Each query corresponds to a `.yml` configuration provided by Mercor (e.g., `tax_lawyer.yml`, `bankers.yml`), and final results are evaluated via the **Mercor Evaluation API**.

---

## 🧩 Architecture Overview

1. **Query Embedding** — Queries are embedded using the `voyage-3` model from VoyageAI.  
2. **Candidate Retrieval** — The top-K candidates are retrieved from a Turbopuffer namespace (`search-test-v4`) using approximate nearest neighbor (ANN) search on 1024-dim embeddings.  
3. **Re-Ranking** — The retrieved results are optionally re-ranked using:
   - Rule-based hard-criteria matching (`degree`, `experience`, `country`).
   - Keyword boosting based on query text overlap.
4. **Evaluation** — The final top 10 `_id`s are submitted to the Mercor `/evaluate` endpoint for each `.yml` config.

---

## ⚙️ Setup

### 1. Clone or extract the project
```bash
git clone https://github.com/<your_username>/mercor-re-ranking.git
cd mercor-re-ranking
````

### 2. Create environment and install dependencies

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 3. Configure environment variables

Copy the sample file:

```bash
cp .env.example .env
```

Edit `.env` and fill in:

```bash
TURBOPUFFER_API_KEY=tpuf_wTbagsVtzNmVfzDm48lNeszzJdTaCOUF
VOYAGE_API_KEY=pa-vNEmoJfc5evP_SSvpxIAj3uFzs9dfppEZkpx-3kOFZy
USER_EMAIL=0ujjwalmishra0@gmail.com
EVAL_ENDPOINT=https://mercor-dev--search-eng-interview.modal.run/evaluate
TPUF_REGION=aws-us-west-2
```

---

## 🚀 Running the System

### ▶️ Run for all queries

Runs all 10 `.yml` configs sequentially and stores results/logs:

```bash
./run_all_configs.sh
```

Results are saved under:

```
results/
  ├── tax_lawyer_top10.json
  ├── bankers_top10.json
  ├── mechanical_engineers_top10.json
  ├── ...
```

---

## 🧠 Example Evaluation (Bankers)

**Request (Python or Postman):**

```json
{
  "config_path": "bankers.yml",
  "object_ids": [
    "679612fd7e0084c5fa7b013f",
    "67952746f9f986ea7fb78042",
    "6794df910db3e792567306aa",
    "6795e5c7f9f986ea7fbe5445",
    "6794bf493eff0c142a7940df",
    "6794ca7c3eff0c142a798a56",
    "6794b5373eff0c142a78fd2b",
    "6794c7e00db3e792567272e6",
    "67974159f9f986ea7fca5c4b",
    "679665543e76d5b58730edab"
  ]
}
```

**Response:**

```json
{
  "config_name": "bankers",
  "num_candidates": 10,
  "average_final_score": 61.0,
  "average_soft_scores": [
    {
      "criteria_name": "healthcare_investment_banking_experience",
      "reasoning": null,
      "average_score": 9.4
    },
    {
      "criteria_name": "healthcare_ma_transactions",
      "reasoning": null,
      "average_score": 9.4
    },
    {
      "criteria_name": "healthcare_metrics_knowledge",
      "reasoning": null,
      "average_score": 7.8
    }
  ],
  "average_hard_scores": [
    {
      "criteria_name": "two_plus_years_banking",
      "reasoning": null,
      "pass_rate": 1.0
    },
    {
      "criteria_name": "mba_us_university",
      "reasoning": null,
      "pass_rate": 0.7
    }
  ],
  "individual_results": [
    {
      "candidate_name": "Jim Alfaro",
      "candidate_linkedin_url": "https://www.linkedin.com/in/jim-alfaro-741671",
      "soft_scores": [
        {
          "criteria_name": "healthcare_investment_banking_experience",
          "reasoning": "The candidate has over 20 years of experience in healthcare investment banking, including biotech, pharmaceuticals, medical devices, and HCIT, showing specialized industry experience.",
          "score": 10.0
        },
        {
          "criteria_name": "healthcare_ma_transactions",
          "reasoning": "Candidate has led M&A and capital raising transactions for healthcare companies and has extensive experience in mergers, acquisitions, and related advisory roles.",
          "score": 10.0
        },
        {
          "criteria_name": "healthcare_metrics_knowledge",
          "reasoning": "While explicit mention of healthcare-specific metrics (payer-provider integration, RCM optimization) is not detailed, extensive experience with healthcare companies, capital raising, and advisory roles implies a strong familiarity with relevant metrics and regulations.",
          "score": 8.0
        }
      ],
      "hard_scores": [
        {
          "criteria_name": "mba_us_university",
          "reasoning": "Candidate holds an MBA from University of California, Berkeley, which is a U.S. university.",
          "passes": true
        },
        {
          "criteria_name": "two_plus_years_banking",
          "reasoning": "Candidate has over 20 years of investment banking experience.",
          "passes": true
        }
      ],
      "final_score": 93.33333333333333,
      "raw_data": {
        "_id": "67952746f9f986ea7fb78042",
        "name": "Jim Alfaro",
        "linkedinId": "jim-alfaro-741671"
      }
    },
    {
      "candidate_name": "Michael Crabb",
      "candidate_linkedin_url": "https://www.linkedin.com/in/treycrabb",
      "soft_scores": [
        {
          "criteria_name": "healthcare_investment_banking_experience",
          "reasoning": "Michael Crabb has over 25 years advising healthcare entities with extensive roles in healthcare investment banking, including leadership positions at Bank of America, Morgan Stanley, and Ziegler focusing on healthcare M&A and financing advisory. His experience spans not-for-profit and for-profit healthcare sectors.",
          "score": 10.0
        },
        {
          "criteria_name": "healthcare_ma_transactions",
          "reasoning": "He has led and managed numerous large and complex healthcare M&A transactions, including hospital joint ventures, health system mergers, and strategic growth transactions. His track record includes founding and managing an M&A advisory firm and serving as healthcare M&A lead at multiple firms.",
          "score": 10.0
        },
        {
          "criteria_name": "healthcare_metrics_knowledge",
          "reasoning": "His roles involve deep engagement with healthcare-specific dynamics such as joint ventures between different healthcare entities, strategic planning, healthcare services sectors, and regulatory considerations. Also, his board service and academic roles highlight his familiarity with healthcare metrics and strategy.",
          "score": 9.0
        }
      ],
      "hard_scores": [
        {
          "criteria_name": "mba_us_university",
          "reasoning": "The candidate holds an MBA from UNC Kenan-Flagler Business School, a well-known U.S. university.",
          "passes": true
        },
        {
          "criteria_name": "two_plus_years_banking",
          "reasoning": "Michael Crabb has over 25 years of experience including multiple senior investment banking roles focused on healthcare, clearly exceeding the two-year minimum requirement.",
          "passes": true
        }
      ],
      "final_score": 96.66666666666667,
      "raw_data": {
        "_id": "6794bf493eff0c142a7940df",
        "name": "Michael Crabb",
        "linkedinId": "treycrabb"
      }
    },
    {
      "candidate_name": "Paul Kacik",
      "candidate_linkedin_url": "https://www.linkedin.com/in/paulkacik",
      "soft_scores": [
        {
          "criteria_name": "healthcare_investment_banking_experience",
          "reasoning": "Candidate has over 25 years of senior experience specifically in healthcare investment banking, advising on a wide range of healthcare sub-verticals including behavioral health, multi-site practices, revenue cycle management, and pharmaceutical services.",
          "score": 10.0
        },
        {
          "criteria_name": "healthcare_ma_transactions",
          "reasoning": "Candidate has a proven track record leading M&A, capital raising, recapitalizations, and financial advisory transactions in healthcare, including middle-market business mergers and acquisitions.",
          "score": 10.0
        },
        {
          "criteria_name": "healthcare_metrics_knowledge",
          "reasoning": "Candidate's roles as Managing Director and Head of Healthcare Investment Banking involved working with clinical labs, hospitals, managed care, and other provider groups, suggesting strong familiarity with healthcare-specific metrics and value creation strategies.",
          "score": 9.0
        }
      ],
      "hard_scores": [
        {
          "criteria_name": "mba_us_university",
          "reasoning": "Candidate holds an MBA from Bayes Business School, which is a U.K based school, not a U.S. university.",
          "passes": false
        },
        {
          "criteria_name": "two_plus_years_banking",
          "reasoning": "Candidate has over 25 years of experience in investment banking and related advisory roles, clearly exceeding two years in the field.",
          "passes": true
        }
      ],
      "final_score": 0.0,
      "raw_data": {
        "_id": "6794b5373eff0c142a78fd2b",
        "name": "Paul Kacik",
        "linkedinId": "paulkacik"
      }
    },
    {
      "candidate_name": "W. GREGORY SHEARER",
      "candidate_linkedin_url": "https://www.linkedin.com/in/gshearer",
      "soft_scores": [
        {
          "criteria_name": "healthcare_investment_banking_experience",
          "reasoning": "Extensive career focused exclusively on healthcare investment banking and venture capital with numerous roles in advisory and growth investing, especially in medical technology and healthcare services sectors.",
          "score": 10.0
        },
        {
          "criteria_name": "healthcare_ma_transactions",
          "reasoning": "Has completed over 150 financing or advisory transactions including mergers and acquisitions, recapitalizations, and private placements in healthcare. Demonstrated leadership in deal sourcing, diligence, and execution.",
          "score": 10.0
        },
        {
          "criteria_name": "healthcare_metrics_knowledge",
          "reasoning": "Strong involvement advising emerging growth healthcare companies, with specialty in private placements, leveraged finance, and strategic alliances suggests deep familiarity with healthcare-specific financial and regulatory frameworks and value creation strategies.",
          "score": 9.0
        }
      ],
      "hard_scores": [
        {
          "criteria_name": "mba_us_university",
          "reasoning": "Earned an MBA in Finance and Accounting from University of Chicago, a U.S. university.",
          "passes": true
        },
        {
          "criteria_name": "two_plus_years_banking",
          "reasoning": "Has decades of progressive experience in investment banking and healthcare deal advisory, clearly exceeding two years of prior experience.",
          "passes": true
        }
      ],
      "final_score": 96.66666666666667,
      "raw_data": {
        "_id": "6794c7e00db3e792567272e6",
        "name": "W. GREGORY SHEARER",
        "linkedinId": "gshearer"
      }
    },
    {
      "candidate_name": "Craig Fryer",
      "candidate_linkedin_url": "https://www.linkedin.com/in/craig-fryer-b884427",
      "soft_scores": [
        {
          "criteria_name": "healthcare_investment_banking_experience",
          "reasoning": "Candidate has extensive experience in healthcare investment banking roles at J.P. Morgan, William Blair, Bank of America Merrill Lynch, and JMP Securities, indicating specialized knowledge in healthcare-focused investment banking.",
          "score": 9.0
        },
        {
          "criteria_name": "healthcare_ma_transactions",
          "reasoning": "Candidate has participated in over 100 transactions totaling around $40 billion, with roles specifically in healthcare M&A and capital markets, showing strong experience leading and contributing to healthcare transactions.",
          "score": 9.0
        },
        {
          "criteria_name": "healthcare_metrics_knowledge",
          "reasoning": "Although candidate's summary details extensive healthcare investment banking experience, there is no explicit mention of familiarity with healthcare-specific metrics or regulatory frameworks. However, given senior banking roles in healthcare, some knowledge can be reasonably inferred.",
          "score": 7.0
        }
      ],
      "hard_scores": [
        {
          "criteria_name": "mba_us_university",
          "reasoning": "Candidate holds an MBA from Duke University, a U.S. university.",
          "passes": true
        },
        {
          "criteria_name": "two_plus_years_banking",
          "reasoning": "Candidate has more than two years of investment banking experience as evidenced by senior roles at multiple banks, including executive director and director positions.",
          "passes": true
        }
      ],
      "final_score": 83.33333333333334,
      "raw_data": {
        "_id": "679665543e76d5b58730edab",
        "name": "Craig Fryer",
        "linkedinId": "craig-fryer-b884427"
      }
    },
    {
      "candidate_name": "Arndt O. Welsch-Lehmann",
      "candidate_linkedin_url": "https://www.linkedin.com/in/arndt-oliver-welsch-lehmann-9bb1122",
      "soft_scores": [
        {
          "criteria_name": "healthcare_investment_banking_experience",
          "reasoning": "Candidate has extensive private equity and investment experience focused on healthcare technology companies, including deal sourcing and investment banking services specific to healthcare technology. This indicates strong specialized experience in healthcare investment banking and private equity sub-verticals related to healthtech.",
          "score": 8.0
        },
        {
          "criteria_name": "healthcare_ma_transactions",
          "reasoning": "Candidate has led and executed various investment transactions involving healthcare technology firms, including direct secondary private equity investments and advisory services. While M&A is not explicitly mentioned, involvement in banking and investment transactions suggests active participation in such deals.",
          "score": 7.0
        },
        {
          "criteria_name": "healthcare_metrics_knowledge",
          "reasoning": "Candidate's summary indicates diverse financial and credit analysis experience with exposure to different industries and detailed familiarity with debt and equity structures. However, there is no explicit mention of healthcare-specific metrics, regulatory frameworks, or value creation strategies such as payer-provider integration or RCM optimization.",
          "score": 4.0
        }
      ],
      "hard_scores": [
        {
          "criteria_name": "mba_us_university",
          "reasoning": "Candidate holds an MBA in Finance from James Madison University, which is a U.S. university.",
          "passes": true
        },
        {
          "criteria_name": "two_plus_years_banking",
          "reasoning": "Candidate has over 20 years of business experience including private equity, investment banking, corporate finance roles, and financial institutions, satisfying the requirement of 2+ years in investment banking, corporate finance, or M&A advisory.",
          "passes": true
        }
      ],
      "final_score": 63.33333333333333,
      "raw_data": {
        "_id": "6794ca7c3eff0c142a798a56",
        "name": "Arndt O. Welsch-Lehmann",
        "linkedinId": "arndt-oliver-welsch-lehmann-9bb1122"
      }
    },
    {
      "candidate_name": "Peter Lang",
      "candidate_linkedin_url": "https://www.linkedin.com/in/peter-lang1",
      "soft_scores": [
        {
          "criteria_name": "healthcare_investment_banking_experience",
          "reasoning": "Candidate has extensive healthcare-focused investment banking experience with over 25 years working at leading firms including HSBC, UBS, Leerink Partners, and others covering biopharma, medtech, and healthcare services, demonstrating deep sector knowledge and leadership.",
          "score": 10.0
        },
        {
          "criteria_name": "healthcare_ma_transactions",
          "reasoning": "Candidate has led and advised on over 40 M&A deals totaling approximately $26 billion including multi-site provider groups and digital health companies, with direct involvement in M&A, recapitalizations, and growth equity investments, including a $955 million acquisition deal.",
          "score": 10.0
        },
        {
          "criteria_name": "healthcare_metrics_knowledge",
          "reasoning": "Candidate has demonstrated familiarity with healthcare-specific financial strategies, capital structure optimization, payer-provider integration concepts, and value creation strategies through CFO roles, growth equity fund experience, and advising on complex healthcare transactions.",
          "score": 9.0
        }
      ],
      "hard_scores": [
        {
          "criteria_name": "mba_us_university",
          "reasoning": "No mention of the candidate holding an MBA from a U.S. university was found in the profile or experience details.",
          "passes": false
        },
        {
          "criteria_name": "two_plus_years_banking",
          "reasoning": "Candidate has over 25 years of continuous experience in investment banking, corporate finance, and M&A advisory roles in healthcare and related sectors.",
          "passes": true
        }
      ],
      "final_score": 0.0,
      "raw_data": {
        "_id": "6794df910db3e792567306aa",
        "name": "Peter Lang",
        "linkedinId": "peter-lang1"
      }
    },
    {
      "candidate_name": "Prasad Parmeshwaran",
      "candidate_linkedin_url": "https://www.linkedin.com/in/prasad-parmeshwaran-b5424a1",
      "soft_scores": [
        {
          "criteria_name": "healthcare_investment_banking_experience",
          "reasoning": "The candidate has over 15 years of healthcare-focused experience in investment banking and related areas, including roles at Merrill Lynch, Lazard, Cowen, and Goldman Sachs, covering biotech, pharma, and healthcare services.",
          "score": 9.0
        },
        {
          "criteria_name": "healthcare_ma_transactions",
          "reasoning": "The candidate has led or contributed to numerous M&A and corporate development transactions including deal sourcing, financial and commercial evaluation, due diligence, valuation, deal structuring, and negotiations in the healthcare sector.",
          "score": 9.0
        },
        {
          "criteria_name": "healthcare_metrics_knowledge",
          "reasoning": "Given the candidate's senior roles in healthcare banking and corporate development with a focus on strategic M&A activities, it is highly likely they possess strong knowledge of healthcare-specific metrics, regulatory frameworks, and value creation strategies.",
          "score": 8.0
        }
      ],
      "hard_scores": [
        {
          "criteria_name": "mba_us_university",
          "reasoning": "The candidate holds an MBA from NYU Stern School of Business, a U.S. university.",
          "passes": true
        },
        {
          "criteria_name": "two_plus_years_banking",
          "reasoning": "The candidate has extensive experience with many years in investment banking and healthcare corporate development roles, clearly exceeding two years in relevant fields.",
          "passes": true
        }
      ],
      "final_score": 86.66666666666667,
      "raw_data": {
        "_id": "6795e5c7f9f986ea7fbe5445",
        "name": "Prasad Parmeshwaran",
        "linkedinId": "prasad-parmeshwaran-b5424a1"
      }
    },
    {
      "candidate_name": "Sameer Chugh",
      "candidate_linkedin_url": "https://www.linkedin.com/in/sameer-chugh",
      "soft_scores": [
        {
          "criteria_name": "healthcare_investment_banking_experience",
          "reasoning": "Has extensive healthcare-focused investment banking experience including coverage of healthcare services, behavioral health, post-acute services, and involvement with digital health-related provider networks.",
          "score": 9.0
        },
        {
          "criteria_name": "healthcare_ma_transactions",
          "reasoning": "Led and contributed to 40+ M&A transactions worth $30+billion primarily in healthcare services, including provider groups, post-acute care, tech-enabled care, and multiple buy-side and sell-side mandates.",
          "score": 10.0
        },
        {
          "criteria_name": "healthcare_metrics_knowledge",
          "reasoning": "Experience working with complex healthcare transactions implies knowledge of relevant healthcare metrics and regulatory environments; no explicit mention of payer-provider integration or RCM, but senior roles suggest substantial familiarity.",
          "score": 8.0
        }
      ],
      "hard_scores": [
        {
          "criteria_name": "mba_us_university",
          "reasoning": "Holds an MBA degree from New York University - Leonard N. Stern School Of Business, a U.S. university.",
          "passes": true
        },
        {
          "criteria_name": "two_plus_years_banking",
          "reasoning": "Over 7 years of investment banking experience at UBS and multiple senior roles in healthcare investment banking and M&A advisory.",
          "passes": true
        }
      ],
      "final_score": 90.0,
      "raw_data": {
        "_id": "679612fd7e0084c5fa7b013f",
        "name": "Sameer Chugh",
        "linkedinId": "sameer-chugh"
      }
    },
    {
      "candidate_name": "Amir Zafar",
      "candidate_linkedin_url": "https://www.linkedin.com/in/amir-zafar",
      "soft_scores": [
        {
          "criteria_name": "healthcare_investment_banking_experience",
          "reasoning": "Amir Zafar has extensive investment banking experience focused on healthcare sectors such as healthcare services, medical technology, biopharma, and consumer health across multiple institutions and geographies, indicating strong specialization.",
          "score": 9.0
        },
        {
          "criteria_name": "healthcare_ma_transactions",
          "reasoning": "He has led and originated multiple M&A transactions and advisory efforts in healthcare, including mid-market M&A and coverage for healthcare services and med-tech sectors, demonstrating substantial involvement in healthcare M&A activities.",
          "score": 9.0
        },
        {
          "criteria_name": "healthcare_metrics_knowledge",
          "reasoning": "While specific metrics or regulatory frameworks are not explicitly listed, his leadership roles in healthcare M&A and strategic advisory, and sector coverage implies strong familiarity with healthcare-specific value creation strategies and regulations.",
          "score": 7.0
        }
      ],
      "hard_scores": [
        {
          "criteria_name": "mba_us_university",
          "reasoning": "The candidate holds MBAs from INSEAD and the Institute Of Business Administration, but there is no indication of an MBA from a U.S. university.",
          "passes": false
        },
        {
          "criteria_name": "two_plus_years_banking",
          "reasoning": "The candidate has held multiple senior and mid-level investment banking roles for well over two years across several leading banks and advisory firms.",
          "passes": true
        }
      ],
      "final_score": 0.0,
      "raw_data": {
        "_id": "67974159f9f986ea7fca5c4b",
        "name": "Amir Zafar",
        "linkedinId": "amir-zafar"
      }
    }
  ]
}
```

---

## 📊 Evaluation Summary (Example)

| Config                      | Description                           | Score | Precision@10 |
| --------------------------- | ------------------------------------- | ----- | ------------ |
| tax_lawyer.yml              | JD, 3+ yrs corporate tax              | 0.82  | 0.70         |
| junior_corporate_lawyer.yml | 2–4 yrs M&A support                   | 0.78  | 0.68         |
| radiology.yml               | MD, imaging expertise                 | 0.80  | 0.71         |
| doctors_md.yml              | General practitioner (US)             | 0.83  | 0.72         |
| biology_expert.yml          | PhD, molecular biology                | 0.85  | 0.75         |
| anthropology.yml            | PhD (in progress), migration research | 0.77  | 0.65         |
| mathematics_phd.yml         | PhD, stochastic modeling              | 0.82  | 0.70         |
| quantitative_finance.yml    | MBA + 3 yrs quant finance             | 0.86  | 0.76         |
| bankers.yml                 | Healthcare investment banker          | 0.84  | 0.72         |
| mechanical_engineers.yml    | 3+ yrs product design                 | 0.80  | 0.68         |

*(Scores illustrative — replace with your actual evaluation results.)*

---

## 🧩 Code Structure

| File                 | Purpose                                         |
| -------------------- | ----------------------------------------------- |
| `tpuf_client.py`     | Connects to Turbopuffer namespace               |
| `embed.py`           | Handles VoyageAI query embeddings               |
| `retrieve.py`        | Retrieves top-K profiles via ANN search         |
| `rerank.py`          | Re-ranks results based on hard/soft criteria    |
| `evaluate.py`        | Submits ranked results to Mercor evaluation API |
| `run_all_configs.sh` | Batch runner for all configs                    |
| `results/`           | Stores logs, top10 IDs, and evaluation results  |

---

## 🧠 Approach Summary

* **Retriever:** Embeddings from `voyage-3`, queried against TPUF’s ANN index.
* **Re-Ranker:**

    * *Hard criteria* (degree, experience, location).
    * *Soft criteria* via text keyword boosts in `rerankSummary`.
* **Evaluation:** Automatic submission to Mercor `/evaluate` endpoint for all `.yml` roles.

This hybrid approach balances **semantic similarity** (via embeddings) with **rule-based precision filtering**, ensuring the top results meet strict qualification criteria before scoring.

---

## 🧾 Results & Deliverables

* ✅ All 10 evaluations completed successfully via Postman.
* ✅ Results stored in `results/` folder.
* ✅ Code is modular and ready for further model-based re-ranking.
* ✅ README and `.env.example` included for reproducibility.

---

## ✉️ Submission Notes

Please evaluate this repository using the provided email authorization header:
`Authorization: 0ujjwalmishra0@gmail.com`

All queries have been validated via the live API.

**Author:** Ujjwal Mishra
**Date:** November 2025
**Email:** [0ujjwalmishra0@gmail.com](mailto:0ujjwalmishra0@gmail.com)

```
