import matplotlib
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.patches import Rectangle
from matplotlib.ticker import MaxNLocator
from matplotlib.backend_bases import MouseButton

matplotlib.use('Qt5Agg')

class Highlight:
    def __init__(self, axes, output_path, output_name):
        self.axes = axes
        self.output_name = output_name
        self.output_path = output_path
        self.highlights = []
        self.cid_press = [ax.figure.canvas.mpl_connect('button_press_event', self.mouse_press) for ax in self.axes]
        self.cid_release = [ax.figure.canvas.mpl_connect('button_release_event', self.mouse_release) for ax in self.axes]
        self.cid_scroll = [ax.figure.canvas.mpl_connect('scroll_event', self.on_scroll) for ax in self.axes]
        self.highlight_id_counter = 0

    def mouse_press(self, event):
        if event.inaxes not in self.axes:
            return

        if event.button == MouseButton.LEFT:
            self.start_position = (event.xdata, event.ydata)
        elif event.button == MouseButton.RIGHT:
            self.check_highlight_edit(event)

    def mouse_release(self, event):
        if event.inaxes not in self.axes or not hasattr(self, 'start_position'):
            return

        if event.button == MouseButton.LEFT:
            self.end_position = (event.xdata, event.ydata)
            if self.start_position and self.end_position:
                self.add_highlight(self.start_position, self.end_position)
                self.start_position, self.end_position = None, None

    def add_highlight(self, start, end):
        label = input("Please enter the label: ")
        highlight_id = self.highlight_id_counter
        self.highlight_id_counter += 1

        for ax in self.axes:
            ylim = ax.get_ylim()
            rect = Rectangle((min(start[0], end[0]), ylim[0]),
                             abs(end[0] - start[0]), ylim[1] - ylim[0],
                             color='red', alpha=0.3)
            ax.add_patch(rect)
            self.highlights.append((highlight_id, ax, rect, label, ylim))
            ax.figure.canvas.draw()
        self.save_to_csv()

    def check_highlight_edit(self, event):
        for highlight_id, ax, rect, label, ylim in self.highlights:
            if rect.contains_point((event.x, event.y)):
                self.selected_highlight = (highlight_id, rect, label)
                self.edit_highlight(highlight_id, label)
                break

    def edit_highlight(self, highlight_id, label):
        print(f"Editing label: {label}")
        new_label = input("Enter new label (leave blank to delete): ")
        if new_label.strip():
            for i, (hid, ax, rect, lbl, ylim) in enumerate(self.highlights):
                if hid == highlight_id:
                    self.highlights[i] = (hid, ax, rect, new_label, ylim)
        else:
            self.remove_highlight(highlight_id)
        self.save_to_csv()
        for ax in self.axes:
            ax.figure.canvas.draw()

    def remove_highlight(self, highlight_id):
        to_remove = [(ax, rect) for hid, ax, rect, lbl, ylim in self.highlights if hid == highlight_id]
        for ax, rect in to_remove:
            rect.remove()
        self.highlights = [h for h in self.highlights if h[0] != highlight_id]

    def save_to_csv(self):
        unique_highlights = {}
        for highlight_id, ax, rect, label, ylim in self.highlights:
            x0, y0 = rect.get_xy()
            x1 = x0 + rect.get_width()
            if highlight_id not in unique_highlights:
                unique_highlights[highlight_id] = [x0, x1, label]

        label_data = [unique_highlights[highlight_id] for highlight_id in unique_highlights]
        df = pd.DataFrame(label_data, columns=["time_one", "time_two", "label"])
        df.to_csv(f"{self.output_path}/{self.output_name}.csv", index=False)

    def disconnect_events(self):
        for cid_press, cid_release, cid_scroll in zip(self.cid_press, self.cid_release, self.cid_scroll):
            for ax in self.axes:
                ax.figure.canvas.mpl_disconnect(cid_press)
                ax.figure.canvas.mpl_disconnect(cid_release)
                ax.figure.canvas.mpl_disconnect(cid_scroll)

    def on_scroll(self, event):
        base_scale = 1.1
        if event.button == 'up':
            scale_factor = base_scale
        elif event.button == 'down':
            scale_factor = 1 / base_scale
        else:
            scale_factor = 1

        for ax in self.axes:
            cur_xlim = ax.get_xlim()
            cur_ylim = ax.get_ylim()

            xdata = event.xdata
            ydata = event.ydata

            if xdata is None or ydata is None:
                continue

            new_width = (cur_xlim[1] - cur_xlim[0]) * scale_factor
            new_height = (cur_ylim[1] - cur_ylim[0]) * scale_factor

            relx = (cur_xlim[1] - xdata) / (cur_xlim[1] - cur_xlim[0])
            rely = (cur_ylim[1] - ydata) / (cur_ylim[1] - cur_ylim[0])

            ax.set_xlim([xdata - new_width * (1 - relx), xdata + new_width * (relx)])
            ax.set_ylim([ydata - new_height * (1 - rely), ydata + new_height * (rely)])
            ax.figure.canvas.draw()

        self.update_highlights()

    def update_highlights(self):
        for highlight_id, ax, rect, label, ylim in self.highlights:
            cur_ylim = ax.get_ylim()
            rect.set_y(cur_ylim[0])
            rect.set_height(cur_ylim[1] - cur_ylim[0])
            ax.figure.canvas.draw()

if __name__ == "__main__":
    file_path = input("Please enter the file path: ")
    output_path = input("Please enter the output path: ")
    participant_code = input("Please enter the participant code: ")
    output_name = f"output_{participant_code}"
    df = pd.read_csv(file_path)
    figsize = (100, 20)
    fig, ax = plt.subplots(3, 1, sharex=True, figsize=figsize)
    fig.subplots_adjust(hspace=0)
    ax[0].plot(df["time"], df["xcoord"])
    ax[0].set_ylabel('xcoord')
    ax[1].plot(df["time"], df["ycoord"])
    ax[1].set_ylabel('ycoord')
    ax[2].plot(df["time"], df["zcoord"])
    ax[2].set_ylabel('zcoord')

    for a in ax:
        a.xaxis.set_major_locator(MaxNLocator(nbins=20))

    fig.canvas.toolbar_visible = True

    highlighter = Highlight(ax, output_path, output_name)
    plt.show()
