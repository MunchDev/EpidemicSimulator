import csv_processor
import helper
from helper import print_type_error as t_stderr
from helper import print_error as stderr
import datetime
import json
import numpy as np
import matplotlib.pyplot as plt

f = open("../cache/population.json")
population = json.load(f)
f.close()

def get_country_data(country, date, days):
    """
    Get data for <country> within the last <days> ago, from the <date>.
    Data is endexed so that the most recent entry is at the end of the list.
    Return format: List(date-days, date-days+1, ..., date-1, date)
    """
    
    entries = []
    for i in range(days-1, -1, -1):
        data = csv_processor.parse_data(helper.modify_date(date, -i)).get(country, None)
        if data == None:   
            return -1
        entries.append(data)
    return entries

def validate_timespan(ts):
    if type(ts) != int:
        t_stderr("timespan", int, ts)
        return False
    if ts <= 0:
        stderr("Expected positive timespan, but given {}".format(ts)) 
        return False
    return True

def validate_date(d):
    if type(d) != str:
        t_stderr("date", str, d)
        return False
    if not helper.is_valid_date(d):
        stderr("Expected format for date is 'dd-mm-yyyy', but given {}".format(d))
        return False
    return True

def validate_scale(s):
    if type(s) != str:
        t_stderr("scale", str, s)
        return False
    if s != "log" and s != "linear":
        stderr("Expected value of scale is either 'log' or 'linear', but given {}".format(s))
        return False
    return True

def validate_pltype(p):
    if type(p) != str:
        t_stderr("plot_type", str, p)
        return False
    return True

def validate_country(ct):
    if type(ct) != str:
        if type(ct) == list:
            return True
        else:
            stderr("Expected type of country is <class 'str'> or <class 'list'>, but given {}"\
                   .format(type(country)))
            return -1
    return False

def country_tally_plot(country, date, timespan, *args, **kwargs):
    multiple_countries = validate_country(country)
    if multiple_countries == -1:
        return -1        
    if not validate_date(date):
        return -1    
    if not validate_timespan(timespan):
        return -1
       
    if not multiple_countries:
        scale = kwargs.get("scale", "log")
        if not validate_scale(scale):
            return -1           
        plot_type = kwargs.get("plot_type", "cdra")
        if not validate_pltype(plot_type):
            return -1
        
        data = get_country_data(country, date, timespan)
        if data == -1:
            stderr("'{}' is unavailable!".format(country))
            return -1
        
        x_data = np.linspace(-(timespan-1), 0, num=timespan)       
        plot_enabled = False
        if "c" in plot_type:
            plt.plot(x_data, np.array([x[0] for x in data]), '.b-', label="Confirmed")
            plot_enabled = True
        if "r" in plot_type:
            plt.plot(x_data, np.array([x[1] for x in data]), '.g-', label="Recovered")
            plot_enabled = True
        if "d" in plot_type:
            plt.plot(x_data, np.array([x[2] for x in data]), '.k-', label="Deaths")
            plot_enabled = True
        if "a" in plot_type:
            plt.plot(x_data, np.array([x[3] for x in data]), '.r-', label="Active")
            plot_enabled = True  
        if not plot_enabled:
            stderr("Expected at least one plot type, but given '{}'".format(plot_type))
            return -1
        
        plt.yscale(scale)
        plt.xlabel("Number of days since the latest report")
        plt.ylabel("Number of cases")
        plt.title("COVID-19 tally for " + country)
        plt.legend(loc="best")
        plt.show() 
        return 0
    else:
        n = len(country)            
        scale = kwargs.get("scale", ["log"] * n)
        if type(scale) == str:
            scale = [scale] * n
        if type(scale) != list:
            t_stderr("scale", list, scale)
            return -1
        if len(scale) < n:
            scale += ["log"] * (n - len(scale))
            
        plot_type = kwargs.get("plot_type", ["cdra"] * n)
        if type(plot_type) == str:
            plot_type = [plot_type] * n
        elif type(plot_type) != list:
            stderr("Expected plot type is of <class 'list'> or <class 'str'>, but given {}"\
                   .format(type(plot_type)))
            return -1
        if len(plot_type) < n:
            plot_type += ["log"] * (n - len(scale))
            
        for i in range(n):
            c = country[i]
            s = scale[i]
            p = plot_type[i]
            country_tally_plot(c, date, timespan, scale=s, plot_type=p)
        return 0

def world_tally_plot(countries, colours, date, timespan = 30, scale = "log", plot_type = "c"):
    if type(countries) != list or type(colours) != list or type(date) != str or type(timespan) != int:
        print("Invalid input type")
        return -1
    
    if scale != "log" and scale != "linear":
        print("Invalid scale")
        return -1
    plt.yscale(scale)
    
    chosen_option = None
    options = {"c" : 0, "d" : 1, "r" : 2, "a" : 3}
    for letter in plot_type:
        if letter in options.keys():
            chosen_option = options[letter]
            break          
    if chosen_option == None:
        print("Invalid plot type")
        return -1
    
    if not helper.is_valid_date(date):
        print("Invalid date")
        return -1
    if timespan <= 0:
        print("Invalid timespan! Timespan must be positive")
        return -1
    for country, colour in zip(countries, colours):
        data = get_country_data(country, date, timespan)
        if data == -1:
            print("'{}' is unavailable!".format(country))
            return -1
        
        cases = [x[chosen_option] for x in data]
        x_data = np.linspace(-(timespan-1), 0, num=timespan)
        cases = np.array(cases)
        
        plt.plot(x_data, cases, color=colour, marker=".", linestyle="-", label=country)
    
    ylabel = "Number of "
    if chosen_option == 0:
        ylabel += "confirmed cases"
    elif chosen_option == 1:
        ylabel += "deaths"
    elif chosen_option == 2:
        ylabel += "recovered cases"
    else:
        ylabel += "active cases"
    
    plt.xlabel("Number of days since the latest report")
    plt.ylabel(ylabel)
    plt.title("COVID-19 tallies over the world")
    plt.legend(loc="best")
    plt.show()
    return 0
