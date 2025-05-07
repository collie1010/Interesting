import sys
import time
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                            QLabel, QScrollArea)
from PyQt6.QtCore import QTimer, Qt
from nba_api.live.nba.endpoints import ScoreBoard, playbyplay

class NBALiveScores(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("NBA Live Scores")
        self.setMinimumSize(800, 600)

        # 建立主要的 widget 和布局
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        self.main_layout = QVBoxLayout(main_widget)

        # 建立滾動區域
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        self.scroll_widget = QWidget()
        self.scroll_layout = QVBoxLayout(self.scroll_widget)
        scroll.setWidget(self.scroll_widget)
        self.main_layout.addWidget(scroll)

        # 更新時間標籤
        self.update_time_label = QLabel()
        self.update_time_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.main_layout.addWidget(self.update_time_label)

        # 設定樣式
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f0f0f0;
            }
            QLabel {
                padding: 5px;
                font-family: Arial;
            }
            .game-card {
                background-color: white;
                border-radius: 10px;
                padding: 20px;
                margin: 10px;
            }
            .score-label {
                font-size: 24px;
                font-weight: bold;
            }
            .status-label {
                color: #666;
                font-size: 14px;
            }
            .play-label {
                color: #333;
                padding: 5px;
                border-bottom: 1px solid #eee;
            }
        """)

        # 設定定時器進行更新
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_scores)
        self.timer.start(15000)  # 每15秒更新一次

        # 初始化顯示
        self.update_scores()

    def fetch_live_games(self):
        scoreboard = ScoreBoard()
        games = scoreboard.games.get_dict()
        return [game for game in games if game['gameStatus'] == 2]

    def fetch_play_by_play(self, game_id):
        pbp = playbyplay.PlayByPlay(game_id=game_id)
        return pbp.get_dict()['game']['actions']

    def clear_layout(self, layout):
        while layout.count():
            child = layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

    def update_scores(self):
        # 清除現有的比分顯示
        self.clear_layout(self.scroll_layout)

        live_games = self.fetch_live_games()

        if not live_games:
            no_games_label = QLabel("No live games currently.")
            no_games_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.scroll_layout.addWidget(no_games_label)
        else:
            for game in live_games:
                # 建立比賽卡片容器
                game_card = QWidget()
                game_card.setProperty('class', 'game-card')
                game_layout = QVBoxLayout(game_card)

                # 比分顯示
                score_label = QLabel(
                    f"{game['awayTeam']['teamName']} {game['awayTeam']['score']} - "
                    f"{game['homeTeam']['score']} {game['homeTeam']['teamName']}"
                )
                score_label.setProperty('class', 'score-label')
                score_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
                game_layout.addWidget(score_label)

                # 比賽狀態
                status_label = QLabel(game['gameStatusText'])
                status_label.setProperty('class', 'status-label')
                status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
                game_layout.addWidget(status_label)

                # 最近比賽動作
                plays = self.fetch_play_by_play(game['gameId'])
                latest_plays = plays[-6:]
                
                plays_label = QLabel("Latest Plays:")
                plays_label.setProperty('class', 'plays-header')
                game_layout.addWidget(plays_label)

                for play in reversed(latest_plays):
                    description = play['description']
                    if 'teamTricode' in play:
                        description = f"{play['teamTricode']}: {description}"
                    
                    play_label = QLabel(description)
                    play_label.setProperty('class', 'play-label')
                    play_label.setWordWrap(True)
                    game_layout.addWidget(play_label)

                self.scroll_layout.addWidget(game_card)

        # 更新時間標籤
        current_time = time.strftime("%H:%M:%S")
        self.update_time_label.setText(f"Last Updated: {current_time}")

def main():
    app = QApplication(sys.argv)
    window = NBALiveScores()
    window.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()

