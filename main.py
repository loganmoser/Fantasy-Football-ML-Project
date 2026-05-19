import nflreadpy
import polars as pl

def main():
    # Load player data for training models
    player_data = nflreadpy.load_player_stats(seasons=2025, summary_level="reg")

    # Select unnecessary columns
    drop_columns = ["headshot_url", "season_type", "gwfg_made", "gwfg_att", "gwfg_missed",
                    "gwfg_blocked", "def_tackles_solo", "def_tackles_with_assist",
                    "def_tackle_assists", "def_tackles_for_loss", "def_tackles_for_loss_yards",
                    "def_fumbles_forced", "def_sacks", "def_sack_yards", "def_qb_hits",
                    "def_interceptions", "def_interception_yards", "def_pass_defended",
                    "def_tds", "def_fumbles", "def_safeties", "punt_returns", "fumble_recovery_own",
                    "fumble_recovery_yards_own", "fumble_recovery_opp", "fumble_recovery_yards_opp",
                    "fumble_recovery_tds", "punt_return_yards", "kickoff_returns", "kickoff_return_yards"]

    player_data_cleaned = player_data.drop(drop_columns)
    # Positional columns
    qb_cols = ["player_name", "completions", "attempts", "passing_yards", "passing_tds",
               "passing_interceptions", "sacks_suffered", "sack_yards_lost", "sack_fumbles",
               "sack_fumbles_lost", "passing_air_yards", "passing_yards_after_catch",
               "passing_first_downs", "passing_epa", "passing_cpoe", "passing_2pt_conversions",
               "pacr", "carries", "rushing_yards", "rushing_tds", "rushing_fumbles",
               "rushing_fumbles_lost", "rushing_first_downs", "rushing_epa",
               "rushing_2pt_conversions"]
    # RBs, TEs, and WRs had many similar columns so they are combined into skill-position columns
    sp_cols = ["player_name", "carries", "rushing_yards", "rushing_tds", "rushing_fumbles", 
               "rushing_fumbles_lost", "rushing_first_downs", "rushing_epa", "rushing_2pt_conversions",
               "receptions", "targets", "receiving_yards", "receiving_tds", "receiving_fumbles",
               "receiving_fumbles_lost", "receiving_air_yards", "receiving_yards_after_catch",
               "receiving_first_downs", "receiving_epa", "receiving_2pt_conversions", "racr",
               "target_share", "air_yards_share", "wopr"]
   

    # Group players by position to build positional models
    qbs = player_data_cleaned.filter(pl.col('position') == 'QB')
    rbs = player_data_cleaned.filter(pl.col('position') == 'RB')
    tes = player_data_cleaned.filter(pl.col('position') == 'TE')
    wrs = player_data_cleaned.filter(pl.col('position') == 'WR')



if __name__ == "__main__":
    main()
