import matplotlib
import matplotlib.pyplot as plt
import pandas as pd
matplotlib.use('Qt5Agg')




class Highlight:
    def __init__(self, axes, output_path, output_name):

        self.axes = axes
        self.output_name = output_name
        self.output_path = output_path
        self.position_one = None
        self.time_one = None
        self.position_two = None
        self.time_two = None
        self.label = None
        self.label_location = []
        self.cid_press = [ax.figure.canvas.mpl_connect('button_press_event', self.mouse_press) for ax in self.axes]
        self.cid_release = [ax.figure.canvas.mpl_connect('button_release_event', self.mouse_release) for ax in
                            self.axes]

    def mouse_press(self, event):
        self.position_one = (event.xdata)
        self.time_one = (event.ydata)

    def mouse_release(self, event):
        self.position_two = (event.xdata)
        self.time_two = (event.ydata)
        if self.position_one and self.position_two:
            for ax in self.axes:
                ax.axvspan(self.position_one, self.position_two, color="red", alpha=0.3)
            self.label = input("Please enter the label: ")
            self.label_location.append([self.position_one, self.time_one, self.position_two, self.time_two, self.label])
            print(self.label_location)


            event.canvas.draw()
            self.save_to_csv()

    def save_to_csv(self):
        label_location_df = pd.DataFrame(self.label_location, columns=["time_one", "position_one", "time_two",  "position_two", "label"])
        label_location_df.to_csv(f"{self.output_path}/{self.output_name}.csv", index=False)

    def disconnect_events(self):
        for cid_press, cid_release in zip(self.cid_press, self.cid_release):
            for ax in self.axes:
                ax.figure.canvas.mpl_disconnect(cid_press)
                ax.figure.canvas.mpl_disconnect(cid_release)




if __name__ == "__main__":

    file_path = input("Please enter the file path: ")  # Prompting for the CSV file path
    output_path= input("Please enter the output path: ")
    participant_code = input("Please enter the participant code: ")
    output_name = str("output" + participant_code)  # Prompting for the participant code
    df = pd.read_csv(file_path)  # Reading the CSV file
    figsize = (100, 20)  # Setting the figure size
    fig, ax = plt.subplots(3, 1, sharex=True,
                           figsize=figsize)  # Creating a figure with 3 subplots for x, y, and z coordinates
    fig.subplots_adjust(hspace=0)
    ax[0].plot(df["time"], df["xcoord"])
    ax[0].set_ylabel('xcoord')
    ax[1].plot(df["time"], df["ycoord"])
    ax[1].set_ylabel('ycoord')
    ax[2].plot(df["time"], df["zcoord"])
    ax[2].set_ylabel('zcoord')
    highlighter = Highlight(ax, output_path, output_name, )
    highlighter.save_to_csv()


    plt.show()
