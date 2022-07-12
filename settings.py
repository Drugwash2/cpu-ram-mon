#!/usr/bin/python3 -B

try:
	import gi
	gi.require_version('Gtk', '3.0')
except:
	print("Error importing the gi module!")
	sys.exit()
import os
os.environ["PYTHONDONTWRITEBYTECODE"] = "1"
from JsonSettingsWidgets import *
from gi.repository import Gdk, Gio, Gtk
#================================================================
class Thresholds(SettingsWidget):
	def __init__(self, info, key, settings):
		SettingsWidget.__init__(self)
		self.settings = settings
		self.set_border_width(2)
		self.set_spacing(5)
		self.props.margin = 2
		self.btns = self.settings.get_value("buttons-type")
#### Main Grid
		self.grid = Gtk.Grid(halign=Gtk.Align.START, valign=Gtk.Align.CENTER \
			, margin = 0, column_spacing = 5, row_spacing = 3)
		self.pack_start(self.grid, False, False, 0)
### Row 1: Selection
## Label
		label1 = Gtk.Label(_("Values:"), halign=Gtk.Align.END)
## Radio Button 1
		btn1 = Gtk.RadioButton(label=self.settings.get_property("temp-default", "description"))
		btn1.set_mode(self.btns)		# True=radiobutton, False=toggle button
		btn1.set_halign(Gtk.Align.CENTER)
		btn1.set_valign(Gtk.Align.CENTER)
		self.settings.bind("temp-default", btn1, 'active', Gio.SettingsBindFlags.DEFAULT)
		btn1.set_tooltip_text(self.settings.get_property("temp-default", "tooltip"))
## Radio Button 2
		btn2 = Gtk.RadioButton(group=btn1, label=self.settings.get_property("temp-custom", "description"))
		btn2.set_mode(self.btns)		# True=radiobutton, False=toggle button
		btn2.set_halign(Gtk.Align.CENTER)
		btn2.set_valign(Gtk.Align.CENTER)
		self.settings.bind("temp-custom", btn2, 'active', Gio.SettingsBindFlags.DEFAULT)
		btn2.connect('toggled', self.tempCustom)
		btn2.set_tooltip_text(self.settings.get_property("temp-custom", "tooltip"))
### Row 2: Values
## Label
		label2 = Gtk.Label(_("High / Critical:"), halign=Gtk.Align.END)
## Spinbutton 1
		mins = self.settings.get_property("high", "min")
		maxs = self.settings.get_property("high", "max")
		step = self.settings.get_property("high", "step")
		ttip = self.settings.get_property("high", "tooltip")
		val = self.settings.get_value("high")
		self.sp1 = Gtk.SpinButton.new_with_range(mins, maxs, step)
		self.sp1.set_wrap(False)
		self.sp1.set_value(val)
		self.sp1.set_tooltip_text(ttip)
		self.settings.bind("high", self.sp1, 'value', Gio.SettingsBindFlags.DEFAULT)
## Spinbutton 2
		mins = self.settings.get_property("crit", "min")
		maxs = self.settings.get_property("crit", "max")
		step = self.settings.get_property("crit", "step")
		ttip = self.settings.get_property("crit", "tooltip")
		val = self.settings.get_value("crit")
		self.sp2 = Gtk.SpinButton.new_with_range(mins, maxs, step)
		self.sp2.set_wrap(False)
		self.sp2.set_value(val)
		self.sp2.set_tooltip_text(ttip)
		self.settings.bind("crit", self.sp2, 'value', Gio.SettingsBindFlags.DEFAULT)
### Row 3: VColors
## Label
		label3 = Gtk.Label(_("Bkg. colors:"), halign=Gtk.Align.END)
## Colorchooser Buttons
		bcol = ["color-high", "color-crit"]
		for i in bcol:
			j = "btn" + str(bcol.index(i)+3)
			color = self.settings.get_value(i)
			rgba = Gdk.RGBA()
			rgba.parse(color)
			globals()[j] = Gtk.ColorButton.new_with_rgba(rgba)
			desc = self.settings.get_property(i, "description")
			globals()[j].set_title(_("Select ") + desc)
			globals()[j].set_tooltip_text(desc + "\n\n" + self.settings.get_property(i, "tooltip"))
			globals()[j].connect('color-set', self.saveColor, i)
		btn5 = Gtk.CheckButton(label="Old-school")
		btn5.set_mode(False)		# True=checkbutton, False=toggle button
		btn5.set_halign(Gtk.Align.CENTER)
		btn5.set_valign(Gtk.Align.CENTER)
		self.settings.bind("buttons-type", btn5, 'active', Gio.SettingsBindFlags.DEFAULT)
		btn5.set_tooltip_text(_("Enable this to have old-school radio buttons in Settings"))
#================================================================
### Grouping
		self.grid.add(label1)
		self.grid.attach(btn1, 1, 0, 1, 1)
		self.grid.attach(btn2, 2, 0, 1, 1)
		self.grid.attach(Gtk.Separator.new(Gtk.Orientation.HORIZONTAL), 0, 1, 3, 1)
		self.grid.attach(label2, 0, 2, 1, 1)
		self.grid.attach(self.sp1, 1, 2, 1, 1)
		self.grid.attach(self.sp2, 2, 2, 1, 1)
		self.grid.attach(Gtk.Separator.new(Gtk.Orientation.HORIZONTAL), 0, 3, 3, 1)
		self.grid.attach(label3, 0, 4, 1, 1)
		self.grid.attach(btn3, 1, 4, 1, 1)
		self.grid.attach(btn4, 2, 4, 1, 1)
		self.grid.attach(Gtk.Separator.new(Gtk.Orientation.HORIZONTAL), 0, 5, 3, 1)
		self.grid.attach(btn5, 1, 6, 1, 1)
		self.grid.show()
#================================================================
	def tempCustom(self, btn):
		pass

	def saveColor(self, btn, key):
		val = btn.get_rgba().to_string()
		self.settings.set_value(key, val)
## End of file
