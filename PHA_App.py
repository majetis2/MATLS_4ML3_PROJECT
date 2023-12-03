import kivy
from kivy.metrics import dp
from kivymd.app import MDApp
from kivy.config import Config
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.core.window import Window
from kivy.core.text import LabelBase
from kivymd.uix.screen import MDScreen
from kivymd.uix.toolbar import MDToolbar
from kivymd.uix.boxlayout import BoxLayout
from kivymd.uix.button import MDFillRoundFlatButton
from kivy.uix.filechooser import FileChooserListView
from kivy.uix.screenmanager import Screen, ScreenManager

import tkinter as tk
from tkinter import filedialog

import PHA_App_Backend as backend

import warnings

warnings.filterwarnings('ignore')

# Register the Ubuntu font
LabelBase.register(name="Ubuntu",
                   fn_regular=r"Ubuntu-Regular.ttf",
                   fn_bold=r"Ubuntu-Bold.ttf")

# Set the window size to a fixed width and height
kivy.config.Config.set('graphics', 'resizable', '0')
kivy.config.Config.set('graphics', 'width', 1280)
kivy.config.Config.set('graphics', 'height', 800)

class MDCustomFillRoundFlatButton(MDFillRoundFlatButton):
    def __init__(self, label_color=(0, 0, 0, 1), label_text_color = '#000000', **kwargs):
        super().__init__(**kwargs)

        self.width = 500
        self.height = 100

        self.md_bg_color = [0.85, 0.85, 0.85, 1]  # D9D9D9

        # Create a label with center-aligned text and add it to the button
        label = Label(
            text = f"[color={label_text_color}][b]{self.text}[/b]",
            markup = True,
            font_name = "Ubuntu",
            font_size = 40,
            size_hint = (None, None),
            halign = "center",  # Set text alignment to center
            valign = "middle",  # Set vertical alignment to middle
        )

        self.text = ""

        label.width = self.width
        label.height = self.height

        self.add_widget(label)


class MDSections(MDFillRoundFlatButton):
    def __init__(self, label_color=[0.0, 0.0, 0.0, 1.0], **kwargs):
        super().__init__(**kwargs)

        self.width = 1200
        self.height = 650

        self.md_bg_color = [0.85, 0.85, 0.85, 1]  # D9D9D9

        # Create a label with center-aligned text and add it to the button
        label = Label(
            text = f"[color=#000000][b]{self.text}[/b]",
            markup = True,
            font_name = "Ubuntu",
            font_size = 25,
            size_hint = (None, None),
            halign = "left",  # Set text alignment to center
            valign = "top",  # Set vertical alignment to middle
        )

        self.text = ""

        label.text_size = (self.width, self.height)
        label.width = self.width
        label.height = self.height

        self.add_widget(label)

class HomeScreen(Screen):

    text_status = "PREDICTION"
    uploaded = False
    label_text_color = "#000000"

    def upload_data(self, instance):
        ## NEED TO USE EXTERNAL FUNCTIONS TO USE THIS DATA
        # Create a root window
        root = tk.Tk()
        root.withdraw()  # Hide the root window

        # Open a file dialog for selecting files
        file_paths = filedialog.askopenfilename(
            title="Select files", filetypes=[("Excel Files", "*.xlsx")]
        )

        # Process the selected file(s)
        if file_paths:
            print("Selected file(s):", file_paths)
            backend.send_csv(file_paths)
            self.uploaded = True

        # Close the root window
        root.destroy()

    def get_prediction(self, instance):
        ## NEED TO CALL EXTERNAL FUNCTIONS TO GET THE PREDICTION
        # ERROR HANDLING => CAN ONLY PREDICT IF DATA CAN BE LOADED

        if self.uploaded:
            self.text_status = backend.compute_prediction()

            self.label_text_color = '#FF0000' if self.text_status == 'HAZARDOUS' else '#006400' if self.text_status == 'NON-HAZARDOUS' else '#000000'

            self.prediction_output_button = MDCustomFillRoundFlatButton(text = self.text_status,
                size_hint = (None, None),  # Allow you to set the size directly
                width = dp(200),
                pos_hint = {"center_x": 0.5, "center_y": 0.75},
                label_text_color = self.label_text_color
            )

            self.prediction_output_button.disabled = True

            self.add_widget(self.prediction_output_button)

            self.uploaded = False

    def on_enter(self):
        self.prediction_output_button = MDCustomFillRoundFlatButton(text = self.text_status,
            size_hint = (None, None),  # Allow you to set the size directly
            width = dp(200),
            pos_hint = {"center_x": 0.5, "center_y": 0.75},
            label_text_color = self.label_text_color
        )

        self.prediction_output_button.disabled = True

        self.add_widget(self.prediction_output_button)

        # upload data button
        self.upload_data_button = MDCustomFillRoundFlatButton(text = "UPLOAD DATA",
            size_hint = (None, None),  # Allow you to set the size directly
            width = dp(200),
            pos_hint = {"center_x": 0.5, "center_y": 0.55},
            on_press=self.upload_data

        )

        self.add_widget(self.upload_data_button)

        # predict button
        self.predict_button = MDCustomFillRoundFlatButton(text="PREDICT",
            size_hint = (None, None),  # Allow you to set the size directly
            width=dp(200),
            pos_hint={"center_x": 0.5, "center_y": 0.35},
            on_press=self.get_prediction
        )

        self.add_widget(self.predict_button)

    def on_leave(self):
        self.prediction_output_button = MDCustomFillRoundFlatButton(text = self.text_status,
            size_hint = (None, None),  # Allow you to set the size directly
            width = dp(200),
            pos_hint = {"center_x": 0.5, "center_y": 0.75},
            label_text_color = self.label_text_color
        )

        self.prediction_output_button.disabled = True

        self.add_widget(self.prediction_output_button)

class AboutScreen(Screen):
    def on_enter(self):
        # About Section
        self.about_section = MDSections(text = "\n About Section Needs To Be Filled \n",
            size_hint = (None, None),  # Allow you to set the size directly
            width = dp(200),
            pos_hint = {"center_x": 0.5, "center_y": 0.55}
        )

        self.about_section.disabled = True

        self.add_widget(self.about_section)

class InstructionsScreen(Screen):
    def on_enter(self):
        # Instructions Section
        self.instructions_section = MDSections(text = "\n Instructions Section Needs To Be Filled \n",
            size_hint = (None, None),  # Allow you to set the size directly
            width = dp(200),
            pos_hint = {"center_x": 0.5, "center_y": 0.55}

        )

        self.instructions_section.disabled = True

        self.add_widget(self.instructions_section)

class PHAApp(MDApp):
    def flip(self):
        screen_name = self.screen_manager.current

        if (screen_name == 'Home'):
            self.home_screen.text_status = "PREDICTION"

            self.home_screen.label_text_color = '#000000'

            self.home_screen.prediction_output_button = MDCustomFillRoundFlatButton(text = self.home_screen.text_status,
                size_hint = (None, None),  # Allow you to set the size directly
                width = dp(200),
                pos_hint = {"center_x": 0.5, "center_y": 0.75},
                label_text_color = self.home_screen.label_text_color
            )

            self.home_screen.prediction_output_button.disabled = True

            self.home_screen.add_widget(self.home_screen.prediction_output_button)

    def build(self):
        Window.size = (1280,800)

        self.screen = MDScreen()

        # Change the background color to #270C2A
        self.screen.md_bg_color = [0.0941, 0.0471, 0.1647, 1] # 270C2A

        layout = BoxLayout(orientation='vertical')

        self.image = Image(
            source = 'bakground_transparent_earth.png',
            allow_stretch = True,
            keep_ratio = True,
            size_hint = (1, None)
        )

        self.image.height = 600
        self.image.width = 800
        self.image.pos_hint = {'center_x': 0.5, 'y': 0}

        layout.add_widget(self.image)

        self.screen.add_widget(layout)

        self.screen_manager = ScreenManager()

        self.home_screen = HomeScreen(name = 'Home')
        self.about_screen = AboutScreen(name = 'About')
        self.instructions_screen = InstructionsScreen(name = 'Instructions')

        self.screen_manager.add_widget(self.home_screen)
        self.screen_manager.add_widget(self.about_screen)
        self.screen_manager.add_widget(self.instructions_screen)

        self.toolbar = MDToolbar(title = "PHA PREDICTOR", anchor_title = "center")
        self.toolbar.title_size = 32
        self.toolbar.font_name = "Ubuntu"
        self.toolbar.pos_hint = {"top": 1}
        self.toolbar.left_action_items = [["home", lambda x: self.show_screen('Home')],
                                    ["book-open-variant", lambda x: self.show_screen('About')]]
        self.toolbar.right_action_items = [["information-outline", lambda x: self.show_screen('Instructions')],
                                     ["rotate-3d-variant", lambda x: self.flip()]]
        self.toolbar.md_bg_color = [0, 0, 0, 0]

        self.screen.add_widget(self.toolbar)
        self.screen.add_widget(self.screen_manager)

        # Set the home page as the initial screen
        self.screen_manager.current = 'Home'

        return self.screen

    def show_screen(self, screen_name):
        self.screen_manager.current = screen_name

        # Update the toolbar title based on the selected screen
        if screen_name == 'Home':
            self.toolbar.title = "PHA PREDICTOR"
        elif screen_name == 'About':
            self.toolbar.title = "ABOUT"
            #self.screen.remove_widget(self.prediction_output_button)
        elif screen_name == 'Instructions':
            self.toolbar.title = "INSTRUCTIONS"
            #self.screen.remove_widget(self.prediction_output_button)

if __name__ == '__main__':
    PHAApp().run()
