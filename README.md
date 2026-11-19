# Talent Development & Succession Planning Dashboard

Only 16 of 1,233 active employees (1.3%) are ready for promotion right now, and 14 of them are Staff or Senior Staff. Nobody at Executive level is ready, and Manager and Senior Manager have one person each. That's the main thing this dashboard shows.

I built it in Power BI on top of the IBM HR Analytics dataset. It puts every active employee on a 9-box talent grid, shows who is ready to step up at each job level, and flags 130 good performers (10.5%) who haven't been promoted in 3 years or more.

Tools: Python (pandas, NumPy), Power BI, DAX
Data: [IBM HR Analytics Employee Attrition](https://www.kaggle.com/datasets/pavansubhasht/ibm-hr-analytics-attrition-dataset), a fictional sample of 1,470 employees and 35 columns
Full write-up: [case study](https://drive.google.com/file/d/1TfIMVftdg4eRFMqqJfEYhTgbyfuN4-uV/view?usp=sharing)

## Questions I wanted to answer

1. How are active employees spread across performance and potential?
2. Does each job level, from L1 Staff to L5 Executive, have someone ready to step up?
3. Where are good performers stuck long enough that they might leave?

The dashboard is meant for the People Development team and HR Business Partners day to day, for department heads planning their teams, and for the VP of HR who wants one view of the pipeline.

## Repo layout

```
├── Data/
│   ├── WA_Fn-UseC_-HR-Employee-Attrition - RAW.csv
│   └── HR_People_Dev_Ready - Processed.csv
├── EDA notebooks/
│   └── EDA.ipynb
├── ETL python/
│   └── ETL.py
├── Power BI dashboard/
│   ├── Succession_Planning.pbix
│   ├── Succession_Planning.pdf
│   └── dashboard.png
├── README.md
└── requirements.txt
```

The EDA happens in the notebook. `ETL.py` cleans the raw file, adds the derived columns and writes the processed CSV, which Power BI reads. If you can't open a .pbix file, the PDF export and the screenshot above show the same page.

## What the EDA turned up

The data was clean: no missing values, no duplicate IDs. I dropped three columns that hold the same value in every row (`EmployeeCount`, `Over18`, `StandardHours`). 1,233 people are still employed and 237 have left, so attrition is 16.1%.

The performance rating was the problem. Everyone is rated either 3 (84.6%) or 4 (15.4%), so a normal 3×3 grid would have an empty bottom row. Digging further, the rating turned out to follow the salary hike exactly: a hike of 11–19% always means a 3, and 20–25% always means a 4. So the hike is the only extra performance signal in the file.

Headcount also drops sharply after L2. By level it's 400, 482, 186, 101 and 64.

## Derived columns

| Column | Rule | Why |
| --- | --- | --- |
| `Performance_Tier` | `PerformanceRating × 10 + PercentSalaryHike`. High ≥ 58, Moderate 45–57, Developing < 45 | Gives the grid three rows. In this data it works out to hike bands of 11–14, 15–19 and 20–25% |
| `Potential_Tier` | `JobInvolvement` 4 = High, 3 = Moderate, 1–2 = Low | There's no potential assessment in the data, so involvement is the proxy. It holds up: attrition drops from 33.7% at involvement 1 to 9.0% at 4 |
| `Succession_Readiness` | Ready Now = High performance, High potential and at least 2 years in role. Ready in 1–2 Years = High or Moderate on both. Everyone else = Needs Development | The tenure rule keeps strong but brand new people from being pushed up too early |
| `Stagnation_Ratio` | `YearsSinceLastPromotion / (YearsInCurrentRole + 1)` | The +1 stops a divide by zero for people who just started their role |
| `Stagnation_Risk_Flag` | Active, 3+ years since last promotion, and not in the Developing tier | A plain threshold is easier for HR to act on than the ratio |

## What I found

The leadership bench is close to empty. Ready Now by level is L1 4, L2 10, L3 1, L4 1, L5 0, and the share who need development climbs from 66.5% at L1 to 79.7% at L5.

I expected the bottleneck to be converting good people into ready ones. It isn't. Only 19 people sit in the top box (High × High), and 16 of them are already Ready Now. The other 3 just haven't hit 2 years in role. The 112 people with high performance but moderate potential can't qualify at all under this rule. If the company wants more successors, the top box has to get bigger.

Half the company (631 people, 51%) sits in the middle of the grid with moderate potential and developing or moderate performance.

Stagnation isn't only an R&D issue. Sales has the highest rate (12.1%), then HR (11.8%), then R&D (9.8%). R&D has the most people in absolute terms, 81 of the 130.

One result surprised me. Potential tracks retention well: nobody in the Ready Now group left, against 17.3% of Needs Development. But people who met the stagnation rule left at 15.6%, which is basically the same as everyone else (16.2%). So the flag points at a risk worth watching. The data doesn't prove it yet.

## What I'd recommend

These are the short version of a 12-month plan. The targets are my proposals, not something the data hands you.

1. Widen the top box before chasing a Ready Now number. Start with a calibration session, because the tiers come from proxies and managers should confirm the names. Then assess the 160 people next to the top box properly. The 112 high performers with moderate potential get a career conversation and mentoring; the 48 high potential, moderate performers get monthly coaching against quarterly goals.
2. Name a successor for every L4 and L5 role. The first accelerated cohort would be the 54 Managers and 28 Senior Managers already rated Ready in 1–2 Years.
3. Talk to the 130 flagged employees within 60 days, Sales first because of the rate, then R&D because of the size. In R&D, a specialist career track (Senior Specialist, Principal, Distinguished) would give people somewhere to go without becoming managers. In Sales, 24 of the 43 are L2, so publishing clear L2-to-L3 criteria would help.
4. Stop giving everyone the same training. Right now it's about 2.8 sessions a year regardless of performance or potential. Individual Development Plans built on the 70-20-10 model would replace it, starting with the 368 people rated Ready in 1–2 Years.

What I'd track over the year: Ready Now from 16 to about 40, Ready Now at L3–L4 from 2 to 10, the top box from 19 to 40, and the stagnation flag down to 5% of active staff.

## Limitations

The dataset is fictional, and salary hike and job involvement are stand-ins, not real talent assessments. It's also a single snapshot, so there's no promotion history or role criticality to work with.

The counts shift with the cut-offs. Setting stagnation at 2, 3, 4 or 5 years flags 194, 130, 109 or 88 people. Requiring 1 or 3 years in role instead of 2 gives 17 or 13 Ready Now instead of 16.

Next I want to build an attrition model to check which factors really predict leaving, and turn the cut-offs into Power BI what-if parameters so users can move them.

## Running it

```bash
pip install -r requirements.txt
python "ETL python/ETL.py"
```

`ETL.py` reads `Data/WA_Fn-UseC_-HR-Employee-Attrition - RAW.csv` and writes `Data/HR_People_Dev_Ready - Processed.csv`. Then open `Power BI dashboard/Succession_Planning.pbix` in Power BI Desktop and point the data source at the processed file.
