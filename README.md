# Fantasy Football ML Project

Predicts next-season fantasy football production and generates draft rankings for the upcoming NFL season, using historical player stats and a stacked ensemble of models feeding into a Keras neural network.

## Overview

For each offensive skill position (QB, RB, TE, WR), this project:

1. Pulls historical player-season stats and biographical data via [`nflreadpy`](https://github.com/nflverse/nflreadpy).
2. Engineers position-specific features (efficiency ratios, age, years of experience, draft capital, year-over-year trends, etc.).
3. Pairs each player's season stats with their **following** season's fantasy output, turning the problem into a supervised "predict next year from this year" regression task.
4. Builds a stacked ensemble: Linear Regression, SGD Regression, KNN, and Gradient Boosting.  Whose out-of-fold predictions are fed as additional features into two neural network architectures (a simple feed-forward network and a wide & deep network).
5. Evaluates both networks on validation data using RMSE and Spearman rank correlation, and blends their predictions for the final output.
6. Applies the trained pipeline to the most recent season's stats to produce **rankings for the upcoming season**, adjusted for positional scarcity (Value Over Replacement Player) so QBs, RBs, TEs, and WRs can be compared on a single draft board.

## Data

Data is sourced from [`nflreadpy`](https://pypi.org/project/nflreadpy/), which provides play-by-play-derived season stats (`load_player_stats`) and player biographical/draft data (`load_players`), joined on each player's `gsis_id`.

Each position group uses a tailored feature set:

- **QB**: completions, attempts, passing yards/TDs/INTs, sacks, EPA, CPOE, rushing stats, plus derived ratios (completion %, yards/attempt, TD rate, sacks/game) and biographical/draft features.
- **RB / TE / WR** (combined "skill position" columns): carries, targets, receptions, receiving/rushing yards and TDs, target share, air yards share, WOPR, RACR, plus derived ratios (yards/carry, yards/target, catch rate) and the same biographical/draft features.

Shared, position-agnostic features engineered on the full dataset before splitting by position:
- **Age** — derived from `birth_date` and `season`.
- **Years of experience** — derived from each player's first appearance in the dataset.
- **Draft capital** — `draft_round` / `draft_pick`, with undrafted players flagged (`was_drafted`) and given a finite sentinel value rather than a null, so they're treated as "worse than any drafted player" without breaking scaling/imputation.
- **CPOE availability flag** — CPOE (completion % over expected) is only tracked league-wide from the Next Gen Stats era onward, so missing values are filled with 0 (a neutral value) and flagged with `has_cpoe_data`.

## Modeling Pipeline

Data is split **chronologically** (not randomly) into train / validation / test sets by season, so the model is always evaluated on seasons it hasn't seen — a more realistic test of forecasting a genuinely future season than a random split would be.

1. **Preprocessing** — median imputation + standard scaling, fit only on the training set and applied (never re-fit) to validation and test data to avoid leakage.
2. **Clustering features** — PCA followed by KMeans (best cluster count chosen via silhouette score) adds each player's distance to learned statistical archetypes as additional features.
3. **Stacked base models** — Linear Regression, SGD Regression, K-Nearest Neighbors, and Gradient Boosting Regressor are each tuned via `RandomizedSearchCV` and contribute out-of-fold predictions as meta-features.
4. **Neural networks** — a simple feed-forward network and a wide & deep network (raw features as the "wide" input, engineered/stacked features through hidden layers as the "deep" input) are both trained with `EarlyStopping`, L2 regularization, and dropout.
5. **Model selection & blending** — the two networks are compared on validation Spearman rank correlation (a better proxy for draft-relevant ranking accuracy than RMSE alone), and their predictions are blended for the final output.
6. **Positional scarcity adjustment (VORP)** — since each position has its own scoring scale, raw predicted points aren't directly comparable across positions (QBs inherently score more raw points than RBs). Final cross-position rankings are computed using Value Over Replacement Player, so positional scarcity is reflected in the draft board rather than just raw predicted totals.

## Repository Structure

```
.
├── model_building.ipynb   # Full pipeline: data loading, feature engineering, stacking, NN training, rankings
├── pyproject.toml         # Project dependencies (managed with uv)
└── uv.lock                # Locked dependency versions
```

## Setup

This project uses [`uv`](https://docs.astral.sh/uv/) for dependency management.

```bash
git clone https://github.com/loganmoser/Fantasy-Football-ML-Project.git
cd Fantasy-Football-ML-Project
uv sync
```

## Usage

The entire pipeline, pulling data via `nflreadpy`, feature engineering, model training, evaluation, and ranking generation runs from `model_building.ipynb`. Open it with Jupyter to step through or re-run the analysis:
```bash
uv run jupyter notebook model_building.ipynb
```

## Notes & Limitations

- Predictions rely entirely on the prior season's box-score stats and biographical/draft data, they don't account for offseason changes like team context, coaching changes, depth chart battles, or injuries that happen after the most recent season's data was collected.
- Rookies and players with no prior-season stats in the dataset can't be ranked with this pipeline, since it requires a full season of historical stats as input.
- Rankings should be treated as one data point among many for draft prep, not a substitute for up-to-date news, ADP, or beat-writer analysis closer to the season.
