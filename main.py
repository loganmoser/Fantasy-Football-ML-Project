import nflreadpy

def main():
    player_data = nflreadpy.load_player_stats(seasons=2025, summary_level="reg")

    print(player_data)
if __name__ == "__main__":
    main()
