from ui import UITrainingApp as UI



class TrainingApp:
    def __init__(self):
        ui_settings = {
            "title": "Training",
            'safe_area': False,
            'padding': 0,
            'spacing': 0,
        }

        self.ui = UI(ui_settings)


    def run(self):
        self.ui.start_ui()



if __name__ == '__main__':
    app = TrainingApp()
    app.run()
