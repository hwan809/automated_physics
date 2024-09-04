import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit,
    QPushButton, QListView, QFileDialog, QMessageBox
)
from PyQt5.QtCore import QStringListModel
from response import create_hwp
import json

import warnings
warnings.filterwarnings('ignore')

class ReportGenerator(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("물리학 실험 보고서 제작기")
        self.setGeometry(100, 100, 400, 400)

        self.layout = QVBoxLayout()

        # 팀명 입력
        self.team_name_label = QLabel("팀명:")
        self.layout.addWidget(self.team_name_label)
        self.team_name_input = QLineEdit()
        self.layout.addWidget(self.team_name_input)
        self.team_name_button = QPushButton("확인")
        self.team_name_button.clicked.connect(self.confirm_team_name)
        self.layout.addWidget(self.team_name_button)

        self.team_name_input.returnPressed.connect(self.confirm_team_name)

        # 팀 구성원 입력
        self.team_members_label = QLabel("팀 구성원:")
        self.layout.addWidget(self.team_members_label)
        self.team_members_input = QLineEdit()
        self.layout.addWidget(self.team_members_input)
        self.team_members_button = QPushButton("확인")
        self.team_members_button.clicked.connect(self.add_team_members)
        self.layout.addWidget(self.team_members_button)

        self.team_members_input.returnPressed.connect(self.add_team_members)

        # 팀 구성원 리스트
        self.team_members_list = QListView()
        self.team_members_model = QStringListModel()
        self.team_members_list.setModel(self.team_members_model)
        self.layout.addWidget(self.team_members_list)

        # 탐구 주제 입력
        self.research_topic_label = QLabel("탐구 주제:")
        self.layout.addWidget(self.research_topic_label)
        self.research_topic_input = QLineEdit()
        self.layout.addWidget(self.research_topic_input)
        self.research_topic_button = QPushButton("확인")
        self.research_topic_button.clicked.connect(self.confirm_research_topic)
        self.layout.addWidget(self.research_topic_button)

        self.research_topic_input.returnPressed.connect(self.confirm_research_topic)

        # 이미지 업로드 버튼
        self.upload_image_button = QPushButton("이미지 업로드")
        self.upload_image_button.clicked.connect(self.upload_image)
        self.layout.addWidget(self.upload_image_button)

        # 생성하기 버튼
        self.create_button = QPushButton("생성하기")
        self.create_button.clicked.connect(self.create_hwp)
        self.create_button.setStyleSheet("font-size: 18px; padding: 10px;")  # 버튼 크기 조정
        self.layout.addWidget(self.create_button)

        # 크레딧
        self.credit_label = QLabel("By. 환. 송T 존경합니다.")
        self.credit_label.setStyleSheet("font-size: 14px; text-align: center; margin-top: 20px;")
        self.layout.addWidget(self.credit_label)

        self.setLayout(self.layout)

        self.team_members = []

        self.team_name = ''
        self.file_name = ''
        self.research_topic = ''

        self.load_team_info()

    def load_team_info(self):
        try:
            with open('resource/team_info.json', 'r', encoding='utf-8') as f:
                team_info = json.load(f)
                self.team_name_input.setText(team_info.get("team_name", ""))
                self.team_members = team_info.get("members", [])
                self.team_members_model.setStringList(self.team_members)
        except FileNotFoundError:
            # 파일이 없으면 무시
            pass
        except json.JSONDecodeError:
            QMessageBox.warning(self, "파일 오류", "팀 정보 파일이 손상되었습니다.")

    def confirm_team_name(self):
        self.team_name = self.team_name_input.text()
        QMessageBox.information(self, "팀명 확인", f"팀명: {self.team_name}")

    def add_team_members(self):
        members_input = self.team_members_input.text()
        if members_input:
            # 쉼표로 구분된 팀원 이름을 리스트로 변환
            new_members = [member.strip() for member in members_input.split(',')]
            self.team_members = (new_members)
            self.team_members_model.setStringList(self.team_members)
            self.team_members_input.clear()
        else:
            QMessageBox.warning(self, "입력 오류", "팀 구성원을 입력하세요.")

    def confirm_research_topic(self):
        self.research_topic = self.research_topic_input.text()
        QMessageBox.information(self, "탐구 주제 확인", f"탐구 주제: {self.research_topic}")

    def closeEvent(self, event):
        team_name = self.team_name_input.text()
        if team_name and self.team_members:
            team_info = {
                "team_name": team_name,
                "members": self.team_members
            }
            # 자동으로 team_info.json 파일에 저장
            with open('resource/team_info.json', 'w', encoding='utf-8') as f:
                json.dump(team_info, f, ensure_ascii=False, indent=4)
            QMessageBox.information(self, "저장 완료", "팀 정보가 team_info.json에 저장되었습니다.")
        event.accept()  # 종료 이벤트를 허용합니다.
    
    def upload_image(self):
        options = QFileDialog.Options()
        self.file_name, _ = QFileDialog.getOpenFileName(self, "이미지 선택", "", "Images (*.png *.jpg *.jpeg *.bmp);;All Files (*)", options=options)
        if self.file_name:
            QMessageBox.information(self, "이미지 업로드", f"업로드된 이미지: {self.file_name}")

    def create_hwp(self):
        if not self.team_name:  
            QMessageBox.warning(self, "입력 오류", "팀명을 입력하세요.")
            return
        if not self.team_members:  
            QMessageBox.warning(self, "입력 오류", "팀 구성원을 입력하세요.")
            return
        if not self.research_topic:  
            QMessageBox.warning(self, "입력 오류", "탐구 주제를 입력하세요.")
            return
        if not self.file_name:  
            QMessageBox.warning(self, "입력 오류", "이미지를 선택하세요.")
            return
        
        QMessageBox.warning(self, "보고서 생성 시작", "- 30초 정도 소요됩니다.\n- 한글 파일을 조작하지 마세요.\n -종료 창이 뜨면 '저장 안함' 을 선택하세요.")
        create_hwp(self.team_name, self.team_members, self.research_topic, self.file_name, openai_api_key)
        QMessageBox.warning(self, "제작 완료", "output 폴더를 확인하세요.")

openai_api_key = ''

if __name__ == "__main__":
    openai_api_key = input('제공받은 API Key를 입력하세요: ')

    app = QApplication(sys.argv)
    window = ReportGenerator()
    window.show()
    sys.exit(app.exec_())