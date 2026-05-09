from ui import UITrainingApp as UI



class TrainingApp:
    def __init__(self):
        ui_settings = {
            "title": "Training",
        }

        self.ui = UI(ui_settings)


    def run(self):
        self.ui.start_ui()



if __name__ == '__main__':
    app = TrainingApp()
    app.run()
