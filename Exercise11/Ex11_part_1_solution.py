import sys

from PyQt5.QtWidgets import (QApplication, QPushButton, QWidget,QMainWindow,
                             QFileDialog, QGridLayout, QLabel, QVBoxLayout, QHBoxLayout, QMessageBox, QComboBox)

import pyqtgraph as pg
import json
import imageio.v2 as io


class MyApp(QMainWindow):
    def __init__(self):
        super().__init__()

        ## Run the function to set defaults
        self.set_defaults()

        # Creating a CentralWidget
        w = QWidget(self)
        self.setCentralWidget(w) # QMainWindow takes ownership of the widget pointer and deletes it at the appropriate time.
        self.mainLayout = QVBoxLayout()
        w.setLayout(self.mainLayout)

        # setting the minimum size
        self.setMinimumSize(250, 300)
        #self.setMaximumSize(1920, 1080)
        
        ####------- DROPDOWNS -------####

        # 1. Create a BoxLayout that will contain the Dropdown(s)
        self.dropdown_box = QVBoxLayout()

        # 2. Initialize the Dropdown that contains the available laguages:
        self.language_dropdown = DropDown(self.available_languages) # Create a Dropdown that displays the available languages in our dictionary.
        self.language_dropdown.currentIndexChanged.connect(self.update_main_dropdown) #  Connect this dropdown with a function to update the window. 
        #                                                              # The function will be fed with the current index changed.
        self.language_dropdown.setCurrentIndex(self.index_language) # Set the default language for the GUI (from our json).

        # 3. Add the Dropdown to the Main Layout:
        self.mainLayout.addWidget(self.language_dropdown)

        # 4. Make a function to set-up and update the drop downs
        self.set_dropdowns()
        
        # 5. Add the Boxlayout containing the dropdowns to the Main Layout
        self.mainLayout.addLayout(self.dropdown_box)


        ####------- IMAGE WIDGET -------####
        self.image_viewer = Interface()
        self.mainLayout.addWidget(self.image_viewer)

        ####------- BUTTON -------####
        self.mainLayout.addWidget(self.open_button)

        ####------- Make the layout look better -------####
        self.mainLayout.addStretch(1)


    def update_main_dropdown(self, index): # update language
        self.index_language = index # define a global variable saving the index of the selected option
        self.language = self.available_languages[self.index_language] # define a variable containing the language of the given index
        self.setWindowTitle(self.options["available languages"][self.language]["window title"]) # Update the window title w.r.t the language selected
        self.open_button.setText(self.options["available languages"][self.language]["button"]) # Update the text of the button
        self.set_dropdowns() # update the other Dropdowns


    def set_dropdowns(self):
        ####---CLEAR---####
        self.clear_layouts(self.dropdown_box)

        ####---Label above the dropdown---####
        self.labels = QLabel()
        self.labels.setText(self.options["available languages"][self.language]["label"])
        # Add the label to our pre-assigned space for dropdown
        self.dropdown_box.addWidget(self.labels)

        ####---Set the first Dropdown ---####
        self.opt1dd = self.options["available languages"][self.language]["first_dropdown"]
        self.first_dd = DropDown(self.opt1dd)
        
        ####---Set the second Dropdown ---####
        self.opt2dd = self.options["available languages"][self.language]["second_dropdown"]
        self.second_dd = DropDown(self.opt2dd)

        ####---Create a Layout that organizes the dropdowns---####
        ## Do we want it horizontal or vertical?
        hbox = QHBoxLayout() # horizontal works better with our current application
        # Add the dropdowns to the layout
        hbox.addWidget(self.first_dd)
        hbox.addWidget(self.second_dd)

        # Add the layout to our pre-assigned space for dropdowns
        self.dropdown_box.addLayout(hbox)
        # Make it look better
        self.dropdown_box.addStretch(1)

 
    def set_defaults(self): ## Set default values for the application
        # Settings for the window:
        self.status = self.statusBar()
        self.status.showMessage("Ready")

        # Initialize the variable containing the image 
        self.im = None 

        ## Load the settings from the json file
        with open ("settings.json", "r") as jsonfile:
            self.options = json.load(jsonfile)

        ## Set window options (width, height)
        width = self.options["defaults"]["width"]
        height = self.options["defaults"]["height"]
        self.resize(width, height)
        
        
        # Settings with language
        ## Store the available languages, the default language and select the index of the default language
        self.available_languages = list(self.options["available languages"].keys()) # list: [english, deutsch]
        self.language = self.options["defaults"]["language"] ## english / deutsch
        self.index_language = self.available_languages.index(self.language)

        ## Change the window title depending on the default language
        self.setWindowTitle(self.options["available languages"][self.language]["window title"])

        ## Create a Button to save the image
        self.open_button = QPushButton() 
        self.open_button.setGeometry(300, 300, 350, 300)
        self.open_button.setText(self.options["available languages"][self.language]["button"])
        self.open_button.clicked.connect(self.open)
        
    ####----CLEAR WIDGETS----#### Think a way to clear properly!
    ### Clear items inside a Layout
    def clear_items(self, layout):
        if layout is not None:
            while layout.count():
                item = layout.takeAt(0)
                widget = item.widget()
                if widget is not None:
                    widget.setParent(None)
                else:
                    self.clear_items(item.layout())
    
    ### Clear layouts inside layouts 
    def clear_layouts(self, layout):
        self.clear_items(layout)
        for i in reversed (range(layout.count())):
            layout_item = layout.itemAt(i)
            self.clear_items(layout_item.layout())
            layout.removeItem(layout_item)

    ## Function to open and load an image
    def open(self):
        fn, _ = QFileDialog.getOpenFileName(filter="*.png *.jpg")

        if fn:
            self.status.showMessage(fn)
            self.im = io.imread(fn)
            self.image_viewer.imv.setImage(self.im)
            QMessageBox.information(self, 
            "file loaded", 
            "Image succesfully loaded!")
        else: 
            QMessageBox.critical(self, 
            "Meaningful error", 
            "Something went wrong!")

    ## We need to give some feedback to the user, don't we? :)
    def show_dialog(self, flag):
            msg = QMessageBox()
            if flag:
                msg.setIcon(QMessageBox.Critical)
                msg.setStandardButtons(QMessageBox.Ok)
                msg.setDefaultButton(QMessageBox.Retry)
                msg.setWindowTitle("Error")
                msg.setText("Error trying to save the image!")
                msg.setInformativeText("Image could not be saved")
                returnValue = msg.exec()
            else:
                msg.setWindowTitle("Info")
                msg.setText("Image was saved succesfully!")
                msg.setIcon(QMessageBox.Information)
                msg.setStandardButtons(QMessageBox.Ok)
                returnValue = msg.exec()
                
class Interface(QWidget):
    def __init__(self):
        super().__init__() #super() is used to refer the superclass from the subclass.

        # Initialize a QGridLayout
        self.grid_layout = QGridLayout(self)
        
        # Create an ImageView inside the central widget
        self.imv = pg.ImageView()
        self.grid_layout.addWidget(self.imv)
        
class DropDown(QComboBox):
    def __init__(self, items):
        super().__init__()
        self.items = items
        self.addItems(self.items)


def main():
    app = QApplication(sys.argv)
    window = MyApp()
    window.show()
    app.exec_()


if __name__ == '__main__':
    main()