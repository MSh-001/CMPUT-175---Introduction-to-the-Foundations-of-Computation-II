'''
CMPUT 175 - Winter 2026
Assignment 1: Global Trade Analysis

This program:
- analyzes a dataset from a set of data files. 
- Determines where to source each product to minimize the tax they must pay to the government,
  and to maximize the profit margin to realize.
- All results are displayed in formatted tables.

Author: Maryna Shumeiko
'''
class Table:
    '''An object in this class represents a single table'''
    
    STRING_LEFT   = "{value:<{width}}"
    STRING_RIGHT  = "{value:>{width}}"
    STRING_CENTER = "{value:^{width}}"

    NUMBER_CURRENCY = "$ {value:>{width},.2f}"
    NUMBER_FLOAT    = "{value:>{width},.2f}"
    NUMBER_PERCENT  = "{value:>{width}.1f}%"
    NUMBER_INTEGER  = "{value:>{width}.0f}"

    TYPE_FLOAT = 'float'
    TYPE_STR = 'string'
    TYPE_INT = 'integer'

    def __init__(self, key_col_name = None):
        '''
        Parameters:
           - self: the table to initialize
           - key_col_name: (str, optional): Name of the column to use as the 
             primary key for data dictionary. If None, sequential line 
             numbers are used as keys.
        Initializes the values of the attributes of a table object
        Creates and returns a table object
        '''
        self.key_col_name = key_col_name
        self.filename = None
        self.column_names = []
        self.columns_width = []
        self.column_types = []
        self.header_styles = []
        self.row_styles = []
        self.data = {}
        self.num_of_lines = 0
    
    def add_column(self, column_name, column_type):
        self.column_names.append(column_name)
        self.column_types.append(column_type)

    def load_data_from_file(self, filename, first_line_names=True):
        '''
        Parameters:
           - self: the table object
           - filename (str): name of the text data file
           - first_line_names (boolean): first line in file is column names
        Loads data from a text file:
            - reads column names from the first line of the file
            - reads data rows from subsequent lines. 
            - increments line count (mum_of_lines) for each row processed
        Input validation:
            - raises OSError if the file cannot be opened or read, including the message with description of the error
            - other exceptions are propagated without modification
        Does not return anything
        '''
        self.filename = filename
        try:
            assert len(self.column_types) > 0, f"Column data types are not set for file '{self.filename}'."
            with open(self.filename, mode='r', encoding='UTF-8') as file:
                for line in file:
                    assert len(line.strip()) > 0, f"Empty line {self.num_of_lines+1} in file: '{self.filename}'."
                    items = line.strip().split(',')
                    assert len(items) == len(self.column_types), f"Line {self.num_of_lines+1} of file '{self.filename}'" + \
                                        f"has {len(items)} values but the table expects {len(self.column_types)} columns."

                    for i in range(len(items)):
                        items[i] = items[i].strip()
                    
                    if first_line_names and self.num_of_lines == 0:
                        self.column_names = items
                        self.num_of_lines += 1
                    else: 
                        self.add_row(items)
        except OSError as err:
            raise OSError(f'Error file operation. Filename: "{self.filename}"\nError: {err}')
        except Exception as err:
            raise

    def add_row(self, entries):
        '''
        Parameters:
           - self: the table object
           - entries (list): list of values for each column
        Creates a dictionary from the entries list:
            - converts values to appropriate types based on column definitions
            - Adds the row information to the table data using either the line number as key
              or the value from the key column if specified.
        Input validation:
            - raises ValueError if type conversion fails
            - other exceptions are propagated without modification
        Does not return anything
        '''
        a_dict = {}
        if self.key_col_name == None:
            self.num_of_lines += 1
        for i in range(len(self.column_names)):

            try:
                if self.column_types[i] == Table.TYPE_FLOAT:
                    a_dict[self.column_names[i]] = float(entries[i])
                elif self.column_types[i] == Table.TYPE_INT:
                    a_dict[self.column_names[i]] = int(entries[i])
                else: a_dict[self.column_names[i]] = entries[i]
            except ValueError as err:
                raise ValueError(f'Error validate data. \nFilename: "{self.filename}", column name: "{self.column_names[i]}", ' + 
                                f'column type: "{self.column_types[i]}", column value: "{entries[i]}"\nError: {err}')
            except Exception as err:
                raise

            if self.key_col_name == None:
                self.data[self.num_of_lines] = a_dict
            else: self.data[a_dict[self.column_names[self.column_names.index(self.key_col_name)]]] = a_dict

    def set_column_names(self, column_names):
        '''
        Parameters:
           - self: the table object
           - column_names (list): list of column name strings
        Sets the column names for the table. Returns nothing.
        '''
        self.column_names = column_names

    def set_columns_types(self, columns_types):
        '''
        Parameters:
           - self: the table object
           - columns_types (list): list of type identifiers for each column
        Sets the data type for each column in the table. Returns nothing.
        '''
        self.column_types = columns_types

    def find_longest_str(self, column_name):
        '''
        Parameters:
           - self: the table object
           - column_name (str): name of the column to check
        Finds the maximum string length among all values in the specified column,
        including the column header itself after formating using the column's style. 
        Returns the maximum length as an integer.
        '''
        max_length = len(column_name)
        idx = self.column_names.index(column_name)
        for row_info in self.data.values():
            row_items = list(row_info.values())
            length_formated_value = len(self.format_value(row_items[idx],self.row_styles[idx],0)) 
            if length_formated_value > max_length:
                max_length = length_formated_value
        return max_length

    def set_columns_width(self):
        '''
        Parameters:
           - self: the table object
        Sets width for each column based on the longest string value in that column using find_longest_str method.
        Returns nothing.
        '''
        for column_name in self.column_names:
            self.columns_width.append(self.find_longest_str(column_name))
        

    def set_header_styles(self, header_styles):
        '''
        Parameters:
           - self: the table object
           - header_styles (list): list of format strings for column headers
        Sets the formatting styles for column headers. Returns nothing.
        '''
        self.header_styles = header_styles
    
    def set_row_styles(self, row_styles):
        '''
        Parameters:
           - self: the table object
           - row_styles (list): list of format strings for data rows
        Sets the formatting styles for data rows. Returns nothing.
        '''
        self.row_styles = row_styles
    
    def get_data(self):
        '''
        Parameters:
           - self: the table object
        Returns table data, type dict.
        '''
        return self.data
    
    def get_entry(self, key, column_name):
        '''
        Parameters:
           - self: the table object
           - key: key value to look up in the table data
           - column_name (str): column name to get value
        Returns the value from the specified column in the row for the given key, or None if not found.
        '''
        key_value = self.data.get(key)
        if key_value == None: 
            return None
        else: 
            return key_value.get(column_name)
        
    def format_value(self, item, style, column_width):
        '''
        Parameters:
           - self: the table object
           - item: value to format
           - style (str): format string template
           - column_width (int): width for the formatted value
        Formats a value according to the given style and width, 
        accounting for extra characters in the format string. 
        Returns the formatted string.
        '''
        return style.format(value=item, width=column_width - (style.index("{") + len(style) - style.rindex("}") - 1))

    def print_table(self):
        '''
        Parameters:
           - self: the table object
        Prints the formatted table to the console with headers, data rows, and borders.
        Calls format_value method to provide proper formatting.
        Does not return anything.
        '''
        c_sep = '|'
        r_sep = '-'
        corner_sep = '+'
            
        # Printing the HEADER
        header_line = c_sep
        line_separator = corner_sep
        for i in range(len(self.column_names)):
            header_line += f' {self.format_value(self.column_names[i], self.header_styles[i], self.columns_width[i])} {c_sep}'
            line_separator += r_sep*(self.columns_width[i]+2) + corner_sep
        
        print(line_separator)
        print(header_line)
        print(line_separator)
        
        # Printing DATA
        for row in self.data.values():
            line = c_sep
            for i in range(len(list(row.values()))):
                line += f' {self.format_value(list(row.values())[i], self.row_styles[i], self.columns_width[i])} {c_sep}'
            print(line)
        
        print(line_separator)

class CountryDeficit(Table):
    '''An object in this class represents a table of country trade data'''
    def compute_deficit(self):
        '''
        Parameters:
           - self: the table object of country trade data 
        
        Computes the deficit for each country by subtracting Exports from Imports
        Adds or updates the column 'Trade Deficit (Billions USD)' for each country
        Does not return anything.
        '''
        for row in self.data.values():
            row['Trade Deficit (Billions USD)'] = row['Imports'] - row['Exports']

def get_countries_with_highest_deficits(countries):
    '''
    Parameters:
       - countries: table object containing country trade data
    
    Creates a result table showing the top five deficit countries, sorted in descending order by trade deficit
    Prints the formatted table.
    Does not return anything
    '''
    result_table = Table(key_col_name='Country')
    result_table.set_column_names(['Country','Trade Deficit (Billions USD)'])
    result_table.set_columns_types([Table.TYPE_STR, Table.TYPE_FLOAT])
    result_table.set_header_styles([Table.STRING_LEFT, Table.STRING_CENTER])
    result_table.set_row_styles([Table.STRING_LEFT, Table.NUMBER_CURRENCY])

    for value in sorted(countries.get_data().values(), key=lambda item: -item['Trade Deficit (Billions USD)'])[:5]: 
        result_table.add_row([value['Country'], value['Trade Deficit (Billions USD)']])
    
    result_table.set_columns_width()
    result_table.print_table()    

def products_num_per_industry(products_data):
    '''
    Parameters:
        - products_data: dictionary containing product information

    Counts how many products belong to each industry. 
    Sorts the output in the alphabetical order of industries.
    Creates a result table showing each industry and the corresponding number of products.
    Prints the formatted table.

    Returns a set of all unique industry names in the products data.
    '''
    industry_products = {}

    for product in products_data.values():
        if  industry_products.get(product['Industry']) == None:
            industry_products[product['Industry']] = 1
        else:
            industry_products[product['Industry']] += 1

    result_table = Table(key_col_name='Industry')
    result_table.set_column_names(['Industry','Number of Products'])
    result_table.set_columns_types([Table.TYPE_STR, Table.TYPE_INT])
    result_table.set_header_styles([Table.STRING_CENTER, Table.STRING_CENTER])
    result_table.set_row_styles([Table.STRING_LEFT, Table.NUMBER_INTEGER])
    for key, value in sorted(industry_products.items()): 
        result_table.add_row([key, value])
    
    result_table.set_columns_width()
    result_table.print_table()
    return set(industry_products.keys())

def find_exclusive_products(product_country_data, products_table, countries_table):
    '''
    Parameters:
        - product_country_data: dictionary containing product-country associations
        - products_table: table object containing product information
        - countries_table: table object containing country trade data
    
    Identifies products produced only in one country.
    Creates a result table containing the following, sorted alphabetically by product name:
        - PID
        - Product Name
        - The Producing Country
    
    Prints the formatted table.
    Returns a dictionary of exclusive products keyed by PID, where each value
    is a dictionary containing PID, Product Name, Country Code, and Country name.
    '''
    product_by_country = {}
    for product in product_country_data.values():
        pid = product['PID']
        if product_by_country.get(pid) == None:
            product_by_country[pid] = {}
        if product_by_country[pid].get(product['Country Code']) == None:
            product_by_country[pid][product['Country Code']] = 1
        else: 
            product_by_country[pid][product['Country Code']] += 1

    exclisive_product = {}

    for pid, value in product_by_country.items():
        if len(value) == 1:
            code_country = list(value.keys())[0]
            product_name = products_table.get_entry(pid, "Product Name")
            country_name = countries_table.get_entry(code_country, "Country")
            if product_name != None and country_name != None:
                exclisive_product[pid] = {"PID": pid,
                                          "Product Name": product_name,
                                          'Country Code': code_country,
                                          "Country": country_name }
                               
    result_table = Table(key_col_name='PID')
    result_table.set_column_names(['PID','Product Name','Producing Country'])
    result_table.set_columns_types([Table.TYPE_STR, Table.TYPE_STR, Table.TYPE_STR])
    result_table.set_header_styles([Table.STRING_LEFT, Table.STRING_LEFT, Table.STRING_LEFT])
    result_table.set_row_styles([Table.STRING_LEFT, Table.STRING_LEFT, Table.STRING_LEFT]) 
    
    for value in sorted(exclisive_product.values(), key=lambda item: item['Product Name']): 
        result_table.add_row([value["PID"], value["Product Name"], value["Country"] ])

    result_table.set_columns_width()
    result_table.print_table()

    return exclisive_product

def countries_most_exclusive_products(exclisive_product):
    '''
    Parameters:
        - exclisive_product: a dictionary of exclusive products keyed by PID, where each value
          is a dictionary containing PID, Product Name, Country Code, and Country name. 
    
    Determines which country produces the highest number of exclusive products
    Creates a result table showing the country name and the number of exclusive products for the 
    countries with the maximum count of exclusive products.
    If there is a tie, sorts alphabetically by country name.
    Prints the formatted table.
    Does not return anything
    '''
    country_produces_exclusive = {}

    for value in exclisive_product.values():
        if country_produces_exclusive.get(value["Country"]) == None:
            country_produces_exclusive[value["Country"]] = 1
        else:
            country_produces_exclusive[value["Country"]] += 1

    result_table = Table()
    result_table.set_column_names(['Country', "No. of Exclusive Products"])
    result_table.set_columns_types([Table.TYPE_STR, Table.TYPE_INT])
    result_table.set_header_styles([Table.STRING_LEFT, Table.STRING_LEFT])
    result_table.set_row_styles([Table.STRING_LEFT, Table.NUMBER_INTEGER]) 
    
    max_value = None
    i = 0
    for key, value in sorted(country_produces_exclusive.items(), key=lambda item: (-item[1], item[0])):
        if i == 0: 
            max_value = value
        if value == max_value:
            result_table.add_row([key, value])
        i += 1 

    result_table.set_columns_width()
    result_table.print_table()

def industries_fewest_exclusives(product_country_data, products_table):
    '''
    Parameters:
        - product_country_data: dictionary containing product-country associations
        - products_table: table object containing product information

    Determines which industry contains the least number of exclusive products
    Creates a result table showing the industry and the number of exclusive products for the 
    industries with the least count of exclusive products.
    If there is a tie, sorts alphabetically by industry name.
    Prints the formatted table.
    Does not return anything
    '''
    product_by_country = {}
    for product in product_country_data.values():
        pid = product['PID']
        if product_by_country.get(pid) == None:
            product_by_country[pid] = []
        if not product['Country Code'] in product_by_country[pid]:
            product_by_country[pid].append(product['Country Code'])

    industries_fewest = {}

    for pid, value in product_by_country.items():
        if len(value) == 1:
            industry = products_table.get_entry(pid, "Industry")
            if industries_fewest.get(industry) == None:
                industries_fewest[industry] = 1
            else:
                industries_fewest[industry] += 1

    result_table = Table()
    result_table.set_column_names(['Industry', "No. of Exclusive Products"])
    result_table.set_columns_types([Table.TYPE_STR, Table.TYPE_INT])
    result_table.set_header_styles([Table.STRING_LEFT, Table.STRING_LEFT])
    result_table.set_row_styles([Table.STRING_LEFT, Table.NUMBER_INTEGER]) 
    
    min_value = None
    i = 0
    for key, value in sorted(industries_fewest.items(), key=lambda item: (item[1], item[0])):
        if i == 0: 
            min_value = value
        if value == min_value:
            result_table.add_row([key, value])
        i += 1 

    result_table.set_columns_width()
    result_table.print_table()

def most_productive_countries(products_country_data, countries):
    '''
    Parameters:
        - products_country_data: dictionary containing product-country associations
        - countries: table object containing country trade data
    
    Identifies the country that produces the largest number of total products.
    Creates a result table showing the country name and the number of products for the 
    countries with the maximum product count. 
    If there is a tie, sorts alphabetically by country name.
    Prints the formatted table.
    Does not return anything
    '''
    most_productive = {}

    for value in products_country_data.values():
        country = countries.get_entry(value["Country Code"], "Country")
        if country != None:
            if most_productive.get(country) == None:
                most_productive[country] = 1
            else:
                most_productive[country] += 1

    result_table = Table()
    result_table.set_column_names(['Country', "Number of Products"])
    result_table.set_columns_types([Table.TYPE_STR, Table.TYPE_INT])
    result_table.set_header_styles([Table.STRING_LEFT, Table.STRING_LEFT])
    result_table.set_row_styles([Table.STRING_LEFT, Table.NUMBER_INTEGER]) 
    
    max_value = None
    i = 0
    for key, value in sorted(most_productive.items(), key=lambda item: (-item[1], item[0])):
        if i == 0: 
            max_value = value
        if value == max_value:
            result_table.add_row([key, value])
        i += 1 

    result_table.set_columns_width()
    result_table.print_table()

def most_widespread_products(product_country_data, products_table):
    '''
    Parameters:
        - product_country_data: dictionary containing product-country associations
        - products_table: table object containing product information
    Identifies products whose number of producing countries falls within the top three values.
    If multiple products share the same number of producing countries, includes all of them.

    Creates a result table showing Product Name, Number of Countries producing it.

    Sorts the output by:
        - Number of countries (descending)
        - Product name (alphabetically) for ties
    
    Prints the formatted table.
    Does not return anything
    '''
    product_by_country = {}
    for product in product_country_data.values():
        pid = product['PID']
        if product_by_country.get(pid) == None:
            product_by_country[pid] = {}
        if product_by_country[pid].get(product['Country Code']) == None:
            product_by_country[pid][product['Country Code']] = 1
        else: 
            product_by_country[pid][product['Country Code']] += 1

    widespread_products = {}

    for pid, value in product_by_country.items():
        product_name = products_table.get_entry(pid, "Product Name")
        if product_name != None :
            widespread_products[product_name] = len(value)

    top_3_value = sorted(set(value for value in widespread_products.values()), reverse=True)[:3]

    result_table = Table()
    result_table.set_column_names(['Product Name','Number of Countries'])
    result_table.set_columns_types([Table.TYPE_STR, Table.TYPE_STR])
    result_table.set_header_styles([Table.STRING_LEFT, Table.STRING_LEFT])
    result_table.set_row_styles([Table.STRING_LEFT, Table.NUMBER_INTEGER]) 
    
    for key, value in sorted(widespread_products.items(), key=lambda item: (-item[1], item[0])):
        if value in top_3_value:
            result_table.add_row([key, value])

    result_table.set_columns_width()
    result_table.print_table()

def outrageous_tariffs(tariff_data, countries):
    '''
    Parameters:
        - tariff_data: dictionary containing tariff information
        - countries: table object containing country trade data
    
    Identifies which countries face tariffs above 50% on one or more of their industries
    Creates a result table showing country names
    Sorts the output alphabetically by country name.

    Prints the formatted table.
    Does not return anything
    '''
    tariff_above_50 = {}
    for key, value in tariff_data.items():
        country = countries.get_entry(value["Country Code"], "Country")
        if country != None: 
            if value["Percentage"] >= 50:
                tariff_above_50[country] = value["Percentage"]

    result_table = Table()
    result_table.set_column_names(['Country'])
    result_table.set_columns_types([Table.TYPE_STR])
    result_table.set_header_styles([Table.STRING_LEFT])
    result_table.set_row_styles([Table.STRING_LEFT]) 
    
    for key, value in sorted(tariff_above_50.items(), key=lambda item: item[0]):
        result_table.add_row([key, value])

    result_table.set_columns_width()
    result_table.print_table()

def tariff_free(tariff_data, countries_data):
    '''
    Parameters:
        - tariff_data: dictionary containing tariff information
        - countries_data: dictionary object containing country trade data

    Identifies which countries have no tariffs at all imposed on them
    Creates a result table showing country names
    Sorts the output alphabetically by country name.

    Prints the formatted table.
    Does not return anything
    '''
    countries_with_tariff = {}
    for value in tariff_data.values():
        countries_with_tariff[value["Country Code"]] = value["Percentage"]   
    
    countries_free_tariff = {}
    for code_country, value in countries_data.items():
        if countries_with_tariff.get(code_country) == None:            
            countries_free_tariff[value["Country"]] = 0

    result_table = Table()
    result_table.set_column_names(['Country'])
    result_table.set_columns_types([Table.TYPE_STR])
    result_table.set_header_styles([Table.STRING_LEFT])
    result_table.set_row_styles([Table.STRING_LEFT]) 
    
    for key, value in sorted(countries_free_tariff.items(), key=lambda item: item[0]):
        result_table.add_row([key, value])

    result_table.set_columns_width()
    result_table.print_table()

def selective_tariff_countries(industry, tariff_data, countries):
    '''
    Parameters:
        - industry: a set of all unique industry names in the products data
        - tariff_data: dictionary containing tariff information
        - countries: table object containing country trade data
    Identifies countries that have tariffs on some industries but not on others.
    Creates a result table showing country name and industries with no tariff in that country
    Sorts the output alphabetically by country name, then industry name.
    Prints the formatted table.
    Does not return anything.
    '''
    tariff_industries = {}

    for value in tariff_data.values():
        if tariff_industries.get(value["Country Code"]) == None:
            tariff_industries[value["Country Code"]] = {}

        tariff_industries[value["Country Code"]][value["Industry"]] = value["Percentage"]

    selective_tariff = {}
    for code_country, value in tariff_industries.items():
        industry_diff = industry.difference(set(value.keys()))
        if len(industry_diff) > 0:
            country = countries.get_entry(code_country, "Country")
            if country != None:
                selective_tariff[country] = industry_diff 

    result_table = Table()
    result_table.set_column_names(['Country', 'Industry'])
    result_table.set_columns_types([Table.TYPE_STR, Table.TYPE_STR])
    result_table.set_header_styles([Table.STRING_LEFT, Table.STRING_LEFT])
    result_table.set_row_styles([Table.STRING_LEFT, Table.STRING_RIGHT]) 
    
    for key, value in sorted(selective_tariff.items(), key=lambda item: (item[0], item[1])):
        for item in value:
            result_table.add_row([key, item])

    result_table.set_columns_width()
    result_table.print_table()

def get_country_tariff(tariff_data):
    '''
    Parameters:
        - tariff_data: dictionary containing tariff information
    Creates and returns a dictionary country_tarif with country codes as keys and values are 
    dictionaries of industries and their corresponding tariff percentages.
    '''
    country_tariff = {}
    for value in tariff_data.values():

        country_code = value["Country Code"]

        if country_tariff.get(country_code) == None:
            country_tariff[country_code] = {}

        if country_tariff[country_code].get(value["Industry"]) == None:
            country_tariff[country_code][value["Industry"]] = value["Percentage"]             
    
    return country_tariff

def get_industry_tariff(code_country, industry, country_tariff):
    '''
    Parameters:
    - code_country: country code, type str
    - industry: industry name, type str
    - country_tariff: dictionary mapping country codes to dictionaries of industries and their tariff percentages

    Returns the tariff percentage for the given industry in the specified country.
    If the country or the industry is not found, returns 0.
    '''
    if country_tariff.get(code_country) == None:
        return 0
    else:
        return country_tariff[code_country].get(industry, 0) 

def cheapest_import_strategy(products, products_country_data, countries, tariff_data):
    '''
    Parameters:
        - products: table object containing product information
        - product_country_data: dictionary containing product-country associations
        - countries: table object containing country trade data
        - tariff_data: dictionary containing tariff information

    For each product:
        - finds the best deal considering your country's tariffs on each country.
        - produces a complete cost breakdown per product using the best deal:
            - shows the cost before tariffs (Actual Cost)
            - shows the tariff percentage (Tariff %)
            - shows the applied tariff amount (Tariff Val)
            - shows the new cost of the product (Total Cost)
        - produces a total cost breakdown for the entire shopping list:
            - cost of shopping list before tariffs
            - total tariffs paid
            - grand total for the shopping list
    Sorts the the output by appearance of products in the shopping list 
    Prints the formatted table.
    Does not return anything.
    '''
    shopping_list = Table()
    shopping_list.set_column_names(['PID'])
    shopping_list.set_columns_types([Table.TYPE_STR])
    shopping_list.load_data_from_file('shopping_list.txt', first_line_names=False)
  
    shoping_products = shopping_list.get_data()

    country_tariff = get_country_tariff(tariff_data)

    best_deal = {}
    for value in products_country_data.values():

        pid = value["PID"]
        code_country = value["Country Code"]
        product_industry = products.get_entry(pid, "Industry") 
        product_tariff = get_industry_tariff(code_country, product_industry, country_tariff)
        
        if best_deal.get(pid) == None:
            best_deal[pid] ={"Country Code": code_country,
                             "Countries": 1,
                             "Industry": product_industry, 
                             "Percentage": product_tariff,
                             "Price": value["Price"],
                             "Cost": value["Price"]*(1+product_tariff/100) }
        else:
            best_deal[pid]["Countries"] += 1
            if value["Price"]*(1+product_tariff/100) < best_deal[pid]["Cost"]:
                best_deal[pid] ={"Country Code": code_country,
                                 "Countries": best_deal[pid]["Countries"],
                                 "Industry": product_industry, 
                                 "Percentage": product_tariff,
                                 "Price": value["Price"],
                                 "Cost": value["Price"]*(1+product_tariff/100) }
        
    result_table = Table()
    result_table.set_column_names(["Product Name", "Countries", "Best Country", "Actual Cost", 
                                   "Tariff %", "Tariff Val", "Total Cost"])
    result_table.set_columns_types([Table.TYPE_STR, Table.TYPE_INT, Table.TYPE_STR, Table.TYPE_FLOAT, 
                                    Table.TYPE_FLOAT, Table.TYPE_FLOAT, Table.TYPE_FLOAT])
    result_table.set_header_styles([Table.STRING_LEFT, Table.STRING_LEFT, Table.STRING_LEFT, Table.STRING_LEFT,
                                    Table.STRING_LEFT, Table.STRING_LEFT, Table.STRING_LEFT])
    result_table.set_row_styles([Table.STRING_LEFT, Table.NUMBER_INTEGER, Table.STRING_LEFT, Table.NUMBER_CURRENCY,
                                 Table.NUMBER_PERCENT, Table.NUMBER_CURRENCY, Table.NUMBER_CURRENCY]) 

    sum_actual_cost = 0
    sum_tariff = 0

    for value in shoping_products.values():
        pid = value["PID"]
        product_name = products.get_entry(pid, "Product Name")
        best_deal_info = best_deal.get(pid)
        if best_deal_info == None:
            result_table.add_row([product_name, None, None, None, None, None, None])
        else:
            sum_actual_cost += best_deal_info["Price"]
            sum_tariff += best_deal_info["Price"]*best_deal_info["Percentage"]/100
            result_table.add_row([product_name, 
                                  best_deal_info["Countries"], 
                                  countries.get_entry(best_deal_info["Country Code"], "Country"), 
                                  best_deal_info["Price"],
                                  best_deal_info["Percentage"],  
                                  best_deal_info["Price"]*best_deal_info["Percentage"]/100, 
                                  best_deal_info["Cost"]] )

    result_table.set_columns_width()
    result_table.print_table()

    print(f"\nCost Before Tariff: {Table.NUMBER_CURRENCY.format(value=sum_actual_cost, width=0)}")
    print(f"Total Tariff Paid: {Table.NUMBER_CURRENCY.format(value=sum_tariff, width=0)}")
    print(f"Grand Total: {Table.NUMBER_CURRENCY.format(value=sum_actual_cost+sum_tariff, width=0)}")

def main():
    '''
    - Loads country, product, product-country, and tariff data from files.
    - Computes trade deficits for countries.
    - Performs analysis on product availability:
        - products per industry
        - exclusive products
        - countries with most exclusive products
        - industries with fewest exclusive products
        - most productive countries
        - most widespread products
    - Analyzes government tariffs decisions:
        - outrageous tariffs
        - tariff-free countries
        - selective tariff countries
    - Calculates cheapest import strategy for a shopping list under tariffs.
    
    Handles unexpected errors and prints a message if they occur.
    '''
    try:
        countries = CountryDeficit(key_col_name='Country Code')
        countries.set_columns_types([Table.TYPE_STR, Table.TYPE_STR, Table.TYPE_FLOAT, Table.TYPE_FLOAT])
        countries.load_data_from_file('country.txt')
        countries.add_column('Trade Deficit (Billions USD)', Table.TYPE_FLOAT)
        countries.compute_deficit()

        products = Table(key_col_name='PID')
        products.set_columns_types([Table.TYPE_STR, Table.TYPE_STR, Table.TYPE_STR])
        products.load_data_from_file('product.txt')

        products_country = Table()
        products_country.set_columns_types([Table.TYPE_STR, Table.TYPE_STR, Table.TYPE_FLOAT])
        products_country.load_data_from_file('product_country.txt')

        # SECTION A - Understanding Global Trade
        print("SECTION A: 1.Countries With Highest Trade Deficits")
        get_countries_with_highest_deficits(countries)

        # SECTION B - Understanding Product Availability
        
        print("\nSECTION B: 1.Products Per Industry")
        industry_set = products_num_per_industry(products.get_data())

        print("\nSECTION B: 2.Exclusive Products")
        exclisive_product = find_exclusive_products(products_country.get_data(), products, countries)

        print("\nSECTION B: 3.Countries With Most Exclusive Products")
        countries_most_exclusive_products(exclisive_product)

        print("\nSECTION B: 4. Industries With Fewest Exclusives")
        industries_fewest_exclusives(products_country.get_data(), products)

        print("\nSECTION B: 5. Most Productive Countries")
        most_productive_countries(products_country.get_data(), countries)

        print("\nSECTION B: 6.Most Widespread Products")
        most_widespread_products(products_country.get_data(), products)
    
        # SECTION C - Analyzing Government’s Tariff Decisions

        tariff = Table()
        tariff.set_columns_types([Table.TYPE_STR, Table.TYPE_STR, Table.TYPE_INT])
        tariff.load_data_from_file('tariff.txt')

        print("\nSECTION C: 1. Outrageous Tariffs")
        outrageous_tariffs(tariff.get_data(), countries)

        print("\nSECTION C: 2. Tariff-Free Countries")
        tariff_free(tariff.get_data(), countries.get_data())

        print("\nSECTION C: 3. Selective Tariff Countries")
        selective_tariff_countries(industry_set, tariff.get_data(), countries)

        # SECTION D - Shopping List Cost Breakdown
        
        print("\nSECTION D: 1. Cheapest Import Strategy Under Tariffs")
        cheapest_import_strategy(products, 
                                products_country.get_data(), 
                                countries, 
                                tariff.get_data() ) 

    except Exception as err:
        print(f"Unexpected ERROR: {err}")
        print("Programm termination due ERROR")

if __name__ == '__main__':
    main()