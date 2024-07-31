from tkinter import Tk, Label, Button, Canvas
import cv2
import os

root = Tk()
root.title("OCT-A Wizard by BioStemCore")

root.geometry("960x480")

# Create a menu section
menu_label = Label(root, text="Select Application:")
menu_label.pack()

def open_image_cropper():
  # Create a new window for image cropping
  def crop_image(image_path):
    # Load the image
    image = cv2.imread(image_path)
    
    # Create a new window for image cropping
    image_cropper_window = Tk()
    image_cropper_window.title("Image Cropper")
    image_cropper_window.geometry("1920x1080")
    
    # Create a canvas to display the image
    canvas = Canvas(image_cropper_window, width=1920, height=1080)
    canvas.pack()
    
    # Display the image on the canvas
    canvas.create_image(0, 0, anchor="nw", image=image)
    
    # Create a list to store the selected rectangles
    selected_rectangles = []
    
   
    instructions_label = Label(image_cropper_window, text="Click and drag to select a rectangle")
    instructions_label.pack()

    # Create a button to start the cropping process
    crop_button = Button(image_cropper_window, text="Crop Image", command=lambda: crop_image(image_path, selected_rectangles))
    crop_button.pack()

    # Function to handle mouse button press event
    def start_dragging(event):
      global dragging
      dragging = True
      x_start, y_start = event.x, event.y
      selected_rectangles.append((x_start, y_start, x_start, y_start))
    
    # Function to handle mouse motion event
    def draw_rectangle(event):
      global dragging
      if dragging:
        x_end, y_end = event.x, event.y
        selected_rectangles[-1] = (selected_rectangles[-1][0], selected_rectangles[-1][1], x_end, y_end)
        canvas.coords("rectangle", *selected_rectangles[-1])
    
    # Function to handle mouse button release event
    def release_mouse(event):
      global dragging
      dragging = False
    
    # Bind the canvas events to the corresponding functions
    canvas.bind("<Button-1>", start_dragging)
    canvas.bind("<B1-Motion>", draw_rectangle)
    canvas.bind("<ButtonRelease-1>", release_mouse)

    image_cropper_window.mainloop()

def select_application(app):
  if app == "OCTAVA":
    # Add code for OCTAVA application
    pass
  elif app == "IMAGE CROPPER":
    open_image_cropper()
    
  elif app == "PIXEL SIZE GENERATOR":
    # Add code for PIXEL SIZE GENERATOR application
    pass

# Create menu buttons
octava_button = Button(root, text="OCTAVA", command=lambda: select_application("OCTAVA"))
octava_button.pack()

image_cropper_button = Button(root, text="IMAGE CROPPER", command=lambda: select_application("IMAGE CROPPER"))
image_cropper_button.pack()

pixel_size_generator_button = Button(root, text="PIXEL SIZE GENERATOR", command=lambda: select_application("PIXEL SIZE GENERATOR"))
pixel_size_generator_button.pack()

root.mainloop()
