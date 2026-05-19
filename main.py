import nflreadpy

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

    print(player_data_cleaned) 

if __name__ == "__main__":
    main()
