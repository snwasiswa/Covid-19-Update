"""Get current cases by using python"""

# Import the covid library
from covid import Covid
from tkinter import*
from tkinter import ttk

import os
import matplotlib
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.pyplot import Figure


# Create object covid
covid_case = Covid()

class Coronavirus:

      def __init__(self, master):

            master.title("Coronavirus Update")
            
            master.configure(bg = 'gray40')
            
            #master.geometry('500x500')
            master.resizable(False, False)

            self.style = ttk.Style()
            self.style.configure('TFrame', background = 'brown1')
            self.style.configure('TButton', background = '#e1d8b9')
            self.style.configure('TLabel', background = '#e1d8b9', font = ('Arial', 13))
            self.style.configure('Header.TLabel', font = ('Arial', 20, 'bold'))  

            self.frame_header = ttk.Frame(master)
            self.frame_header.pack()

            self.logo = PhotoImage(file = 'corona.gif').subsample(3,3)
            ttk.Label(self.frame_header, image = self.logo).grid(row = 0, column = 0, rowspan = 2, sticky = 'w')
            ttk.Label(self.frame_header, text = 'Welcome!', style = 'Header.TLabel').grid(row = 0, column = 1)
            ttk.Label(self.frame_header, wraplength = 300 ,text = 'Source : Johns Hopkins University.'
                      'Data change rapidly; therefore, they might be slightly different with the current numbers',
                      font = ('Arial', 13, 'bold italic')).grid(row = 1, column = 1)
      
            self.frame_content = ttk.Frame(master)
            self.frame_content.pack()

            # Add more labels
            ttk.Label(self.frame_content, text = "Covid-19 Worldwide:").grid(row = 1, column = 0, padx = 0, pady = 10)
            
            self.text1 = Text(self.frame_content, width = 25, height = 7, font = ('Arial', 13),background = 'misty rose')
            self.text1.grid(row = 2, column = 0)

            self.canvas1 = Canvas(self.frame_content, width = 200, height = 105)
            self.canvas1.grid(row = 2, column = 1, columnspan = 2, padx = 6)

            #Create a string variable to be used in the combobox
            self.country = StringVar()
            combobox = ttk.Combobox(self.frame_content, textvariable = self.country)
            combobox.grid(row = 4, column = 0, padx = 10)
            self.country.set('Countries:')
            combobox.config( values = self.covid_countries_names())
            combobox.bind("<<ComboboxSelected>>", self.covid_numbers_country)
        
            ttk.Label(self.frame_content, text = " Choose a country to get update:").grid(row = 3, column = 0, padx = 10, pady = 10)
            self.text2 = Text(self.frame_content, width = 25, height = 7, font = ('Arial', 13), background = 'misty rose')
            self.text2.grid(row = 5, column = 0)

            self.canvas2 = Canvas(self.frame_content, width = 200, height = 105)
            self.canvas2.grid(row = 5, column = 1, columnspan = 2, padx = 6)
            
            ttk.Button(self.frame_content , text = 'Get Update',
                       command = self.covid_numbers_world).grid(row = 1, column = 2, padx = 0, pady = 5)
            ttk.Button(self.frame_content, text = 'Exit',
                       command  = self.exit_program).grid(row = 6, column = 1, padx = 0, pady = 5)


            
      def exit_program(self):

            os._exit(0)

            
      def covid_numbers_world(self):

            list_to_display = []

            end = 3

            list_to_display.append ("Confirmed cases: " + str(covid_case.get_total_confirmed_cases()) + '\n' + '\n')
            list_to_display.append("Active cases: " + str(covid_case.get_total_active_cases()) + '\n' +'\n')
            list_to_display.append("Total recovered: " + str(covid_case.get_total_recovered()) + '\n' + '\n')
            list_to_display.append("Total deaths: " + str(covid_case.get_total_deaths()) + '\n' + '\n')

            for i in range (len(list_to_display)):

                  if i == end:

                        self.text1.config(state=DISABLED)
                  else:

                        for text in list_to_display:
                              self.text1.tag_configure("center", justify = 'center')
                              self.text1.tag_add("center","1.0","end")
                              self.text1.insert(END, text)

            cases = ['Confirmed', 'Active', 'Recovered', 'Deaths']

            numbers = [covid_case.get_total_confirmed_cases(), covid_case.get_total_active_cases(),covid_case.get_total_recovered(),covid_case.get_total_deaths()]

            # Creating figure
            figure = Figure(figsize = (5,4), dpi = 80)

            # Plot the graph inside the figure
            plot = figure.add_subplot(1,1,1)

            plot.bar(cases,numbers)
            plot.set_title("Worldwide", fontsize = 12)
            plot.set_xlabel('Cases', fontsize = 12)
            plot.set_ylabel('Numbers', fontsize = 12)
      
            # Creating canvas
            fig_to_canvas = FigureCanvasTkAgg(figure, self.canvas1)
            fig_to_canvas.draw()

            get_the_drawing = fig_to_canvas.get_tk_widget()
            get_the_drawing.pack(fill =BOTH, expand = True)

            
      def clear1(self):

            self.text1.delete('1.0','end')
            

      def covid_countries_names(self):

            self.clear1()

            countries = covid_case.list_countries()
            all_countries = []

            for country in countries:
                  
                  all_countries.append(country['name'])

            return sorted(all_countries)

      def clear(self):

            self.text2.delete('1.0','end')
            self.canvas2.delete(ALL)

      def covid_numbers_country(self, event):

            self.clear()

            list_to_display = []

            requested_country = covid_case.get_status_by_country_name(self.country.get())

            data_requested = { key: requested_country[key] for key in requested_country.keys() and
                                 {'confirmed','active','deaths','recovered'}

                                }

            list_to_display.append("Comfirmed cases: " + str(data_requested['confirmed']) + '\n' + '\n')
            list_to_display.append("Active cases: " + str(data_requested['active']) + '\n' + '\n')
            list_to_display.append("Total recovered: " + str(data_requested['recovered']) + '\n' + '\n')
            list_to_display.append("Total deaths: " + str(data_requested['deaths']) + '\n' + '\n')

            for text in list_to_display:
                  self.text2.tag_configure("center", justify = 'center')
                  self.text2.insert(END, text)
                  self.text2.tag_add("center","1.0","end")

            cases = ['Confirmed', 'Active', 'Recovered', 'Deaths']
            numbers = [data_requested['confirmed'],data_requested['active'],data_requested['recovered'],data_requested['deaths']]


            try:
                  self.get_the_drawing = self.fig_to_canvas.get_tk_widget().grid_forget()

            except AttributeError:
                  pass
                  
            # Creating figure
            figure = Figure(figsize = (5,4), dpi = 80)

            # Plot the graph inside the figure
            plot = figure.add_subplot(1,1,1)

            plot.bar(cases,numbers)
            plot.set_title(self.country.get(), fontsize = 12)
            
            plot.set_xlabel('Cases', fontsize = 10)
            plot.set_ylabel('Numbers', fontsize = 10)
            #plot.set_tick_params(labelsize=12)

            # Creating canvas
            self.fig_to_canvas = FigureCanvasTkAgg(figure, self.canvas2)
            
            self.fig_to_canvas.get_tk_widget().grid(sticky = 'w')
            self.fig_to_canvas.draw()
                        
def main():
      root = Tk()
      covid  = Coronavirus(root)
      root.mainloop()

if __name__ == "__main__":
      main()
      
