# Hand Labeling Plots: A Quest Project

  ## Overview

  This Python script allows users to interact with a plot displaying eye movements in three directions (x, y, z) over time. The plot consists of three separate subplots aligned vertically along the y-axis, with time represented on the x-axis. Users can label and highlight regions of interest, edit or remove highlights and labels, and zoom in or out for better precision. The highlighted regions and their labels are saved to a CSV file, and the figures can be saved separately.

  ## Dependencies
- `matplotlib`
- `pandas`

## Example Usage 

To use the script, run it and follow the prompts to enter the file path for the plot, the output path to indicate the location for saving the CSV file, and the participant code for ease of use. At this point, a plot will be displayed and you can interact with the plot to highlight regions. After each mouse left click and release, you will be prompted to enter the label of the highlighted area. Moreover, you can edit the labels by right-clicking on any of the highlighted areas and either entering a new label or removing the highlight and label by simply leaving the prompt without a new entry. Furthermore, you can use the scroll button to zoom in and out of the plot. 
The highlights and their labels will be saved to a CSV file specified by the user. 






